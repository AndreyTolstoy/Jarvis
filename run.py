import threading
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__name__)))
from Jarvis.main import Main
from Panel.server import run_server

if __name__ == "__main__":
 h1 = threading.Thread(target=run_server, daemon=True).start()
 run = Main()
 run.main()

