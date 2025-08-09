#START{
from webhole import webhole
from webhole.__version__ import __version__,__source__,__author__,__website__
import argparse
import os
from hexor import *
import json
import sys
import hashlib

# Create an ArgumentParser object
parser = argparse.ArgumentParser(
    description="Webhole Command-Line Interface: Configure keys, URLs, and manage packages."
)

#
parser.add_argument('--KEY', '--key', dest='KEY', type=str, default=os.getenv('KEY', None), help='Authentication key used for secure operations. Can be provided via the KEY environment variable.')
parser.add_argument('--URL', '--url', dest='URL', type=str, default=os.getenv('URL', None), help='Target URL for the operation. Can be provided via the URL environment variable.')
parser.add_argument('--HOLE', '--hole', dest='HOLE', type=str, default=os.getenv('HOLE', None), help='Hole identifier or reference. Can be provided via the HOLE environment variable.')
parser.add_argument('--NKEY', '--nkey', dest='NKEY', type=str, default=os.getenv('NKEY', None), help='New authentication key for updating or replacing an existing key. Can be provided via the NKEY environment variable.')
parser.add_argument('--PKGS', '--pkgs',dest='PKGS',action='store_true',default=bool(os.getenv('PKGS', False)),help='Display all installed packages in Webhole. Can be enabled via the PKGS environment variable.')

# Parse the command-line arguments
args = parser.parse_args()

# Access the variables by their names
KEY = str(args.KEY)
URL = str(args.URL)
HOLE = str(args.HOLE)
if args.NKEY!=None:
    NKEY = md5_hash = hashlib.md5(str(args.NKEY).encode()).hexdigest()
else:
    NKEY = args.NKEY

# colors with hexor:
color=hexor(True,"hex")
#used hex colors in this programm:
c_red="#ea4335"# red
c_white_red="#f3938b"# white-red
c_blue="#4285f4"# blue
c_yellow="#fbbc05"# yellow
c_green="#34a853"# green
c_white="#ffffff"# white

def match_command(user_input, commands_json):
    parts = user_input.strip().split()
    base_command = []
    remaining_args = []

    for i in range(len(parts), 0, -1):
        candidate = ' '.join(parts[:i])
        if candidate in commands_json:
            base_command = candidate
            remaining_args = parts[i:]
            break
    else:
        return None, None, None

    command_config = commands_json[base_command]
    return command_config, base_command, remaining_args[0] if remaining_args else None

def process_logo(logo_lines, version, source,author,website, color_map=None):
    if color_map is None:
        color_map = {
            '░': f'{color.c("░", c_blue)}',  # Blue
            '▄': f'{color.c("▄", c_green)}',  # Green
            '▀': f'{color.c("▀", c_yellow)}',  # Yellow
        }
    
    # Join all lines with newlines
    result = "\n".join(logo_lines)
    
    # Replace each char according to the map
    for char, colored_char in color_map.items():
        result = result.replace(char, colored_char)
    
    result = result.replace("__version__", version)
    result = result.replace("__source__", source)
    result = result.replace("__author__", author)
    result = result.replace("__website__", website)
    return result

if URL!=str('None') and KEY!=str('None'):
    try:
        con=webhole(url=URL, user_key=KEY)
        if con.fatal_error:
            print("🔥 Critical Errors:")
            for idx, err in enumerate(con.messages, 1):
                print(f"{idx}. {err}")
            sys.exit(1)  # Exit if initialization failed
        else:
            # Proceed with normal operations
            print("✅ Connection successful!")
            package_name=con.connect(value="package_name")
    except:
        exit()

    # Read JSON file
    with open("config.json", "r", encoding="utf-8") as file:
        cmd_data  = json.load(file)  # Load JSON into a dictionary
        logo = cmd_data["logo"]  # Get the "logo" key
        cmd_data = cmd_data["commands"]  # Access the "commands" key

    print(process_logo(logo,__version__,__source__,__author__,__website__))

    xxr1=color.c('┌──(', c_green)
    xxr2=color.c(')──[', c_green)
    xxr3=color.c(']', c_green)
    xxr4=color.c('└─WEBHOLE→ ', c_green)
    xxr_at=color.c('@', c_green)
    xxr_URL=color.c(URL, c_blue).replace("https://", "").replace("http://", "")
    xxr_package_name=color.c(package_name, c_white_red)

    try:
        while True:
            pwd=con.connect(value="pwd")
            xxr_pwd=color.c(pwd, c_yellow)
            command=input(xxr1+xxr_package_name+xxr_at+xxr_URL+xxr2+xxr_pwd+xxr3+'\n'+xxr4)

            if not command:
                continue
            
            cmd_options,cmd,cmd_parts = match_command(command, cmd_data)
            
            if cmd_options is not None and cmd is not None:
                c_action = cmd_options["action"]
                c_params = cmd_options["parameters"]
                c_output = cmd_options["output"]
                c_post_execute = cmd_options["post_execute"]
                c_return_list = cmd_options["return_list"]

                for key, value in c_params.items():
                    if isinstance(value, str) and value.strip().startswith("con.connect"):
                        c_params[key] = eval(value)
                    elif value in globals():
                        c_params[key] = globals()[value]
                    else:
                        c_params[key] = value
                        
                if c_action['type'] == "query":
                    output = con.connect(cli=cmd, **c_params)

                elif c_action['type'] == "function":
                    output = eval(c_action['handler'])

                if bool(c_post_execute):
                    globals()[c_post_execute] = output

                if bool(c_output) and not bool(c_return_list):
                    print(output)
                
                if bool(c_return_list) and bool(c_output):
                    import ast
                    lst = ast.literal_eval(output)
                    if isinstance(lst, list):
                        for item in lst:
                            print(item)
                    else:
                        print("❌ Error: Expected a list but got:", type(output))
            
            else:
                print(con.connect(command))
    
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    '''
    except Exception as e:
        print(f"Error: {str(e)}")'''
elif HOLE!=str('None'):
    if NKEY!=str('None'):
        con=webhole(hole=str(HOLE), nkey=NKEY)
    else:
        con=webhole(hole=str(HOLE))
elif args.PKGS:
    con=webhole(pkgs=True)
else:
    print("""usage: main.py [-h] [--KEY KEY] [--URL URL] [--HOLE HOLE] [--NKEY NKEY] [--PKGS]

Webhole Command-Line Interface: Configure keys, URLs, and manage packages.

options:
  -h, --help                   Show this help message and exit.
  --KEY KEY, --key KEY         Authentication key used for secure operations. Can be provided via the KEY environment variable.
  --URL URL, --url URL         Target URL for the operation. Can be provided via the URL environment variable.
  --HOLE HOLE, --hole HOLE     Hole identifier or reference. Can be provided via the HOLE environment variable.
  --NKEY NKEY, --nkey NKEY     New authentication key for updating or replacing an existing key. Can be provided via the NKEY environment variable.       
  --PKGS, --pkgs               Display all installed packages in Webhole. Can be enabled via the PKGS environment variable.""")