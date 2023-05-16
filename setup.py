import subprocess
import sys
import os


def check_pyinstaller_installed():
    try:
        import PyInstaller
        return True
    except ImportError:
        return False


def install_pyinstaller():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])


def execute_commands():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    subprocess.check_call(["pyinstaller", "--onefile", "--noconsole", "youtube_downloader.py"])

    dist_dir = os.path.join(script_dir, "dist")
    os.chdir(dist_dir)

    subprocess.check_call(["youtube_downloader.exe"])


if __name__ == "__main__":
    if not check_pyinstaller_installed():
        print("Установка PyInstaller...")
        install_pyinstaller()
        print("PyInstaller успешно установлен!")

    print("Выполнение команд...")
    execute_commands()
