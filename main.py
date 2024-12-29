import sys
import os
import subprocess
import pathlib
import shlex
from donut import draw_donut


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
        sys.exit(0)
def pwd(args):
    if len(args)>0:
        print("pwd: too many arguments")
    else:
        print(os.getcwd())

def echo(args):
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



builtin_commands={
    "cd":cd,
    "ls":ls,
    "exit":exit, 
    "pwd":pwd,
    "echo":echo,
    "type":type_cmd,
    "cat":cat,
    "donut":donut
}

aliases = {
    "python": "python.exe",
    "g++": "g++.exe"
}

def resolve_alias(cmd):
    return aliases.get(cmd, cmd)


def main():



    while True:
        sys.stdout.flush()
        sys.stdout.write(f"$ ")
        full_command = input()
        if(full_command==""):
            continue
        args=parse_args(full_command)
        args[0] = resolve_alias(args[0]) 

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



if  __name__ == "__main__":
    main()