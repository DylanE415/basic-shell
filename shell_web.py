from flask import Flask, render_template, request, jsonify
import sys
import os
import io
import contextlib

# Import your existing shell script functions
from shell import valid_commands, separate_args, find

app = Flask(__name__)

def execute_command(command):
    """
    Capture the output of shell commands safely
    """
    # Redirect stdout to capture print statements
    output = io.StringIO()
    
    try:
        with contextlib.redirect_stdout(output):
            # Split command and arguments
            command_parts = command.split(' ', 1)
            cmd = command_parts[0]
            
            # Handle arguments
            arguments = separate_args(command.split(' ', 1)[1:]) if len(command_parts) > 1 else []
            
            # Execute built-in commands
            if cmd in valid_commands:
                valid_commands[cmd](arguments)
            
            # Execute external commands
            elif find(cmd.split()[0]):
                os.system(command)
            else:
                print(f"{cmd}: command not found")
        
        return output.getvalue()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html', commands=list(valid_commands.keys()))

@app.route('/execute', methods=['POST'])
def execute():
    command = request.form.get('command', '')
    result = execute_command(command)
    return jsonify({'output': result})

if __name__ == '__main__':
    app.run(debug=True)