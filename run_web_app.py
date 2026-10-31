"""
Runner Script for Campus Lost and Found Web Application
Author: Arahat Gaikwad (24BYB0182) - VIT Vellore
"""

import os
import sys
import webbrowser
import threading
import time

app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app")
sys.path.insert(0, app_dir)

import web_app

def open_browser():
    time.sleep(1.2)
    webbrowser.open("http://localhost:5000")

if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    web_app.run_server(5000)
