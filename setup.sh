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
    SHELL_CONFIG=~/.bash_aliases
    SHELL_TYPE="bash"
    # Check if the file exists
    if [ ! -f "$ALIASES_FILE" ]; then
        echo "File ~/.bash_aliases does not exist. Creating it now..."
        touch "$ALIASES_FILE"
        echo "# This file is used to store custom aliases" >> "$ALIASES_FILE"
        echo "File ~/.bash_aliases created successfully."
    else
        echo "File ~/.bash_aliases already exists."
    fi
elif [ "$1" == "zsh" ]; then
    SHELL_CONFIG=~/.zshrc
    SHELL_TYPE="zsh"
else
    echo "Error: Unsupported shell type '$1'. Use 'bash' or 'zsh'."
    usage
fi

# Step 1: Create the Python virtual environment and install dependencies
cd ~ || exit

# Create virtual environment
if [ ! -d "BordedAF_env" ]; then
    echo "Creating virtual environment BordedAF_env..."
    python3 -m venv BordedAF_env
else
    echo "Virtual environment BordedAF_env already exists."
fi
# Activate virtual environment and install dependencies
source ~/BordedAF_env/bin/activate
pip install --upgrade pip
pip install rich ics Pillow beautifulsoup4 requests

deactivate

# Step 2: Configure the alias
ALIAS_COMMAND="alias hateCISD='function _hateCISD() { cd; source ~/BordedAF_env/bin/activate; python3 ~/BoredAF/wanna_quit_my_major.py \"\$@\"; }; _hateCISD'"
if ! grep -Fq 'alias hateCISD' "$SHELL_CONFIG"; then
    echo "" >> "$SHELL_CONFIG"
    echo "$ALIAS_COMMAND" >> "$SHELL_CONFIG"
    echo "Alias added to $SHELL_CONFIG"
else
    echo "Alias already exists in $SHELL_CONFIG"
fi