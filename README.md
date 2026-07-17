<div align="center">
  <img src="https://raw.githubusercontent.com/yasserbdj96/WebHole/main/Screenshots/logo.png" alt="hiphp by yasserbdj96" height="300">
</div>


# 🕳️ WebHole - Remote File System Explorer

WebHole is an advanced, open-source remote access and control tool designed for modern web environments. Unlike its predecessor HIPHP, which was limited to PHP, WebHole supports multiple server-side languages, including PHP, Flask (Python), Go (Golang), and Django, offering unmatched flexibility for developers and administrators.

By injecting a small piece of code—referred to as the WebHole Hole Code—into your project, WebHole enables secure communication over HTTP/HTTPS using POST or GET methods, typically over port 80 or 443. This allows authorized users to perform operations such as file management, script execution, configuration editing, and more, all remotely and in real-time.

Key features include:

 - ✅ Multi-Language Support: Seamlessly works with PHP, Python (Flask & Django), and Go.

 - 🔐 Password-Protected Access: Ensures only authorized users can control the server.

 - 🧱 Modular Architecture: Easily extend or adapt to new environments and frameworks.

 - 🌍 Remote File Execution & Editing: Modify, run, and manage files from any location.

 - 📦 Zero-Dependency Setup: No need for third-party software—just plug the hole code into your project.

Originally inspired by the limitations of HIPHP, WebHole is built for developers, security professionals, and system admins who need granular control over diverse web stacks—without relying on external tools or services.

Whether you're managing a single PHP site or a multi-framework infrastructure, WebHole empowers you with a unified, secure, and developer-friendly backdoor solution.

## 📦 Components
### Client-Side (main.py)
```bash
usage: main.py [-h] [--KEY KEY] [--URL URL] [--HOLE HOLE] [--NKEY NKEY] [--PKGS]

Webhole Command-Line Interface: Configure keys, URLs, and manage packages.

options:
  -h, --help                   Show this help message and exit.
  --KEY KEY, --key KEY         Authentication key used for secure operations. Can be provided via the KEY environment variable.
  --URL URL, --url URL         Target URL for the operation. Can be provided via the URL environment variable.
  --HOLE HOLE, --hole HOLE     Hole identifier or reference. Can be provided via the HOLE environment variable.
  --NKEY NKEY, --nkey NKEY     New authentication key for updating or replacing an existing key. Can be provided via the NKEY environment variable.       
  --PKGS, --pkgs               Display all installed packages in Webhole. Can be enabled via the PKGS environment variable.
```

### Server-Side (hole.[py,php,go...])
```bash
# Flask server configuration
endpoint: "/"
authentication:
  method: "User-Agent header"
  key: "__key__"  # Replace with your secret key
execution:
  commands: 
    - "ls"
    - "cd"
    - "tree"
    - "cat"
```

## ⚙️ Setup & Usage
1. Setup
```bash
# Clone the WebHole repository
git clone https://github.com/yasserbdj96/WebHole.git

# Navigate to the project directory
cd WebHole

# Install the required dependencies
pip install -r requirements.txt
```

2. Client Connection
```bash
# Connect to an existing WebHole instance
python main.py --URL="http://server-ip:port" --KEY="your_secret_key"

# Display installed packages on the WebHole
python main.py --pkgs
# Example output:
# go-http-server   → 0.0.1-beta
# php              → 0.0.2-beta
# python-django    → 0.0.0-beta
# python-flask     → 0.0.2-beta

# Create a new WebHole code for a specific platform (Flask, Django, Go, PHP, etc.)

# Without a password (you can set one manually later):
python main.py --hole="package_name"

# With a specified password (encrypted automatically):
python main.py --hole="package_name" --nkey="your_new_key"
```

## 🌐 Supported Operations
| Command        | Description                                                   | Example        | *go-http-server  | *php        | *python-django | *python-flask |
| :------------: | :-----------------------------------------------------------: | :------------: | :-------------: | :--------: | :-----------: | :----------: |
| [COMMAND]      | Put your command                                              | [COMMAND]      | ✅              |  ✅        | ✅             | ✅        |
| ls             | List directory contents                                       | ls             | ✅              |  ✅        | ✅             | ✅        |
| cd             | Change directory                                              | cd [PATH]      | ❌              |  ✅        | ✅             | ✅        |
| tree           | Show directory tree                                           | tree           | ❌              |  ✅        | ✅             | ✅        |
| tree -f        | Display directory structure in a tree format with full paths  | tree -f        | ❌              |  ✅        | ✅             | ✅        |
| cat            | Display file content                                          | cat [file]     | ❌              |  ✅        | ✅             | ✅        |
| edit           | Open and edit a file                                          | edit [file]    | ❌              |  ❌        | ❌             | ✅        |
| up             | Upload a file                                                 | up [file]      | ❌              |  ❌        | ❌             | ✅        |
| hole           | Display HOLE Code                                             | hole           | ✅              |  ✅        | ✅             | ✅        |
| -v             | Show version information                                      | -v             | ✅              |  ✅        | ✅             | ✅        |
| -h             | Show help	                                                   | -h             | ✅              |  ✅        | ✅             | ✅        |
| exit           | Exit the shell	                                               | exit           | ✅              |  ✅        | ✅             | ✅        |

## 🔒 Security Features
- MD5-hashed authentication keys
- Secure command execution sandbox
- Encrypted communication
- Restricted command whitelisting

## 📂 Directory Structure
```bash
webhole/
│   CHANGELOG
│   config.json
│   logo.png
│   main.py
│   README.md
│   requirements.txt
│   version.txt
├───Tasks
│       django_server.py
│       flask_server.py
│       go_server.go
│       php_server.php
│       servers_config.json
│       server_launcher.py
└───webhole
    │   messages.json
    │   __init__.py
    │   __version__.py
    │
    ├───modules
    │       del_line_startswith.py
    │       tomd5.py
    │       url_fix.py
    │
    └───packages
        ├───go-http-server
        │       config.json
        │       hole.go
        │       ls.go
        │
        ├───php
        │       cat.php
        │       cd.php
        │       config.json
        │       hole.php
        │       ls.php
        │       tree.php
        │       tree_f.php
        │
        ├───python-django
        │       cat.py
        │       cd.py
        │       config.json
        │       hole.py
        │       ls.py
        │       tree.py
        │       tree_f.py
        │
        ├───python-flask
        │       cat.py
        │       cd.py
        │       config.json
        │       hole.py
        │       ls.py
        │       tree.py
        │       tree_f.py
        │
        └───__functions__
                fn_listsort.py
```

## 💻 Example Session
```bash
┌──(python-flask@example.com)──[/home/user]
└─WEBHOLE> ls
📄 CHANGELOG           |    📄 config.json         |    📄 logo.png            
📄 main.py             |    📄 README.md           |    📄 requirements.txt
📁 Tasks               |    📄 version.txt         |    📁 versions            
📁 webhole
┌──(python-flask@example.com)──[/home/user]
└─WEBHOLE> cd Tasks
┌──(python-flask@example.com)──[/home/user/Tasks]
└─WEBHOLE> tree
.
├─── django_server.py
├─── flask_server.py
├─── go_server.go
├─── php_server.php
├─── server_launcher.py
└─── servers_config.json
┌──(python-flask@example.com)──[/home/user/Tasks]
└─WEBHOLE> tree -f
rrw-rw-rw- Jun 18 14:54     1.54 KB django_server.py
rrw-rw-rw- Jun 18 14:52     1.30 KB flask_server.py
rrw-rw-rw- Jun 18 15:20     2.30 KB go_server.go
rrw-rw-rw- Apr 07 21:22   655 bytes php_server.php
rrw-rw-rw- Jun 18 15:03   528 bytes servers_config.json
rrw-rw-rw- Jun 18 14:54     3.00 KB server_launcher.py
┌──(python-flask@example.com)──[/home/user/Tasks]
└─WEBHOLE> cat servers_config.json
{
  "flask": {
    "enabled": true,
    "host": "127.0.0.1",
    "port": 81,
    "entry": "flask_server.py"
  },
  "php": {
    "enabled": true,
    "host": "127.0.0.1",
    "port": 82,
    "php_path": "C:\\xampp\\php\\php.exe",
    "root": ".",
    "entry": "php_server.php"
  },
  "go": {
    "enabled": true,
    "entry": "go_server.go",
    "host": "127.0.0.1",
    "port": 83
  },
  "django": {
    "enabled": true,
    "host": "127.0.0.1",
    "port": 84,
    "entry": "django_server.py"
  }
}
```

> ## Screenshots:

<p align="center">
  <a href="https://raw.githubusercontent.com/yasserbdj96/WebHole/main/Screenshots/Screenshot_01.png" target="_blank">
    <img src="https://raw.githubusercontent.com/yasserbdj96/WebHole/main/Screenshots/Screenshot_01.png" alt="Preview" width="300">
  </a>
  <a href="https://raw.githubusercontent.com/yasserbdj96/WebHole/main/Screenshots/Screenshot_02.png" target="_blank">
    <img src="https://raw.githubusercontent.com/yasserbdj96/WebHole/main/Screenshots/Screenshot_02.png" alt="Preview" width="300">
  </a>
</p>

> ## 🚨 Warning
> Always use in trusted environments - command execution capabilities pose security risks if misconfigured.


<br>
<br>

<p align="center">
  <samp>
    <a href="https://yasserbdj96.github.io/">Website</a> .
    <a href="https://github.com/yasserbdj96">Github</a> .
    <a href="https://instagram.com/yasserbdj96">Instagram</a> .
    <a href="https://www.youtube.com/@yasserbdj96">youtube</a> .
    <a href="https://pypi.org/user/yasserbdj96">pypi</a> .
    <a href="https://hub.docker.com/u/yasserbdj96">docker</a> .
    <a href="https://gitter.im/yasserbdj96/yasserbdj96">gitter</a> .
    <a href="mailto:yasser.bdj96@gmail.com">e-mail</a> .
    <a href="https://github.com/sponsors/yasserbdj96">sponsor</a>
  </samp>
</p>
