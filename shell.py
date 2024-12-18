import sys
import os
import pathlib
import re




        

# command functions
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

def type_cmd(*args):
    funcs=args[0]
    if len(funcs) > 1:
        print("type: too many arguments")
    elif len(funcs) == 1:
        arg=funcs[0]
        if arg in valid_commands:
             print(f"{arg} is a shell builtin")
        elif find(arg):
            print(find(arg))
        else:
            print(f"{arg}: not found")
    else:
        print("type: missing argument")
def pwd(*args):
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
        print(os.listdir())
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
        "mkdir":mkdir
    }       


#helper functions

#to separate arguments by ''
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
    path = os.environ['PATH']
    for directory in path.split(':'):
        full_path = os.path.join(directory, name)
        if os.path.isfile(full_path):
            return full_path
    return None





def main():


    # Wait for user input
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        full_command = input()
        command_args=full_command.split(' ',1)
        if len(command_args) == 0:
            print("type help for all valid commands")
            continue
        command=command_args[0]
        arguments=separate_args(full_command.split(' ',1)[1:])
        if command in valid_commands:
            valid_commands[command](arguments)
        elif find(command.split()[0]):
            os.system(full_command)
            continue
        else:
            print(f"{command}: command not found, type help for all valid commands")   




if __name__ == "__main__":
    main()


