# Langflow 文檔問答系統 MCP 工具

這是一個使用 Model Context Protocol (MCP) 開發的工具，用於與 Langflow 文檔問答系統進行交互。它允許您直接在 Claude 中查詢 Langflow 應用，並獲取回應。

## 功能

- 支援向 Langflow 文檔問答系統提交查詢
- 檢查 Langflow 服務的狀態
- 提供查詢提示模板

## 系統要求

### 必要條件

- **Python**: >= 3.10（由於 MCP 1.3.0 的要求）
- [MCP](https://github.com/modelcontextprotocol/python-sdk) >= 1.3.0
- Claude Desktop 應用（如需使用 Claude 集成功能）
- [uv](https://github.com/astral-sh/uv) 套件管理器（推薦）

### 相依套件

- requests >= 2.31.0
- python-dotenv >= 1.0.0
- typer >= 0.9.0
- uvicorn >= 0.22.0

## 安裝步驟

### 1. 確認 Python 版本

```bash
python --version  # 確保版本 >= 3.10
```

### 2. 使用 uv 創建虛擬環境

```bash
# 安裝 uv（如果尚未安裝）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 創建虛擬環境
uv venv .venv

# 激活虛擬環境
source .venv/bin/activate
```

### 3. 安裝依賴

```bash
# 使用 uv 安裝依賴
uv pip install -e .
```

### 4. 配置環境變數

創建 `.env` 文件並設置以下參數：

```ini
# Langflow API 設定
LANGFLOW_API_URL=http://127.0.0.1:7864  # 根據您的 Langflow 服務地址調整
LANGFLOW_FLOW_ID=your-flow-id-here      # 您的 Langflow flow ID
LANGFLOW_ENDPOINT=                       # 可選的端點名稱
LANGFLOW_API_KEY=                        # 如果需要 API 密鑰

# 服務器設定
PORT=8000                               # MCP 服務器運行的端口
```

## 使用方法

### 開發模式

在開發模式下運行並測試：

```bash
langflow-mcp dev
```

這將啟動：
- MCP 服務器在 http://localhost:8000
- MCP Inspector 在 http://localhost:5173

### 安裝到 Claude Desktop

確保所有依賴都正確安裝：

```bash
mcp install langflow_mcp_tool/server.py \
    --name "Langflow 文檔問答" \
    --with requests \
    --with python-dotenv \
    --with uvicorn \
    --with typer
```

### 直接運行服務器

```bash
langflow-mcp run
```

## 功能說明

### 1. 查詢功能 (Tool)

在 Claude 中使用：

```
使用 langflow_query 工具來查詢 "您的問題"
```

參數:
- `query`: 要檢索的查詢或問題
- `tweaks`: (可選) 用於自定義 flow 的參數

### 2. 狀態查詢 (Resource)

檢查服務狀態：

```
請檢查 langflow://status 資源
```

### 3. 查詢模板 (Prompt)

使用預定義模板：

```
使用 langflow_query_template 提示，我想查詢 "您的問題"
```

## 故障排除

### 常見問題

1. **Python 版本錯誤**
   - 確保使用 Python >= 3.10
   - 使用 `python --version` 檢查版本

2. **依賴問題**
   - 確保所有依賴都已正確安裝
   - 使用 `--with` 參數安裝必要依賴

3. **連接問題**
   - 確認 Langflow 服務運行中
   - 檢查 `.env` 中的 URL 設定

4. **Claude Desktop 整合問題**
   - 確保所有依賴都在安裝時指定
   - 檢查 Claude Desktop 的錯誤日誌

### 日誌和調試

- 使用 `--verbose` 參數運行 CLI 命令獲取詳細日誌
- 檢查 Claude Desktop 的錯誤日誌
- 使用 MCP Inspector 進行調試

## 專案結構

```
langflow-mcp-tool/
├── langflow_mcp_tool/           # 主要程式碼目錄
│   ├── __init__.py             # 套件初始化檔案
│   ├── cli.py                  # CLI 工具實現
│   └── server.py               # MCP 服務器實現
├── .env                        # 環境變數配置
├── .gitignore                  # Git 忽略檔案
├── pyproject.toml              # 專案配置和依賴管理
├── README.md                   # 專案文檔
├── requirements.txt            # 依賴套件列表
└── uv.lock                     # uv 套件管理器鎖定檔案
```

### 主要檔案說明

- `langflow_mcp_tool/server.py`: 實現了 MCP 服務器的核心功能，包括查詢處理和狀態檢查
- `langflow_mcp_tool/cli.py`: 提供命令行介面，用於啟動服務器和安裝工具
- `pyproject.toml`: 定義專案元數據、依賴和構建設定
- `.env`: 包含環境變數配置，如 API URL 和密鑰
- `requirements.txt`: 列出專案的 Python 套件依賴

## 開發指南

### 本地開發

1. 克隆倉庫
2. 創建虛擬環境
3. 安裝開發依賴：
   ```bash
   uv pip install -e ".[dev]"
   ```
4. 運行測試：
   ```bash
   pytest
   ```

### 代碼風格

- 使用 Black 進行代碼格式化
- 遵循 PEP 8 規範
- 添加適當的類型提示

## 授權

MIT

## 支持資源

- [MCP 文檔](https://github.com/modelcontextprotocol/python-sdk)
- [Langflow 文檔](https://docs.langflow.org)
- [問題追蹤](https://github.com/your-repo/issues)

---

如有任何問題或建議，請隨時提出 issue 或聯繫開發團隊。 