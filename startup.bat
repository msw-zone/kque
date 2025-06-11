@echo off
setlocal enabledelayedexpansion

rem Step 1: Move to project directory (where this script resides)
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%langgraph-sql-agent"

rem Step 2: Choose or create virtual environment
set /p VENV_PATH=Enter path to virtual environment [venv]: 
if "%VENV_PATH%"=="" set VENV_PATH=venv
if not exist "%VENV_PATH%" (
    echo Creating virtual environment at %VENV_PATH%
    python -m venv "%VENV_PATH%"
)
call "%VENV_PATH%\Scripts\activate.bat"

rem Step 3: Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

rem Step 4: Ensure .env and config\config.yaml exist
if not exist ".env" (
    echo # Environment variables go here> .env
    echo # EXAMPLE_KEY=value>> .env
    echo Created .env with placeholder values. Update it before running in production.
)

if not exist "config\config.yaml" (
    if not exist config mkdir config
    (
    echo embedding:
    echo   provider: "openai"
    echo   model_id: "text-embedding-ada-002"
    echo   api_key: "YOUR_OPENAI_KEY"
    echo.
    echo llm:
    echo   provider: "openai"
    echo   model_id: "gpt-3.5-turbo"
    echo   api_key: "YOUR_OPENAI_KEY"
    echo.
    echo vector_db:
    echo   provider: "qdrant"
    echo   host: "http://localhost:6333"
    echo   collection: "documents"
    echo.
    echo sql:
    echo   connection_string: "mysql+pymysql://user:password@localhost:3306/mydb"
    echo.
    echo history:
    echo   db_uri: "sqlite:///chat_history.db"
    ) > config\config.yaml
    echo Created config\config.yaml with placeholder values.
)

rem Step 5: Validate config values
python - <<END
import yaml, sys
from pathlib import Path
cfg_path = Path('config/config.yaml')
cfg = yaml.safe_load(cfg_path.read_text())

def check(path):
    val = cfg
    for key in path.split('.'):
        if not isinstance(val, dict) or key not in val:
            return False
        val = val[key]
    if val in (None, '', 'YOUR_OPENAI_KEY', 'mysql+pymysql://user:password@localhost:3306/mydb'):
        return False
    return True

required = ['embedding.model_id','llm.model_id','sql.connection_string','history.db_uri','vector_db.host']
missing = [p for p in required if not check(p)]
if missing:
    print(f"Missing required configuration: {', '.join(missing)}. Please update your config.yaml or .env file before continuing.")
    sys.exit(1)
END
if errorlevel 1 exit /b

rem Step 6: Initialize local databases (chat history)
python - <<END
from config.config import load_config
from chat.history_manager import HistoryManager
cfg = load_config()
HistoryManager(cfg['history']['db_uri'])
END

rem Step 7: Launch application
echo Choose how to run the application:
echo 1^) Streamlit UI
echo 2^) API server
echo 3^) Both
set /p CHOICE=Selection [1/2/3]: 
if "%CHOICE%"=="1" (
    streamlit run ui/app.py
) else if "%CHOICE%"=="2" (
    uvicorn api.app:app --reload
) else (
    start "api" cmd /c "uvicorn api.app:app --reload"
    streamlit run ui/app.py
)

endlocal
