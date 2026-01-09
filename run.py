import threading
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__name__)))
from Jarvis.main import Main, listen
from Panel.server import run_server
from title import title
import colorama
import time
print(colorama.Fore.RED + title + colorama.Style.RESET_ALL)

if __name__ == "__main__":
 sys.stdout = None
 threading.Thread(target=run_server, daemon=True).start()
 threading.Thread(target=listen, daemon=True).start()
 time.sleep(0.001) #*Задержка, чтобы фласк полностью запустил локальный сервер и при этом все логи перенаправляются в никуда
 sys.stdout = sys.__stdout__
 Main().main()
 

