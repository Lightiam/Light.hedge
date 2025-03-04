import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import from src
sys.path.append(str(Path(__file__).parent))

# Set environment variable for Streamlit
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

if __name__ == "__main__":
    import streamlit.web.cli as stcli
    import sys
    
    sys.argv = ["streamlit", "run", "src/web/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
    sys.exit(stcli.main())
