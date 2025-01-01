import sys
import os
import subprocess
import pathlib
import shlex
from donut import draw_donut
import readline 

readline.parse_and_bind("tab: complete")
readline.parse_and_bind("set editing-mode vi")
history_file = os.path.expanduser("~/.myshell_history")
try:
    readline.read_history_file(history_file)
except FileNotFoundError:
    pass


path= os.getenv("PATH", "").split(os.pathsep)

def parse_args(args):
    args = shlex.split(args)
    return args
def find_executable_path(cmd):
    paths = os.getenv("PATH", "").split(os.pathsep)
    for path in paths:
        executablePath = os.path.join(path, cmd)
        if os.path.isfile(executablePath):
            return executablePath
    return None
def cd(args):
    if args ==[]:
        print("cd: missing argument")
        return None
    if len(args) > 1:
        print("cd: too many arguments")
        return None
    path = args[0]
    if path.startswith('~'):
        path = os.path.expanduser(path)

    try:
        os.chdir(path)
    except Exception:
        print(f"cd: {path}: No such file or directory")
def ls(args):
    args=args
    if len(args)>1:
        print("ls: too many arguments")
    else:
        for x in(os.listdir(os.getcwd())):
            print(x, "-bytes:",os.path.getsize(x))

def exit(args):
    args=args
    if len(args)>1:
        print("exit: too many arguments")
    else:
        try:
            os.remove(history_file)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error deleting history file: {e}")
        sys.exit(0)
def pwd(args):
    if len(args)>0:
        print("pwd: too many arguments")
    else:
        print(os.getcwd())

def echo(args):
    if[args[0]=='"$PATH"']:
        print(path)
    print(" ".join(args))
def cat(args):
    if not args:
        print("cat: missing argument")
    else:
        output=""
        for arg in args:
            try:
                with open(arg) as f:
                    output+=f.read()      
            except FileNotFoundError:
                print(f"cat: {arg}: No such file or directory")
                return
        print(output,end="")
                
def type_cmd(args): 
    if len(args)>1:
        print("type: too many arguments")
    elif args[0] in ("echo", "exit", "type", "pwd", "cd"):
        print(f"{args[0]} is a shell builtin")
    else:
        executablePath = find_executable_path(args[0])
        if executablePath:
            print(f"{args[0]} is {executablePath}")
        else:
            print(f"{args[0]}: not found")

def donut(args):
    try:
        draw_donut()
    except KeyboardInterrupt as e:
        print(e)


import subprocess

def vi(args):
    if len(args) != 1:
        print("vi: too many arguments")
        return

    filename = args[0]
    try:
        # Launch vi ensuring it inherits the terminal's file descriptors
        subprocess.run(['vi', filename], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    except FileNotFoundError:
        print("vi: command not found")
    except Exception as e:
        print(f"Error: {e}")

def launch_vim(args):
    vim_path = os.path.join(os.getcwd(), "macvim", "bin", "vim")

    if not os.path.isfile(vim_path):
        print(f"Error: vim binary not found at {vim_path}")
        return
    os.environ["VIMRUNTIME"] = os.path.join(os.getcwd(), "macvim", "resources", "vim", "runtime")

    vim_args = [vim_path]
    if args:
        vim_args.extend(args)

    try:
        subprocess.run([vim_path] + args)
    except Exception as e:
        print(f"Error: {e}")



def help(args):
    if len(args)>1:
        print("help: too many arguments")
    else:
        print("all commands:")
        for command in builtin_commands:
            print(command)
        print("echo "'"$PATH"'" to print path")
             

builtin_commands={
    "cd":cd,
    "ls":ls,
    "exit":exit, 
    "pwd":pwd,
    "echo":echo,
    "type":type_cmd,
    "cat":cat,
    "donut":donut,
    "vim": launch_vim,
    "help":help
}




def main():


    while True:
        try:
            full_command = input(f"{os.getcwd()} $ ")
            if(full_command==""):
                continue
            args=parse_args(full_command)
            readline.add_history(full_command)
            readline.write_history_file(history_file)

            if args[0] in builtin_commands:
                builtin_commands[args[0]](args[1:])
            else:
                executablePath = find_executable_path(args[0])
                if executablePath:
                    result = subprocess.run(
                        args,capture_output=True, text=True)
                    print(result.stdout, end="")
                else:
                    print(f"{args[0]}: command not found")
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")






if  __name__ == "__main__":
    main()