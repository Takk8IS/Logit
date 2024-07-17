#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) Takk™ Innovate Studio
# License: Attribution 4.0 International (CC BY 4.0)

# David C Cavalcante
# LinkedIn: https://www.linkedin.com/in/hellodav/
# Medium: https://medium.com/@davcavalcante/
#
# Takk™ Innovate Studio
# Positive results, rapid innovation
# Leading the Digital Revolution as the Pioneering 100% Artificial Intelligence Team
# URL: https://takk.ag/
# X: https://twitter.com/takk8is/
# Medium: https://takk8is.medium.com/
#
# Consider making a donation to support us
# $USDT (TRC-20): TGpiWetnYK2VQpxNGPR27D9vfM6Mei5vNA

# ░▒▓█▓▒░         ░▒▓██████▓▒░   ░▒▓██████▓▒░  ░▒▓█▓▒░ ░▒▓████████▓▒░
# ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    ░▒▓█▓▒░
# ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░        ░▒▓█▓▒░    ░▒▓█▓▒░
# ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒▒▓███▓▒░ ░▒▓█▓▒░    ░▒▓█▓▒░
# ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    ░▒▓█▓▒░
# ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    ░▒▓█▓▒░
# ░▒▓████████▓▒░  ░▒▓██████▓▒░   ░▒▓██████▓▒░  ░▒▓█▓▒░    ░▒▓█▓▒░

import os
import subprocess
import platform
import sys
import shutil
import textwrap
import readline

VERSION = "1.0.0"

def run_command(command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        output, error = process.communicate(timeout=60)
        return output.strip(), error.strip()
    except subprocess.TimeoutExpired:
        return "", "Command execution timed out"
    except Exception as e:
        return "", str(e)

def is_git_installed():
    return shutil.which("git") is not None

def is_git_repo():
    return os.path.isdir('.git')

def get_home_directory():
    return os.path.expanduser("~")

def create_repo():
    if not is_git_repo():
        print("Vamos criar um repositório? (y/n)")
        choice = input().lower()
        if choice == 'y':
            print("Executing: `git init`")
            output, error = run_command('git init')
            if error:
                print(f"Error initializing repository: {error}")
                return False
            print("Git repository initialized.")
        else:
            print("Operation cancelled.")
            return False
    return True

def get_ssh_add_command():
    system = platform.system()
    home = get_home_directory()
    if system == "Windows":
        return f'ssh-add {home}\\.ssh\\id_ed25519'
    elif system == "Darwin":
        return f'ssh-add -K {home}/.ssh/id_ed25519'
    else:
        return f'ssh-add {home}/.ssh/id_ed25519'

def print_help():
    help_text = """
    Logit - Comprehensive Git Management Tool

    Usage:
    Simply run the script and follow the on-screen prompts.

    Features:
    - Covers a wide range of Git operations
    - Interactive menu for easy command selection
    - Cross-platform compatibility (Windows, macOS, Linux)
    - Built-in error handling and user guidance

    Note: Some Git commands can have significant effects on your repository.
    Make sure you understand what each command does before executing it.

    For more information on Git commands, visit: https://git-scm.com/docs
    """
    print(textwrap.dedent(help_text))

def print_formatted_output(output):
    terminal_width = shutil.get_terminal_size().columns
    print("-" * terminal_width)
    for line in output.split('\n'):
        print(textwrap.fill(line, width=terminal_width))
    print("-" * terminal_width)

def truncate_text(text, max_length=50):
    return text[:max_length-3] + '...' if len(text) > max_length else text

def main():
    if not is_git_installed():
        print("Git is not installed. Please install Git and try again.")
        sys.exit(1)

    if not create_repo():
        return

    options = [
        # Initial Setup and Configuration
        ('Configure user.name', 'git config --global user.name "{your_name}"'),
        ('Configure user.email', 'git config --global user.email "{your_email}"'),
        ('Configure default branch name', 'git config --global init.defaultBranch {branch_name}'),
        ('View configurations', 'git config --list'),
        ('Generate SSH key', 'ssh-keygen -t ed25519 -C "{your_email}"'),
        ('Add SSH key to ssh-agent', get_ssh_add_command()),
        ('Initialize repository', 'git init'),
        ('Clone repository', 'git clone {repository_url}'),

        # Remote Repository Management
        ('Add remote', 'git remote add {remote_name} {repository_url}'),
        ('List remotes', 'git remote -v'),
        ('Remove remote', 'git remote remove {remote_name}'),

        # Basic Git Workflow
        ('Check status', 'git status'),
        ('Stage file', 'git add {file_name}'),
        ('Stage all changes', 'git add -A'),
        ('Unstage file', 'git restore --staged {file_name}'),
        ('Discard changes in working directory', 'git restore {file_name}'),
        ('View differences', 'git diff {file_name}'),
        ('View staged differences', 'git diff --staged'),
        ('Commit changes', 'git commit -m "{commit_message}" -m "{extended_description}"'),
        ('Amend last commit', 'git commit --amend'),
        ('Push to remote', 'git push -u {remote_name} {branch_name}'),
        ('Pull from remote', 'git pull {remote_name} {branch_name}'),

        # Branch Management
        ('List branches', 'git branch'),
        ('List remote branches', 'git branch -r'),
        ('Create new branch', 'git branch {branch_name}'),
        ('Switch branch', 'git switch {branch_name}'),
        ('Create and switch to new branch', 'git switch -c {branch_name}'),
        ('Delete local branch', 'git branch -d {branch_name}'),
        ('Force delete local branch', 'git branch -D {branch_name}'),
        ('Delete remote branch', 'git push {remote_name} --delete {branch_name}'),

        # Merging and Rebasing
        ('Merge branches', 'git merge {branch_name}'),
        ('Abort merge', 'git merge --abort'),
        ('Rebase', 'git rebase {branch_name}'),
        ('Abort rebase', 'git rebase --abort'),
        ('Continue rebase', 'git rebase --continue'),
        ('Cherry-pick', 'git cherry-pick {commit_hash}'),

        # History and Logs
        ('View commit log', 'git log'),
        ('View commit log (short format)', 'git log --oneline'),
        ('View commit log with graph', 'git log --graph --oneline --all'),
        ('Show commit details', 'git show {commit_hash}'),

        # Undoing Changes
        ('Revert commit', 'git revert {commit_hash}'),
        ('Reset (soft)', 'git reset --soft {commit_hash}'),
        ('Reset (mixed)', 'git reset --mixed {commit_hash}'),
        ('Reset (hard)', 'git reset --hard {commit_hash}'),

        # Stashing
        ('Stash changes', 'git stash'),
        ('Apply stash', 'git stash apply'),
        ('Pop stash', 'git stash pop'),
        ('List stashes', 'git stash list'),
        ('Show stash', 'git stash show -p {stash_index}'),
        ('Remove stash', 'git stash drop {stash_index}'),

        # Tagging
        ('Create tag', 'git tag {tag_name}'),
        ('Create annotated tag', 'git tag -a {tag_name} -m "{tag_message}"'),
        ('List tags', 'git tag -l'),
        ('Delete tag', 'git tag -d {tag_name}'),
        ('Push tags to remote', 'git push --tags'),

        # Advanced Operations
        ('Fetch from remote', 'git fetch {remote_name}'),
        ('Force push to remote', 'git push -f {remote_name} {branch_name}'),
        ('Clean untracked files', 'git clean -fd'),
        ('Search text in commits', 'git grep "{search_text}"'),
        ('Blame', 'git blame {file_name}'),
        ('Create patch', 'git format-patch -1 {commit_hash}'),
        ('Apply patch', 'git apply {patch_file}'),
        ('Reflog', 'git reflog'),

        # Submodules
        ('Submodule add', 'git submodule add {repository_url} {path}'),
        ('Submodule update', 'git submodule update --init --recursive'),

        # Large File Storage (LFS)
        ('LFS install', 'git lfs install'),
        ('LFS track', 'git lfs track "*.{file_extension}"'),
        ('LFS status', 'git lfs status'),

        # Worktree
        ('Worktree add', 'git worktree add {path} {branch_name}'),
        ('Worktree list', 'git worktree list'),
        ('Worktree remove', 'git worktree remove {path}'),

        # Bisect
        ('Bisect start', 'git bisect start'),
        ('Bisect good', 'git bisect good'),
        ('Bisect bad', 'git bisect bad'),
        ('Bisect reset', 'git bisect reset'),

        # Additional Options
        ('Show Git version', 'git --version'),
        ('Show current branch', 'git rev-parse --abbrev-ref HEAD'),
        ('Show remote URL', 'git remote get-url origin'),
        ('Show last commit', 'git show --summary'),
        ('Show file history', 'git log --follow {file_name}'),
        ('Compare branches', 'git diff {branch1}..{branch2}'),
        ('Find common ancestor', 'git merge-base {branch1} {branch2}'),
        ('Count commits', 'git rev-list --count HEAD'),
        ('List ignored files', 'git check-ignore *'),
        ('Show branch creation date', 'git show -s --format=%cr {branch_name}'),

        # Help and Exit
        ('Help', 'help'),
        ('Exit', 'bye')
    ]

    print(f"Welcome to Logit - Your Comprehensive Git Management Tool")
    print(f"Version {VERSION}")
    print(f"Running on: {platform.system()} {platform.release()}")
    print("Type 'help' for usage information or 'exit' to quit.")

    while True:
        print("\nChoose an option:")
        for i, (desc, command) in enumerate(options, 1):
            print(f"{i}. {desc} `{command}`")

        choice = input("Enter the option number or command: ")

        if choice.lower() == 'help':
            print_help()
            continue
        elif choice.lower() in ['exit', 'quit', 'q']:
            print("Exiting Logit. Goodbye!")
            break

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
            print("Invalid option. Please try again.")
            continue

        choice = int(choice)
        if options[choice-1][1] == 'help':
            print_help()
            continue
        elif options[choice-1][1] == 'bye':
            print("Exiting Logit. Goodbye!")
            break

        command = options[choice-1][1]
        if '{' in command and '}' in command:
            params = [param.split('}')[0] for param in command.split('{')[1:]]
            for param in params:
                value = input(f"{param}: ")
                value = truncate_text(value)
                command = command.replace('{' + param + '}', value)
            print(f"> {command}")
            input("Press ENTER to execute")

        print(f"Executing: {command}")
        output, error = run_command(command)
        if output:
            print("Output:")
            print_formatted_output(output)
        if error:
            print("Error:")
            print_formatted_output(error)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation interrupted by user. Exiting Logit.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
