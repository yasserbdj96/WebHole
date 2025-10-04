#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   |                                                         |   #
# --+---------------------------------------------------------+-- #
#   |    Code by : yasserbdj96                                |   #
#   |    Email   : yasserbdj96@gmail.com                      |   #
#   |    GitHub  : github.com/yasserbdj96                     |   #
#   |    WebSite : yasserbdj96.github.io                      |   #
#   |    Sponsor : github.com/sponsors/yasserbdj96            |   #
#   |    BTC: bc1q2dks8w8uurca5xmfwv4jwl7upehyjjakr3xga9      |   #
#   |                                                         |   #
#   |    All posts with #yasserbdj96 All views are my own.    |   #
#   |                                                         |   #
# --+---------------------------------------------------------+-- #
#   |                                                         |   #
#START{
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import requests
from webhole.modules.tomd5 import tomd5
from webhole.modules.url_fix import url_fix
from webhole.modules.del_line_startswith import del_line_startwith
from webhole.__version__ import __version__,__source__
import json
import re
import curses
import ast
import os
import shutil

sys.stdout.reconfigure(encoding='utf-8')

class webhole:
    def __init__(self, url=None, user_key=None, Return=True, hole=None, nkey=None, pkgs=False):
        self.Return = Return
        self.messages = []  # To collect error messages
        self.fatal_error = False  # Indicates if initialization failed

        self.__version__ = "WebHole Version : "+__version__
        self.__package_version__ = None
        self.__source__="WebHole Source : "+__source__
        self.__package_source__ = None

        self.packages = "packages"
        self.config_file = "config.json"

        if hole is not None:
            self.package_name = None
            if nkey is not None:
                print(self.hole(pkg=hole,nkey=nkey))
            else:
                print(self.hole(pkg=hole))
            return 

        if pkgs:
            print(self.pkgs())
            return

        self.url = url_fix(url)
        self.user_key = tomd5(user_key)
        self.header = {'User-Agent': self.user_key}

        try:
            self.is_connect, self.connect_one = self.first_connect()
        except requests.exceptions.RequestException as e:
            msg = f"❌ Connection Error: Failed to establish connection to '{url}'. Verify network connectivity and server availability.\nDetails: {str(e)}"
            self._handle_error(msg)
            return
        except Exception as e:
            msg = f"❌ Initialization Error: Unexpected error occurred during setup.\nDetails: {str(e)}"
            self._handle_error(msg)
            return

        if not self.is_connect:
            msg = f"❌ Connection Failed: {self.connect_one}"
            self._handle_error(msg)
            return

        try:
            self.pakg_name = self.connect_one.split("#")[1]
            config_path = os.path.join(os.path.dirname(__file__), self.packages, self.pakg_name, self.config_file)

            try:
                with open(config_path, "r", encoding="utf-8") as file:
                    self.data = json.load(file)
            except FileNotFoundError:
                msg = f"❌ Configuration Error: Package configuration not found at '{config_path}'"
                self._handle_error(msg)
                return
            except json.JSONDecodeError:
                msg = f"❌ Configuration Error: Invalid JSON format in '{config_path}'"
                self._handle_error(msg)
                return

            if self.pakg_name != self.data["package-name"]:
                msg = f"❌ Validation Error: Package name mismatch. Expected '{self.data['package-name']}', received '{self.pakg_name}'"
                self._handle_error(msg)
                return

            command_zero_output = self.connect(self.data["command-0"])
            if self.data["command-0-output"] != command_zero_output:
                msg = f"❌ Validation Error: Initial command verification failed. Expected '{self.data['command-0-output']}', received '{command_zero_output}'"
                self._handle_error(msg)
                return

            self.connect_to_pkg = True
            self.package_name = self.data["package-name"]
            self.__package_version__ = self.package_name+" Version : "+self.data["values"]["package_version"]
            self.__package_source__ = self.package_name+" Source : "+self.data["values"]["package_source"]
            self.__author__ = self.data["values"]["author"]

            for key, value in self.data["auto-call"].items():
                setattr(self, key, self.connect(value))

        except IndexError:
            msg = "❌ Protocol Error: Invalid server response format"
            self._handle_error(msg)
            return
        except KeyError as e:
            msg = f"❌ Configuration Error: Missing required key in config - {str(e)}"
            self._handle_error(msg)
            return

    def _handle_error(self, message):
        """Handle errors based on Return flag."""
        if self.Return:
            self.messages.append(message)
            self.fatal_error = True
        else:
            print(message)
            sys.exit(1)

    def connect(self, command=None, cli=None, value=None, cf=True, **kwargs):
        try:
            self.command_function = False
            self.command_return = False
            self.command_function_path = ""
            self.command_function_fn = ""
            self.command_default = False
            self.formatted_command = ""

            if command and not cli and not value:
                commandx = command
            elif cli and not command and not value:
                start = self.data["start"]
                end = self.data["end"]
                command_file_path = os.path.join(
                    os.path.dirname(__file__),
                    self.packages,
                    self.pakg_name,
                    self.data["commands"][cli]["command-file"]
                )

                try:
                    with open(command_file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                except FileNotFoundError:
                    return f"❌ Command Error: CLI template '{cli}' not found"

                content = content[len(start):] if content.startswith(start) and start else content
                content = content[:-len(end)] if content.endswith(end) and end else content

                for key, val in kwargs.items():
                    try:
                        settingx = self.data["commands"][cli]["command-arguments"][key]
                        content = content.replace(settingx, val)
                    except KeyError:
                        return f"❌ Argument Error: Invalid parameter '{key}' for command '{cli}'"

                    try:
                        if cf:
                            self.command_function_path = self.data["commands"][cli]["command-function"]["path"].format(self=self)
                            self.command_function_fn = self.data["commands"][cli]["command-function"]["function"]
                            self.command_function = True
                    except KeyError:
                        pass

                    try:
                        self.command_return_var = self.data["commands"][cli]["command-return"]
                        self.command_return = True
                    except KeyError:
                        pass

                    try:
                        self.command_config = self.data["commands"][cli]["command-default"]
                        self.formatted_command = self.format_command_data(self.command_config, {"self": self})
                        self.command_default = True
                        content = self.replace_none_with_value(content, self.formatted_command)
                    except KeyError:
                        pass

                commandx = content
            elif value and not command and not cli:
                try:
                    return self.data["values"][value]["value-get"].format(self=self)
                except KeyError:
                    return f"❌ Value Error: Requested value '{value}' not found in configuration"
            else:
                return "❌ Parameter Error: Invalid parameter combination. Use either command, cli, or value"

            response = requests.post(self.url, headers=self.header, data={'command': commandx})
            if response.status_code != 200:
                return f"❌ Server Response Error: Received HTTP {response.status_code} - {response.reason}"

            response_text = del_line_startwith(response.text, "#")
            processed_response = self.styling_response(
                response_text,
                self.command_function,
                self.command_function_path,
                self.command_function_fn
            )

            if self.command_return:
                setattr(self, self.command_return_var, processed_response)

            return processed_response

        except requests.exceptions.RequestException as e:
            return f"❌ Network Error: Failed to execute command - {str(e)}"
        except Exception as e:
            return f"❌ Execution Error: {str(e)}"

    def first_connect(self):
        try:
            response = requests.post(self.url, headers=self.header, timeout=10)
            response.raise_for_status()

            first_line = response.text.splitlines()[0]
            if not first_line.startswith("#"):
                return [False, "❌ Protocol Error: Invalid server handshake format"]

            text = response.text.strip()
            if ':-:' not in text:
                return [False, "❌ Protocol Error: Invalid authentication structure"]

            pkg_name, key = text.split(':-:', 1)
            if key != self.user_key:
                return [False, "❌ Authentication Error: Invalid credentials provided"]

            return [True, pkg_name]

        except requests.exceptions.HTTPError as e:
            return [False, f"❌ HTTP Error: {str(e)}"]
        except requests.exceptions.ConnectionError:
            return [False, "❌ Connection Refused: Server unavailable or unreachable"]
        except requests.exceptions.Timeout:
            return [False, "❌ Timeout Error: Server did not respond in time"]
        except Exception as e:
            return [False, f"❌ Connection Error: {str(e)}"]

    def styling_response(self, response, command_function, command_function_path, command_function_fn):
        if not command_function:
            return response

        try:
            import importlib
            module_path = f"webhole.{command_function_path}"
            module = importlib.import_module(module_path)
            function_fn = getattr(module, command_function_fn)
            return function_fn(response)
        except ImportError:
            error_msg = f"❌ Module Error: Could not import processing module '{module_path}'"
            return error_msg if self.Return else print(error_msg) or response
        except AttributeError:
            error_msg = f"❌ Function Error: Processing function '{command_function_fn}' not found"
            return error_msg if self.Return else print(error_msg) or response

    def format_command_data(self, command_dict, context):
        try:
            formatted_data = {}
            for key, value in command_dict.items():
                if isinstance(value, str):
                    formatted_data[key] = value.format(**context)
                else:
                    formatted_data[key] = value
            return formatted_data
        except KeyError as e:
            raise ValueError(f"❌ Template Error: Missing context parameter '{e}'") from None

    def replace_none_with_value(self, text, replacements):
        pattern = r'(\$?\w+)\s*=\s*(None|null|nil)'
        def replacer(match):
            key = match.group(1).lstrip("$")
            return f"{match.group(1)} = {repr(replacements.get(key, match.group(2)))}"
        return re.sub(pattern, replacer, text)
    
    def info(self, *infos):
        return "\n".join(f"{getattr(self, info, 'Attribute not found')}" for info in infos)
    
    def help(self, pkg=None):
        commands = self.data["commands"]

        # Separate commands automatically
        core_cmds = {}
        pkg_cmds = {}

        for cmd, details in commands.items():
            desc = details.get("command-description", "No description")
            emoji = details.get("command-emoji", "👉")
            if cmd.startswith("-"):
                pkg_cmds[cmd] = [desc, emoji]
            else:
                core_cmds[cmd] = [desc, emoji]

        result = []
        result.append(f"📖 WebHole Command Reference — {self.package_name}")
        result.append("─" * 60)

        # Core Commands
        result.append(" Core Commands:")
        result.append("─" * 40)
        for cmd, desc in core_cmds.items():
            result.append(f"{desc[1]:<1}  {cmd:<8} : {desc[0]}")

        result.append("")
        result.append("📦 Package & Source Management:")
        result.append("─" * 40)
        for cmd, desc in pkg_cmds.items():
            result.append(f"{desc[1]:<1}  {cmd:<8} : {desc[0]}")

        result.append("")
        #result.append("─" * 60)
        #result.append(" Tip: Use `command --help` for more details")
        #result.append("─" * 60)

        return "\n".join(result)

    
    def hole(self,pkg=None,nkey=None):
        if pkg is None:
            pkg = self.package_name
        config_path = os.path.dirname(__file__)+"/"+self.packages+"/"+pkg+"/config.json"
        with open(config_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        hole = data.get("hole-code", "No hole code available")
        file_path = os.path.dirname(__file__)+"/"+self.packages+"/"+pkg+"/"+hole
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if nkey is not None:
                content = content.replace("__key__", nkey)
        return content
    

    def pkgs(self):
        results = []
        search_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packages")

        for root, dirs, files in os.walk(search_path):
            if "config.json" in files:
                file_path = os.path.join(root, "config.json")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        name = data.get("package-name")
                        version = data.get("values", {}).get("package_version")
                        if name:
                            results.append(f"{name} → {version}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

        return "\n".join(results)  # joins all lines in one string

    def editor(self, text=""):
        def _editor(stdscr):
            xxvo = True
            s = stdscr
            s.nodelay(0)
            curses.noecho()
            curses.raw()
            s.keypad(True)

            # Buffer initialization
            b = []
            R, C = s.getmaxyx()
            x, y, r, c = [0] * 4  # scrolling and cursor positions

            # Load string into buffer
            cont = text.split("\n")
            for rw in cont:
                b.append([ord(ch) for ch in rw])

            if not b:
                b.append([])

            result = None

            while xxvo:
                s.erase()

                # Scroll handling
                if r < y:
                    y = r
                if r >= y + R:
                    y = r - R + 1
                if c < x:
                    x = c
                if c >= x + C:
                    x = c - C + 1

                # Draw screen
                for rw in range(R):
                    brw = rw + y
                    if brw >= len(b):
                        break
                    line = b[brw]
                    for cl in range(C):
                        bcl = cl + x
                        if bcl >= len(line):
                            break
                        try:
                            s.addch(rw, cl, line[bcl])
                        except curses.error:
                            pass
                    s.clrtoeol()

                # Move cursor
                try:
                    curses.curs_set(1)
                except curses.error:
                    pass
                s.move(r - y, c - x)
                s.refresh()

                ch = s.getch()

                # Text input (ASCII only)
                if ch != ((ch) & 0x1f) and ch < 128:
                    b[r].insert(c, ch)
                    c += 1

                elif ch in (10, 13):  # Enter
                    l = b[r][c:]
                    b[r] = b[r][:c]
                    r += 1
                    c = 0
                    b.insert(r, l)

                elif ch in (8, 263):  # Backspace
                    if c:
                        c -= 1
                        del b[r][c]
                    elif r:
                        l = b[r][c:]
                        del b[r]
                        r -= 1
                        c = len(b[r])
                        b[r] += l

                elif ch == curses.KEY_LEFT:
                    if c > 0:
                        c -= 1
                    elif r > 0:
                        r -= 1
                        c = len(b[r])

                elif ch == curses.KEY_RIGHT:
                    if c < len(b[r]):
                        c += 1
                    elif r < len(b) - 1:
                        r += 1
                        c = 0

                elif ch == curses.KEY_UP and r > 0:
                    r -= 1

                elif ch == curses.KEY_DOWN and r < len(b) - 1:
                    r += 1

                # Keep cursor inside line bounds
                rw = b[r] if r < len(b) else None
                rwlen = len(rw) if rw is not None else 0
                if c > rwlen:
                    c = rwlen

                # Quit (Ctrl+Q)
                if ch == (ord("c") & 0x1f):
                    xxvo = False
                    result = None

                # Save (Ctrl+S)
                elif ch == (ord("s") & 0x1f):
                    cont = ""
                    for l in b:
                        cont += "".join([chr(c) for c in l]) + "\n"
                    result = cont.rstrip("\n")
                    xxvo = False

            # inside _editor return block
            if result is None:
                return ""   # instead of None
            return result

        # wrapper handles init/reset, no need for savetty/resetty
        return curses.wrapper(_editor)

    def config(self):
        config_path = os.path.join(
        os.path.dirname(__file__),
        self.packages,
        self.pakg_name,
        self.config_file
        )
        with open(config_path, "r", encoding="utf-8") as file:
            cmd_data  = json.load(file)  # Load JSON into a dictionary
            package_version = cmd_data["values"]["package_version"]
            logo = cmd_data["logo"]  # Get the "logo" key
            logo_color = cmd_data["logo_color"]
            cmd_data = cmd_data["commands"]  # Access the "commands" key
        return cmd_data,package_version,logo,logo_color,cmd_data

    def fn_listsort(self, response, separator='    |    '):
        try:
            response = response.strip()  # Remove leading/trailing spaces/newlines
            if not response.startswith("[") or not response.endswith("]"):
                print(f"❌ Invalid response: {response}")  # Debugging line
                raise ValueError(f"❌ Invalid response format: {response}")

            lslist = ast.literal_eval(response)
            
            if not isinstance(lslist, list):
                raise ValueError("❌ Parsed response is not a list.")
            
            lslist = [os.path.normpath(item) for item in lslist]  # Normalize paths

            # Get terminal size safely
            try:
                ts = shutil.get_terminal_size(fallback=(120, 50))
            except:
                ts = os.get_terminal_size(0)

            # Calculate column width based on longest item
            max_length = len(max(lslist, key=len, default=""))
            num_columns = max(1, ts.columns // (max_length + len(separator)))  # Avoid zero division
            
            # Format output
            formatted_list = ""
            for idx, key in enumerate(lslist):
                if (idx + 1) % num_columns:
                    formatted_list += key.ljust(max_length) + separator
                else:
                    formatted_list += key + '\n'
            
            return formatted_list.strip()
        
        except (SyntaxError, ValueError) as e:
            return f"❌ Error: Unable to parse response - {str(e)}{response}"


# Example usage
'''
if __name__ == "__main__":
    try:
        python_flask_connect = webhole(url="http://127.0.0.1:50", user_key="123456789")
        print(python_flask_connect.connect(cli="tree -f", path="."))
        print(python_flask_connect.connect(cli="ls", path="."))
        print(python_flask_connect.connect(cli="cd", path="."))
        print(python_flask_connect.connect(cli="cd", path=".."))


        php_connect = webhole(url="http://127.0.0.1:51/php.php", user_key="123456789")
        print(php_connect.connect(cli="tree", path=".."))
        print(php_connect.connect("echo 'this is python-flask:';"))
        print(php_connect.connect(cli="ls", path="."))
        print(php_connect.connect(cli="cd", path="."))
        print(php_connect.connect(cli="cd", path=".."))
    except Exception as e:
        print(f"Application Error: {str(e)}")
'''
#}END.