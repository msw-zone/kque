#!/usr/bin/env bash
set -e

# Move to project directory (where this script resides)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR/langgraph-sql-agent"
cd "$PROJECT_DIR"

# Step 1: Choose or create virtual environment
read -p "Enter path to virtual environment [venv]: " VENV_PATH
VENV_PATH=${VENV_PATH:-venv}
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment at $VENV_PATH"
    python3 -m venv "$VENV_PATH"
fi
source "$VENV_PATH/bin/activate"

# Step 2: Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Ensure .env and config.yaml exist
if [ ! -f ".env" ]; then
    cat > .env <<'EOV'
# Environment variables go here
# EXAMPLE_KEY=value
EOV
    echo "Created .env with placeholder values. Update it before running in production."
fi

if [ ! -f "config/config.yaml" ]; then
    cat > config/config.yaml <<'EOC'
embedding:
  provider: "openai"
  model_id: "text-embedding-ada-002"
  api_key: "YOUR_OPENAI_KEY"

llm:
  provider: "openai"
  model_id: "gpt-3.5-turbo"
  api_key: "YOUR_OPENAI_KEY"

vector_db:
  provider: "qdrant"
  host: "http://localhost:6333"
  collection: "documents"

sql:
  connection_string: "mysql+pymysql://user:password@localhost:3306/mydb"

history:
  db_uri: "sqlite:///chat_history.db"
EOC
    echo "Created config/config.yaml with placeholder values."
fi

# Step 4: Validate config values
python <<'PY'
import yaml, sys
from pathlib import Path
cfg_path = Path('config/config.yaml')
with cfg_path.open() as f:
    cfg = yaml.safe_load(f)

def check(path):
    val = cfg
    for key in path.split('.'):
        if not isinstance(val, dict) or key not in val:
            return False
        val = val[key]
    if val in (None, '', 'YOUR_OPENAI_KEY', 'mysql+pymysql://user:password@localhost:3306/mydb'):
        return False
    return True

required = [
    'embedding.model_id',
    'llm.model_id',
    'sql.connection_string',
    'history.db_uri',
    'vector_db.host'
]
missing = [p for p in required if not check(p)]
if missing:
    print(f"Missing required configuration: {', '.join(missing)}. Please update your config.yaml or .env file before continuing.")
    sys.exit(1)
PY

# Step 5: Initialize local databases (chat history)
python <<'PY'
from config.config import load_config
from chat.history_manager import HistoryManager
cfg = load_config()
HistoryManager(cfg['history']['db_uri'])
PY

# Step 6: Placeholder for migrations (none currently)

# Step 7: Launch application
echo "Choose how to run the application:" >&2
echo "1) Streamlit UI" >&2
echo "2) API server" >&2
echo "3) Both" >&2
read -p "Selection [1/2/3]: " CHOICE
if [ "$CHOICE" = "1" ]; then
    streamlit run ui/app.py
elif [ "$CHOICE" = "2" ]; then
    uvicorn api.app:app --reload
else
    uvicorn api.app:app --reload &
    API_PID=$!
    streamlit run ui/app.py
    kill $API_PID
fi
