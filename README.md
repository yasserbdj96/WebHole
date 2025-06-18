<!-- Project Header -->
<div align="center">
  <img src="https://raw.githubusercontent.com/yasserbdj96/WebHole/main/Screenshots/logo.png" alt="hiphp by yasserbdj96" height="300">
</div>


# 🕳️ WebHole - Remote File System Explorer

WebHole is a secure client-server tool for exploring remote file systems through a web interface, featuring encrypted communication and cross-platform compatibility.

## 📦 Components
### Client-Side (main.py)
```bash
usage: main.py [-h] [--KEY KEY] [--URL URL]

options:
  -h, --help     show this help message
  --KEY, --key   Authentication key
  --URL, --url   Server endpoint URL
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
1. Server Setup
```bash
# Install dependencies
pip install flask

# Start server (modify key in hole.[py,php,go...] first)
start hole.[py,php,go...]
```

2. Client Connection
```bash
# Linux/macOS
export KEY="your_secret_key"
export URL="http://server-ip:port"
python main.py

# Windows
set KEY="your_secret_key"
set URL="http://server-ip:port"
python main.py
```

## 🌐 Supported Operations
| Command        | Description                                                   | Example        | go-http-server | php        | python-django | python-flask |
| :------------: | :-----------------------------------------------------------: | :------------: | :------------: | :--------: | :-----------: | :----------: |
| [COMMAND]      | Put your command                                              | [COMMAND]      | ✅              |  ✅        | ✅             | ✅           |
| ls             | List directory contents                                       | ls             | ✅              |  ✅        | ✅             | ✅           |
| cd             | Change directory                                              | cd [PATH]      | ❌              |  ✅        | ✅             | ✅           |
| tree           | Show directory tree                                           | tree           | ❌              |  ✅        | ✅             | ✅           |
| tree -f        | Display directory structure in a tree format with full paths  | tree -f        | ❌              |  ✅        | ✅             | ✅           |
| cat            | Display file content                                          | cat [file]     | ❌              |  ✅        | ✅             | ✅           |
| -v             | Show version information                                      | -v             | ✅              |  ✅        | ✅             | ✅           |
| -h             | Show help	                                                 | -h             | ✅              |  ✅        | ✅             | ✅           |
| exit           | Exit the shell	                                             | exit           | ✅              |  ✅        | ✅             | ✅           |

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
📄 django_server.py       |    📄 flask_server.py        |    📄 go_server.go           |    📄 php_server.php         |    📄 servers_config.json
📄 server_launcher.py     
┌──(python-flask@example.com)──[/home/user]
└─WEBHOLE> cd Documents
┌──(python-flask@example.com)──[/home/user/Documents]
└─WEBHOLE> tree
.
├─── django_server.py
├─── flask_server.py
├─── go_server.go
├─── php_server.php
├─── server_launcher.py
└─── servers_config.json
┌──(python-flask@example.com)──[/home/user/Documents]
└─WEBHOLE> tree -f
rrw-rw-rw- Jun 18 14:54     1.54 KB django_server.py
rrw-rw-rw- Jun 18 14:52     1.30 KB flask_server.py
rrw-rw-rw- Jun 18 15:20     2.30 KB go_server.go
rrw-rw-rw- Apr 07 21:22   655 bytes php_server.php
rrw-rw-rw- Jun 18 15:03   528 bytes servers_config.json
rrw-rw-rw- Jun 18 14:54     3.00 KB server_launcher.py
```

> ## Screenshots:

<p align="center">
  <a href="https://github.com/yasserbdj96/WebHole/blob/db723c36a6b802b6937e5cc755f6cc0da5ba9a81/Screenshots/Screenshot_01.png" target="_blank">
    <img src="https://github.com/yasserbdj96/WebHole/blob/db723c36a6b802b6937e5cc755f6cc0da5ba9a81/Screenshots/Screenshot_01.png" alt="Preview" width="300">
  </a>
</p>

> ## 🚨 Warning
> Always use in trusted environments - command execution capabilities pose security risks if misconfigured.
