import sys
import os
import pathlib
import re
import donut
import subprocess




        


def git_command(*args):
    if not args[0]:
        print("git: missing argument")
    else:
        cmd=["git"]
        for arg in args[0]:
            cmd.append(arg)
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone repository. Error code: {e.returncode}")
        except FileNotFoundError:
            print("Git is not installed or not found in PATH.")



# shell command functions
def draw_donut(*args):
    try:
        donut.draw_donut()
    except KeyboardInterrupt as e:
        print(e)


#exit shell       
def exit(*args):
    if len(args[0]) > 1:
        print("exit: too many arguments")
    elif len(args[0]) == 0:
        sys.exit(0)
    else:
        arg=args[0][0]
        if arg == '0':
            sys.exit(0)
        else:
            print(f"{arg}: invalid argument")

def echo(*args):
    print(" ".join(args[0]))
#type, will display contents of executable files, tell directory paths, and tell shell commands
def type_cmd(*args):
    funcs = args[0]
    if len(funcs) > 1:
        print("type: too many arguments")
    elif len(funcs) == 1:
        arg = funcs[0]
        cwd = os.getcwd() 
        full_path = os.path.join(cwd, arg)

        # check if the argument is a directory
        if os.path.isdir(full_path):
            print(f"{arg} is {full_path}")
            return

        # check ifshell built-in
        if arg in valid_commands:
            print(f"{arg} is a shell builtin")
            return

        # check if  executable file
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            print(f"{arg} is an executable file. Displaying contents:\n")
            try:
                with open(full_path, 'r') as f:
                    print(f.read())
            except Exception as e:
                print(f"Error reading file: {e}")
            return

        if os.path.isfile(full_path):
            print(f"{arg} is {full_path} (not executable)")
            return

        print(f"{arg}: not found")
    else:
        print("type: missing argument")

def pwd(*args):
    if(args):
        print("pwd: too many arguments")
    else:
        print(os.getcwd())

def cd(*args):
    if args[0] ==[]:
        print("cd: missing argument")
        return None
    if len(args[0]) > 1:
        print("cd: too many arguments")
        return None
    path = args[0][0]
    cwd = pathlib.Path(os.getcwd())
    if path == '~':
        home_dir = os.environ.get("HOME")
        if home_dir is None:
                print("HOME environment variable is not set")
        else:
            os.chdir(home_dir)
    else:
        path = cwd.joinpath(path).resolve()
        try:
            os.chdir(path)
        except FileNotFoundError or IsADirectoryError:
            print(f"cd: {path}: No such file or directory")
        except PermissionError:
            print(f"Permission denied to access {path}")

def help(*args):
    if args[0] ==[]:
        print("all avaliable commands:")
        for command in valid_commands:
            print(command)
        return None
    else:
        print("help: too many arguments")
        return None
    
# read files
def cat(*args):
    if args[0] ==[]:    
        print("cat: missing argument")
        return None
    else:
        content=''
        for x in args[0]:

            try:
                with open(x) as f:
                    content += str(f.read())
            except FileNotFoundError:
                print(f"cat: {x}: No such file or directory")
        print(content)

def ls(*args):
    if args[0] ==[]:
        for x in os.listdir():
            print(x)
        return None
    else:
        print("ls: too many arguments")
        return None
   
def mkdir(*args):
    if args[0] ==[]:
        print("mkdir: missing argument")
        return None
    elif len(args[0]) > 1:
        print("mkdir: too many arguments")
        return None
    else:
        for x in args[0]:
            os.mkdir(x)

# execute python scripts
def python_script(*args):
    if args[0] ==[]:
        print("python: missing argument")
        return None
    elif len(args[0]) > 1:
        print("python: too many arguments")
    else:
        for file in args[0:]:
            if file[0].endswith(".py"):
                try:
                    print(f"Executing {file[0]}...")
                    subprocess.run(["python", file[0]], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Execution of {file[0]} failed with error code {e.returncode}.")
                except FileNotFoundError:
                    print(f"Python interpreter or file {file[0]} not found.")
            else:
                print(f"Skipping non-Python file: {file[0]}")


#directory of valid commands to execute their respective functions
valid_commands={
        "exit":exit,
        "echo":echo,
        "type":type_cmd,
        "pwd":pwd,
        "cd":cd,
        "help":help,
        "cat":cat,
        "ls":ls,
        "mkdir":mkdir,
        "donut":draw_donut,
        "python":python_script,
        "git":git_command,

    }       


#helper functions

#to separate arguments by '', catch literals
def separate_args(args):
    if len(args) == 0:
        return []
    args="".join(args)
    pattern = r"'([^']*?)'|(\S+)"
    matches = re.findall(pattern, args)
    
    arguments = []
    for quoted, unquoted in matches:
        if quoted: 
            arguments.append(quoted)
        else:  
            arguments.append(unquoted.replace("'", ""))
 

    return arguments


#helper function for the type command for finding a file
def find(name):
    path = os.getcwd()  # Current working directory
    for root, dirs, files in os.walk(path):  
        if name in files:
            full_path = os.path.join(root, name)
            if os.path.isfile(full_path):  # Ensure it's a file
                return full_path
    return None






def main():


    # Wait for user input
    while True:
        wd=os.getcwd()
        sys.stdout.write(f"{wd}$ ")
        sys.stdout.flush()
        full_command = input()
        if(full_command==""):
            continue
        if(full_command.count("'")%2==1):
            print("error : ' not closed")
            continue
        command_args=full_command.split(' ',1)
        if len(command_args) == 0:
            print("type help for all valid commands")
            continue
        command=command_args[0]
        #get literal arguments
        arguments=separate_args(full_command.split(' ',1)[1:])
        if command in valid_commands:
            valid_commands[command](arguments)
        #open files
        elif find(command.split()[0]):
            try:
                os.system(full_command)
                continue
            except Exception as e:
                print(f"Error executing command: {e}")
                continue
            continue
        else:
            print(f"{command}: command not found, type help for all valid commands")   




if __name__ == "__main__":
    main()


