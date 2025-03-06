#!/usr/bin/env python
import os
import json
from typing import Optional, Dict, Any, List
import requests
from dotenv import load_dotenv
from modelcontextprotocol.fastmcp import FastMCP, Message, ToolCall

# 載入環境變數
load_dotenv()

# Langflow API 設定
BASE_API_URL = os.getenv("LANGFLOW_API_URL", "http://127.0.0.1:7864")
FLOW_ID = os.getenv("LANGFLOW_FLOW_ID", "2dae8e68-a6a4-406d-8ee2-2960cec2be70")
ENDPOINT = os.getenv("LANGFLOW_ENDPOINT", "")  # 可以在 flow 設定中指定特定的端點名稱
API_KEY = os.getenv("LANGFLOW_API_KEY", None)

# 預設的 tweaks 設定
DEFAULT_TWEAKS = {
  "ChatInput-D5Ljc": {},
  "ChatOutput-kJ67U": {},
  "ParseData-5woPt": {},
  "File-suptA": {},
  "Prompt-XtPm2": {},
  "MistralModel-6SiHM": {}
}

def run_flow(
    message: str,
    endpoint: str = ENDPOINT or FLOW_ID,
    output_type: str = "chat",
    input_type: str = "chat",
    tweaks: Optional[dict] = None,
    api_key: Optional[str] = API_KEY
) -> dict:
    """
    運行 Langflow flow 並取得回應

    :param message: 發送到 flow 的訊息
    :param endpoint: flow 的 ID 或端點名稱
    :param output_type: 輸出類型，預設為 'chat'
    :param input_type: 輸入類型，預設為 'chat'
    :param tweaks: 可選的 tweaks 用於自定義 flow
    :param api_key: 可選的 API 密鑰用於認證
    :return: flow 的 JSON 回應
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    
    if tweaks:
        payload["tweaks"] = tweaks
    if api_key:
        headers = {"x-api-key": api_key}
        
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# 創建一個 FastMCP 實例
app = FastMCP("Langflow 文檔問答系統")

@app.tool(
    "langflow_query", 
    description="向 Langflow 文檔問答系統提交查詢並獲取結果",
    param_descriptions={
        "query": "要檢索的查詢或問題",
        "tweaks": "可選的 tweaks 用於自定義 flow（高級使用者）"
    }
)
async def langflow_query(
    message: Message, 
    query: str, 
    tweaks: Optional[Dict[str, Any]] = None
) -> str:
    """
    向 Langflow 文檔問答系統提交查詢並獲取結果
    """
    try:
        # 使用預設或用戶提供的 tweaks
        actual_tweaks = tweaks or DEFAULT_TWEAKS
        
        # 呼叫 Langflow API
        response = run_flow(
            message=query,
            tweaks=actual_tweaks
        )
        
        # 檢查錯誤
        if "error" in response:
            return f"查詢處理過程中發生錯誤: {response['error']}"
        
        # 返回結果
        if "result" in response:
            return response["result"]
        else:
            return json.dumps(response, ensure_ascii=False, indent=2)
    
    except Exception as e:
        return f"處理您的請求時出現異常: {str(e)}"

@app.resource("langflow_status")
async def get_langflow_status() -> Dict[str, Any]:
    """
    取得 Langflow 服務狀態
    """
    try:
        # 檢查 Langflow 服務是否在線
        health_url = f"{BASE_API_URL}/api/v1/health"
        response = requests.get(health_url)
        
        if response.status_code == 200:
            status = "online"
        else:
            status = "offline"
            
        return {
            "status": status,
            "base_url": BASE_API_URL,
            "flow_id": FLOW_ID,
            "endpoint": ENDPOINT or FLOW_ID
        }
    except Exception:
        return {
            "status": "offline",
            "base_url": BASE_API_URL,
            "flow_id": FLOW_ID,
            "endpoint": ENDPOINT or FLOW_ID
        }

@app.prompt("langflow_query_template")
def query_template() -> str:
    return """
    我想要查詢關於以下主題的資訊:
    {{ query }}
    
    請提供詳細的回答和相關資訊來源。
    """

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    
    print(f"啟動 Langflow MCP 服務器於 http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port) 