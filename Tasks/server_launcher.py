import subprocess
import time
import json
import os
import sys
from typing import Dict, List
from hexor import *

# colors with hexor:
color = hexor(True, "hex")

# used hex colors in this program:
c_red = "#ea4335"       # red
c_white_red = "#f3938b" # white-red
c_blue = "#4285f4"      # blue
c_yellow = "#fbbc05"    # yellow
c_green = "#34a853"     # green
c_white = "#ffffff"     # white

# pre-colored tags
ERROR = color.c('[ERROR]', c_red)
FATAL = color.c('[FATAL]', c_red)
INFO = color.c('[INFO]', c_green)

CONFIG_FILE = "servers_config.json"

def load_config(path: str) -> Dict:
    """Load JSON configuration file."""
    if not os.path.isfile(path):
        print(f"{ERROR} {color.c('Configuration file not found:', c_white)} {color.c(path, c_yellow)}")
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# helper: silence subprocess
def silent_popen(cmd: list, cwd=None) -> subprocess.Popen:
    return subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.DEVNULL,   # suppress output
        stderr=subprocess.DEVNULL    # suppress errors
    )

def start_flask_app(config: Dict) -> subprocess.Popen:
    url = f"http://{config['host']}:{config['port']}"
    print(f"{INFO} {color.c('Launching Flask server on', c_white)} {color.c(url, c_blue)}")
    return silent_popen([
        "python", config["entry"],
        config["host"], str(config["port"])
    ])

def start_django_app(config: Dict) -> subprocess.Popen:
    url = f"http://{config['host']}:{config['port']}"
    print(f"{INFO} {color.c('Launching Django server on', c_white)} {color.c(url, c_blue)}")
    return silent_popen([
        "python", config["entry"], "runserver",
        f"{config['host']}:{config['port']}"
    ])

def start_php_server(config: Dict) -> subprocess.Popen:
    root_path = os.path.abspath(config["root"])
    entry = config.get("entry", "index.php")
    url = f"http://{config['host']}:{config['port']}"
    print(f"{INFO} {color.c('Launching PHP server on', c_white)} {color.c(url, c_blue)} {color.c('(Root:', c_white)} {color.c(root_path, c_yellow)}{color.c(')', c_white)}")
    return silent_popen([
        config["php_path"],
        "-S", f"{config['host']}:{config['port']}",
        "-t", root_path,
        os.path.join(root_path, entry)
    ], cwd=root_path)

def start_go_app(config: Dict) -> subprocess.Popen:
    url = f"http://{config['host']}:{config['port']}"
    print(f"{INFO} {color.c('Launching Go server on', c_white)} {color.c(url, c_blue)}")
    return silent_popen([
        "go", "run", config["entry"],
        "--host", config["host"],
        "--port", str(config["port"])
    ])


def start_enabled_servers(config: Dict) -> List[subprocess.Popen]:
    """Start all enabled servers from config."""
    processes = []

    server_launchers = {
        "flask": start_flask_app,
        "php": start_php_server,
        "go": start_go_app,
        "django": start_django_app
    }

    for name, launcher in server_launchers.items():
        server_config = config.get(name, {})
        if server_config.get("enabled", False):
            try:
                proc = launcher(server_config)
                processes.append(proc)
                time.sleep(1)  # Small delay to avoid port clashes
            except Exception as e:
                print(f"{ERROR} {color.c('Failed to start', c_white)} {color.c(name, c_yellow)} {color.c('server:', c_white)} {color.c(str(e), c_red)}")
    return processes

def main():
    config = load_config(CONFIG_FILE)
    processes = []

    try:
        processes = start_enabled_servers(config)
        print(f"{INFO} {color.c('All enabled servers are now running.', c_green)} {color.c('Press Ctrl+C to stop.', c_white)}")

        for proc in processes:
            proc.wait()
    except KeyboardInterrupt:
        print(f"\n{INFO} {color.c('Stopping servers...', c_yellow)}")
        for proc in processes:
            proc.terminate()
    except Exception as e:
        print(f"{FATAL} {color.c('Unexpected error:', c_white)} {color.c(str(e), c_red)}")
        for proc in processes:
            proc.terminate()

if __name__ == "__main__":
    main()
