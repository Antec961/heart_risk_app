import os
import sys
import subprocess
import time
import webbrowser
import threading
import urllib.request

HOST = "127.0.0.1"
PORT = 8000
BASE_URL = f"http://{HOST}:{PORT}"
HEALTH_URL = f"{BASE_URL}/health"
VENV_DIR = "app_venv"


def is_app_running(timeout=1):
    """Проверяем, что именно НАШ FastAPI отвечает"""
    try:
        with urllib.request.urlopen(HEALTH_URL, timeout=timeout) as response:
            return response.status == 200
    except:
        return False


def run(cmd):
    subprocess.check_call(cmd, shell=True)


def main():
    # 🔍 Проверка приложения
    if is_app_running():
        print(f"FastAPI already running at {BASE_URL}")
        webbrowser.open(BASE_URL)
        return

    # 1️⃣ Создание venv
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        run(f"{sys.executable} -m venv {VENV_DIR}")

    # 2️⃣ Активация venv
    if os.name == "nt":
        activate = f"{VENV_DIR}\\Scripts\\activate"
    else:
        activate = f"source {VENV_DIR}/bin/activate"

    # 3️⃣ Установка зависимостей
    print("Installing dependencies...")
    run(f"{activate} && pip install --upgrade pip")
    run(f"{activate} && pip install -r requirements.txt")

    # 4️⃣ Открытие браузера ПОСЛЕ старта сервера
    def open_browser_when_ready():
        for _ in range(10):  # ждём до 10 секунд
            time.sleep(1)
            if is_app_running():
                webbrowser.open(BASE_URL)
                return

    threading.Thread(target=open_browser_when_ready, daemon=True).start()

    # 5️⃣ Запуск FastAPI
    print("Starting FastAPI server...")
    run(
        f"{activate} && "
        f"uvicorn app:app --host {HOST} --port {PORT} --reload"
    )


if __name__ == "__main__":
    main()
