# Langflow 文檔問答系統 MCP 工具

這是一個使用 Model Context Protocol (MCP) 開發的工具，用於與 Langflow 文檔問答系統進行交互。它允許您直接在 Claude 中查詢 Langflow 應用，並獲取回應。

## 功能

- 支援向 Langflow 文檔問答系統提交查詢
- 檢查 Langflow 服務的狀態
- 提供查詢提示模板

## 安裝

### 前提條件

- Python 3.8+
- [MCP](https://github.com/modelcontextprotocol/python-sdk) 已安裝
- Claude Desktop 應用已安裝 (如果需要使用 Claude 集成功能)

### 使用 pip 安裝

```bash
pip install .
```

## 配置

在使用前，您需要設定相關環境變數。您可以創建一個 `.env` 文件，包含以下設定：

```
# Langflow API 設定
LANGFLOW_API_URL=http://127.0.0.1:7864
LANGFLOW_FLOW_ID=your-flow-id-here
LANGFLOW_ENDPOINT=
LANGFLOW_API_KEY=

# 服務器設定
PORT=8000
```

## 使用方法

### 安裝到 Claude Desktop

```bash
langflow-mcp install --name "Langflow 文檔問答" --env-file .env
```

### 開發模式運行

```bash
langflow-mcp dev --port 8000
```

### 直接運行服務器

```bash
langflow-mcp run --port 8000
```

## MCP 功能

### 工具 (Tools)

- `langflow_query`: 向 Langflow 文檔問答系統提交查詢並獲取結果

### 資源 (Resources)

- `langflow_status`: 取得 Langflow 服務狀態

### 提示模板 (Prompts)

- `langflow_query_template`: 提供一個用於查詢 Langflow 的提示模板

## 開發

要進行開發，請遵循以下步驟：

1. 克隆此倉庫
2. 使用 uv 創建虛擬環境並安裝依賴：
   ```bash
   uv venv .venv
   source .venv/bin/activate
   uv add "mcp[cli]" requests python-dotenv typer uvicorn
   ```
3. 安裝可編輯模式的包：
   ```bash
   pip install -e .
   ```
4. 運行開發服務器：
   ```bash
   langflow-mcp dev
   ```

## 授權

MIT 