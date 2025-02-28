from collections.abc import Mapping
import readline
import shlex
import subprocess
import sys
import pathlib
import os
from typing import Final, TextIO

SHELL_BUILTINS: Final[list[str]] = [
    "echo",
    "exit",
    "type",
    "pwd",
    "cd",
]

def parse_programs_in_path(path: str, programs: dict[str, pathlib.Path]) -> None:
    """Creates a mapping of programs in path to their paths"""
    try:
        path_obj = pathlib.Path(path)
        if path_obj.exists() and path_obj.is_dir():
            for item in path_obj.iterdir():
                if item.is_file() and os.access(item, os.X_OK):
                    # Only add the program if it doesn't already exist in the programs dict
                    # This ensures we respect PATH order (first occurrence wins)
                    if item.name not in programs:
                        programs[item.name] = item
    except Exception:
        pass

def generate_program_paths() -> Mapping[str, pathlib.Path]:
    programs: dict[str, pathlib.Path] = {}
    for p in (os.getenv("PATH") or "").split(":"):
        parse_programs_in_path(p, programs)
    return programs

def refresh_programs_in_path() -> Mapping[str, pathlib.Path]:
    """Refreshes the programs in PATH to ensure we have the latest"""
    return generate_program_paths()

COMPLETIONS: Final[list[str]] = [*SHELL_BUILTINS]

def display_matches(substitution, matches, longest_match_length):
    print()
    if matches:
        print("  ".join(matches))
    print("$ " + substitution, end="")

def complete(text: str, state: int) -> str | None:
    programs = refresh_programs_in_path()
    all_completions = [*SHELL_BUILTINS, *programs.keys()]
    matches = list(set([s for s in all_completions if s.startswith(text)]))
    if len(matches) == 1:
        return matches[state] + " " if state < len(matches) else None
    return matches[state] if state < len(matches) else None

readline.set_completion_display_matches_hook(display_matches)
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

def main():
    while True:
        sys.stdout.write("$ ")
        cmds = shlex.split(input())
        out = sys.stdout
        err = sys.stderr
        close_out = False
        close_err = False
        try:
            if ">" in cmds:
                out_index = cmds.index(">")
                out = open(cmds[out_index + 1], "w")
                close_out = True
                cmds = cmds[:out_index] + cmds[out_index + 2 :]
            elif "1>" in cmds:
                out_index = cmds.index("1>")
                out = open(cmds[out_index + 1], "w")
                close_out = True
                cmds = cmds[:out_index] + cmds[out_index + 2 :]
            if "2>" in cmds:
                out_index = cmds.index("2>")
                err = open(cmds[out_index + 1], "w")
                close_err = True
                cmds = cmds[:out_index] + cmds[out_index + 2 :]
            if ">>" in cmds:
                out_index = cmds.index(">>")
                out = open(cmds[out_index + 1], "a")
                close_out = True
                cmds = cmds[:out_index] + cmds[out_index + 2 :]
            elif "1>>" in cmds:
                out_index = cmds.index("1>>")
                out = open(cmds[out_index + 1], "a")
                close_out = True
                cmds = cmds[:out_index] + cmds[out_index + 2 :]
            if "2>>" in cmds:
                out_index = cmds.index("2>>")
                err = open(cmds[out_index + 1], "a")
                close_err = True
                cmds = cmds[:out_index] + cmds[out_index + 2 :]
            handle_all(cmds, out, err)
        finally:
            if close_out:
                out.close()
            if close_err:
                err.close()

def handle_all(cmds: list[str], out: TextIO, err: TextIO):
    # Wait for user input
    match cmds:
        case ["echo", *s]:
            out.write(" ".join(s) + "\n")
        case ["type", s]:
            type_command(s, out, err)
        case ["exit", "0"]:
            sys.exit(0)
        case ["pwd"]:
            out.write(f"{os.getcwd()}\n")
        case ["cd", dir]:
            cd(dir, out, err)
        case [cmd, *args]:
            # Always refresh the programs in PATH before executing
            programs = refresh_programs_in_path()
            if cmd in programs:
                # Pass the program name (cmd) as argv[0], not the full path
                process = subprocess.Popen([cmd, *args], stdout=out, stderr=err)
                process.wait()
            else:
                out.write(f"{cmd}: command not found\n")
        case command:
            out.write(f"{' '.join(command)}: command not found\n")

def type_command(command: str, out: TextIO, err: TextIO):
    if command in SHELL_BUILTINS:
        out.write(f"{command} is a shell builtin\n")
        return
    
    # Always refresh the programs in PATH before checking
    programs = refresh_programs_in_path()
    if command in programs:
        out.write(f"{command} is {programs[command]}\n")
        return
    
    out.write(f"{command}: not found\n")

def cd(path: str, out: TextIO, err: TextIO) -> None:
    if path.startswith("~"):
        home = os.getenv("HOME") or "/root"
        path = path.replace("~", home)
    p = pathlib.Path(path)
    if not p.exists():
        err.write(f"cd: {path}: No such file or directory\n")
        return
    os.chdir(p)

if __name__ == "__main__":
    main()
