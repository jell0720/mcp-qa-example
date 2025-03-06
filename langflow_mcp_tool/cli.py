#!/usr/bin/env python
"""
Langflow MCP 工具的命令行介面
"""
import typer
import os
from dotenv import load_dotenv
from .server import app, main as server_main

# 創建一個 Typer 應用
cli = typer.Typer(
    name="langflow-mcp",
    help="用於 Langflow 文檔問答系統的 MCP 工具",
    add_completion=False,
)

@cli.command("install")
def install(
    name: str = typer.Option("Langflow 文檔問答", help="安裝在 Claude 桌面應用中的 MCP 工具名稱"),
    env_file: str = typer.Option(".env", help="環境變數檔案路徑"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="顯示詳細日誌")
):
    """
    安裝 MCP 工具到 Claude 桌面應用
    """
    import subprocess
    import sys

    # 確保環境變數已加載
    if os.path.exists(env_file):
        load_dotenv(env_file)
        typer.echo(f"已載入環境變數從 {env_file}")
    
    # 構建安裝命令
    cmd = [
        "mcp",
        "install",
        os.path.abspath("langflow_mcp_tool/server.py"),
        "--name",
        name
    ]
    
    # 添加環境變數
    if os.path.exists(env_file):
        cmd.extend(["-f", env_file])
    
    if verbose:
        typer.echo(f"執行命令: {' '.join(cmd)}")
    
    # 執行安裝命令
    try:
        subprocess.run(cmd, check=True)
        typer.echo(f"已成功安裝 '{name}' MCP 工具到 Claude 桌面應用")
    except subprocess.CalledProcessError as e:
        typer.echo(f"安裝失敗: {e}", err=True)
        sys.exit(1)

@cli.command("dev")
def dev(
    env_file: str = typer.Option(".env", help="環境變數檔案路徑"),
    port: int = typer.Option(8000, help="開發伺服器的埠號")
):
    """
    在開發模式下運行 MCP 工具
    """
    # 確保環境變數已加載
    if os.path.exists(env_file):
        load_dotenv(env_file)
        typer.echo(f"已載入環境變數從 {env_file}")
    
    # 設定端口
    os.environ["PORT"] = str(port)
    
    typer.echo(f"在開發模式下啟動 Langflow MCP 服務器於 http://localhost:{port}")
    
    # 使用 mcp dev 啟動開發伺服器
    import subprocess
    subprocess.run(["mcp", "dev", os.path.abspath("langflow_mcp_tool/server.py")])

@cli.command("run")
def run(
    env_file: str = typer.Option(".env", help="環境變數檔案路徑"),
    port: int = typer.Option(8000, help="伺服器的埠號")
):
    """
    直接運行 MCP 服務器
    """
    # 確保環境變數已加載
    if os.path.exists(env_file):
        load_dotenv(env_file)
        typer.echo(f"已載入環境變數從 {env_file}")
    
    # 設定端口
    os.environ["PORT"] = str(port)
    
    # 啟動伺服器
    server_main()

if __name__ == "__main__":
    cli() 