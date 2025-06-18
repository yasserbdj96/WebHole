#START{
from webhole import webhole
import argparse
import os
from hexor import *
import json
import sys

# Create an ArgumentParser object
parser = argparse.ArgumentParser()

#
parser.add_argument('--KEY', '--key', dest='KEY', type=str, default=os.getenv('KEY', None), help='Specify the key for the operation.')
parser.add_argument('--URL', '--url', dest='URL', type=str, default=os.getenv('URL', None), help='Specify the URL for the operation.')
parser.add_argument('--HOLE', '--hole', dest='HOLE', type=str, default=os.getenv('HOLE', None), help='Specify the hole for the operation.')

# Parse the command-line arguments
args = parser.parse_args()

# Access the variables by their names
KEY = str(args.KEY)
URL = str(args.URL)
HOLE = str(args.HOLE)

 #colors with hexor:
color=hexor(True,"hex")
#used hex colors in this programm:
c_red="#ea4335"#red
c_white_red="#f3938b"#white-red
c_blue="#4285f4"#blue
c_yellow="#fbbc05"#yellow
c_green="#34a853"#green
c_white="#ffffff"

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
        cmd_data = cmd_data["commands"]  # Access the "commands" key


    xxr1=color.c('┌──(', c_green)
    xxr2=color.c(')──[', c_green)
    xxr3=color.c(']', c_green)
    xxr4=color.c('└─WEBHOLE> ', c_green)
    xxr_at=color.c('@', c_red)
    xxr_URL=color.c(URL, c_blue).replace("https://", "").replace("http://", "")
    xxr_package_name=color.c(package_name, c_white_red)

    try:
        while True:
            pwd=con.connect(value="pwd")
            #print(pwd)
            xxr_pwd=color.c(pwd, c_yellow)
            command=input(xxr1+xxr_package_name+xxr_at+xxr_URL+xxr2+xxr_pwd+xxr3+'\n'+xxr4)

            if not command:
                continue  # Ignore empty input

            #parts = command.split(maxsplit=1)
            #cmd = parts[0]  # Extract command name
            #cmd_parts = parts[1] if len(parts) > 1 else None  # Extract argument if provided

            #x=match_command(command, cmd_data)
            #print(x)
            
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
    con=webhole(hole=str(HOLE))
    
else:
    print("""usage: main.py [-h] [--KEY KEY] [--URL URL]

options:
  -h, --help                                      Show this help message
  --KEY=[KEY], --key=[KEY]                        Authentication key
  --URL=[URL], --url=[URL]                        Server endpoint URL
  --HOLE=[PACKAGE_NAME], --hole=[PACKAGE_NAME]    Get Hole Code for a specific package""")