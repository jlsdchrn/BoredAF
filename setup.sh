#!/bin/bash

# This script sets up a Python virtual environment, installs dependencies,
# and configures an alias for either Bash or Zsh.

# Function to display usage instructions
usage() {
    echo "Usage: $0 [bash|zsh]"
    echo "  Specify your shell type as the first argument."
    exit 1
}

# Check if a shell type is provided
if [ -z "$1" ]; then
    usage
fi

# Determine the shell configuration file
if [ "$1" == "bash" ]; then
    SHELL_CONFIG=~/.bashrc
    SHELL_TYPE="bash"
elif [ "$1" == "zsh" ]; then
    SHELL_CONFIG=~/.zshrc
    SHELL_TYPE="zsh"
else
    echo "Error: Unsupported shell type '$1'. Use 'bash' or 'zsh'."
    usage
fi

# Check for dependencies
if [ ! -d ~/BordedAF_env ]; then
    echo "Error: Virtual environment directory '~/BordedAF_env' does not exist."
    exit 1
fi

if [ ! -f ~/BoredAF/wanna_quit_my_major.py ]; then
    echo "Error: Python script '~/BoredAF/wanna_quit_my_major.py' does not exist."
    exit 1
fi

# Add alias to shell configuration
ALIAS_COMMAND='alias hateCISD="function _hateCISD { cd; source ~/BordedAF_env/bin/activate; python3 ~/BoredAF/wanna_quit_my_major.py \"$@\"; }; _hateCISD"'
if ! grep -Fq 'alias hateCISD' "$SHELL_CONFIG"; then
    echo "" >> "$SHELL_CONFIG"
    echo "$ALIAS_COMMAND" >> "$SHELL_CONFIG"
    echo "Alias added to $SHELL_CONFIG"
else
    echo "Alias already exists in $SHELL_CONFIG"
fi

# Reload shell configuration
echo "Setup completed successfully for $SHELL_TYPE. Please restart your shell or run 'source $SHELL_CONFIG' to apply changes."
