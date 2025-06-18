import subprocess
import time
import json
import os
import sys
from typing import Dict, List

CONFIG_FILE = "servers_config.json"

def load_config(path: str) -> Dict:
    """Load JSON configuration file."""
    if not os.path.isfile(path):
        print(f"[ERROR] Configuration file not found: {path}")
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def start_flask_app(config: Dict) -> subprocess.Popen:
    print(f"[INFO] Launching Flask server on http://{config['host']}:{config['port']}")
    return subprocess.Popen([
        "python", config["entry"],
        config["host"], str(config["port"])
    ])

def start_django_app(config: Dict) -> subprocess.Popen:
    print(f"[INFO] Launching Django server on http://{config['host']}:{config['port']}")
    return subprocess.Popen([
        "python", config["entry"], "runserver",
        f"{config['host']}:{config['port']}"
    ])


def start_php_server(config: Dict) -> subprocess.Popen:
    root_path = os.path.abspath(config["root"])
    entry = config.get("entry", "index.php")
    print(f"[INFO] Launching PHP server on http://{config['host']}:{config['port']} (Root: {root_path})")
    return subprocess.Popen([
        config["php_path"],
        "-S", f"{config['host']}:{config['port']}",
        "-t", root_path,
        os.path.join(root_path, entry)
    ])


def start_go_app(config: Dict) -> subprocess.Popen:
    print(f"[INFO] Launching Go server on http://{config['host']}:{config['port']}")
    return subprocess.Popen([
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
                print(f"[ERROR] Failed to start {name} server: {e}")
    return processes

def main():
    config = load_config(CONFIG_FILE)
    processes = []

    try:
        processes = start_enabled_servers(config)
        print("[INFO] All enabled servers are now running. Press Ctrl+C to stop.")

        for proc in processes:
            proc.wait()
    except KeyboardInterrupt:
        print("\n[INFO] Stopping servers...")
        for proc in processes:
            proc.terminate()
    except Exception as e:
        print(f"[FATAL] Unexpected error: {e}")
        for proc in processes:
            proc.terminate()

if __name__ == "__main__":
    main()
