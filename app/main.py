import sys
import re
import os
import subprocess
import shlex

BUILDIN_KEYWORDS = [
    "echo",
    "exit",
    "type",
    "pwd",
    "cd",
]
ECHO_PATTERN = re.compile(r"^echo ")
TYPE_PATTERN = re.compile(r"^type ")
CD_PATTERN = re.compile(r"^cd ")
CAT_PATTERN = re.compile(r"^cat ")


def _is_builtin(keyword: str) -> bool:
    return keyword in BUILDIN_KEYWORDS


def _find_in_path(param: str) -> str:
    # Resolve both absolute and relative paths
    if os.path.isfile(param) and os.access(param, os.X_OK):
        return os.path.abspath(param)
    paths = os.getenv("PATH", "").split(os.pathsep)
    for path in paths:
        executable_path = os.path.join(path, param)
        if os.path.isfile(executable_path) and os.access(executable_path, os.X_OK):
            return executable_path
    return None


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()

        if command == "exit 0":
            break

        # Parse command with shlex to handle quoted strings properly
        try:
            cmd_list = shlex.split(command, posix=True)
        except ValueError as e:
            sys.stdout.write(f"Error parsing command: {e}\n")
            continue

        if not cmd_list:
            continue

        cmd = cmd_list[0]
        args = cmd_list[1:]

        # Handle built-in commands
        if cmd == "pwd":
            sys.stdout.write(f"{os.getcwd()}\n")
        elif cmd == "exit":
            code = int(args[0]) if args else 0
            sys.exit(code)
        elif cmd == "echo":
            sys.stdout.write(" ".join(args) + "\n")
        elif cmd == "cd":
            if not args:
                sys.stdout.write("cd: missing argument\n")
            else:
                path = args[0]
                try:
                    os.chdir(os.path.expanduser(path))
                except FileNotFoundError:
                    sys.stdout.write(f"cd: {path}: No such file or directory\n")
                except NotADirectoryError:
                    sys.stdout.write(f"cd: {path}: Not a directory\n")
                except PermissionError:
                    sys.stdout.write(f"cd: {path}: Permission denied\n")
        elif cmd == "type":
            if not args:
                sys.stdout.write("type: missing argument\n")
            else:
                name = args[0]
                if _is_builtin(name):
                    sys.stdout.write(f"{name} is a shell builtin\n")
                elif executable := _find_in_path(name):
                    sys.stdout.write(f"{name} is {executable}\n")
                else:
                    sys.stdout.write(f"{name}: not found\n")
        else:
            # Handle external commands, including quoted executables
            executable_path = _find_in_path(cmd)
            if executable_path:
                try:
                    subprocess.run([executable_path, *args])
                except FileNotFoundError:
                    sys.stdout.write(f"{cmd}: command not found\n")
                except PermissionError:
                    sys.stdout.write(f"{cmd}: Permission denied\n")
            else:
                sys.stdout.write(f"{cmd}: command not found\n")


if __name__ == "__main__":
    main()
