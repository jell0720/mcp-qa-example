# MCP 概述 (模型上下文協議概述)

**模型上下文協議 (Model Context Protocol, MCP)** 是一種開放協議，用於標準化將應用程式的「上下文」提供給大型語言模型 (LLM)。

MCP 可類比為 AI 應用的 *USB-C 埠* 或 *HTTP 協議*，提供統一的方式連接各種裝置或應用程式。透過 MCP，開發者可以將資料庫、檔案、網路服務等 **外部資源作為上下文** 提供給 LLM，充當 AI 模型與資料源之間的橋樑。

**MCP 的優勢**：
- **標準化上下文管理**：MCP 提供統一的接口，便於不同應用存取。
- **與模型供應商無關**：適用於各種 LLM 平台，便於切換。
- **安全機制**：提供權限管理，確保上下文傳輸安全。

---

# MCP 在 AutoGen 中的應用

Microsoft AutoGen 自 v0.4 版本起支援 MCP，使得 AutoGen 智能體 (AI 代理，AI Agent) 可以透過 MCP 使用外部工具與資料源。

**AutoGen 透過 MCP 進行上下文管理的方式：**
1. **SSE 適配器 (`SseMcpToolAdapter`)**：透過 HTTP SSE 連接 MCP 服務。
2. **STDIO 適配器 (`StdioMcpToolAdapter`)**：透過標準輸入/輸出溝通 MCP 工具。
3. **工具自動發現 (`mcp_server_tools()`)**：自動獲取 MCP 伺服器上的可用工具。

AutoGen 可以**動態發現並使用外部工具**，將 MCP 工具的功能視作 LLM 可用的「函數」，增強對話能力與上下文擴充。

---

# 技術細節：上下文管理實作

**AutoGen 透過 MCP 管理上下文的步驟：**
1. **智能體判斷需求**：LLM 判斷需要某項外部資訊時，發起工具請求。
2. **AutoGen 代理攔截請求**：使用 MCP 適配器調用工具，獲取結果。
3. **封裝回應並更新上下文**：透過 `ToolCallSummaryMessage` 插入對話歷史，確保連貫性。
4. **反饋總結 (`reflect_on_tool_use=True`)**：若輸出過長，先摘要後納入上下文。

---

# 程式碼範例：AutoGen 使用 MCP 工具

以下範例示範如何使用 MCP 工具 `fetch`，讓 AI 代理讀取指定 URL 並摘要內容。

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools

async def main():
    fetch_server = StdioServerParams(command="uvx", args=["mcp-server-fetch"])
    tools = await mcp_server_tools(fetch_server)
    model_client = OpenAIChatCompletionClient(model="gpt-4o")
    agent = AssistantAgent(
        name="assistant", 
        model_client=model_client, 
        tools=tools, 
        system_message="你是一個網頁內容抓取助手。",
        reflect_on_tool_use=True
    )
    result = await agent.run(task="Summarize the content of https://en.wikipedia.org/wiki/Seattle")
    print(result.messages[-1].content)

asyncio.run(main())
```

---

# MCP 的優勢與限制

### **優勢**
✅ **標準化工具整合**：可即插即用 MCP 工具，擴展 AI 代理能力。
✅ **動態發現與調用**：無需手動配置，AI 代理自動識別可用工具。
✅ **跨平台、跨語言兼容**：適用於不同 AI 框架與開發語言。

### **限制**
⚠ **部署與維護成本高**：MCP 需要獨立工具伺服器，增加運維負擔。
⚠ **通訊延遲**：工具透過 HTTP/STDIO 交互，可能影響即時性。
⚠ **模型上下文限制**：過多輸出仍需摘要，避免超出 LLM 上下文長度。
⚠ **安全風險**：外部工具可能產生不可靠資訊，需控管存取權限。

---

# AutoGen 的上下文管理策略

### 1️⃣ **緩衝記憶 (Buffered Context)**
- 透過 `BufferedChatCompletionContext` 只保留最近 N 條對話，避免上下文過長。

### 2️⃣ **內容摘要與取舍**
- 使用 `reflect_on_tool_use=True` 讓 LLM 自行摘要 MCP 工具的輸出，減少冗長資訊。

### 3️⃣ **向量資料庫與檢索 (RAG)**
- AutoGen 可結合 LlamaIndex 等工具，從長期記憶檢索相關資訊。

### 4️⃣ **人工監督 (Human-in-the-loop)**
- 允許人工審查與修正對話，確保上下文完整與準確。

---

**結論**：AutoGen 透過 MCP 工具實現外部資料擴充，並結合多種上下文管理策略，確保對話的準確性、連貫性與可擴展性。

