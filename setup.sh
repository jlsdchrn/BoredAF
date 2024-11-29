#!/bin/bash

# This script sets up a Python virtual environment, installs dependencies, and configures an alias for either bash or zsh.

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
elif [ "$1" == "zsh" ]; then
    SHELL_CONFIG=~/.zshrc
else
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
ALIAS="alias hateCISD='function _hateCISD() { cd; source ~/BordedAF_env/bin/activate; python3 ~/BoredAF/wanna_quit_my_major.py \"\$@\"; }; _hateCISD'"

grep -qxF "$ALIAS" "$SHELL_CONFIG" || echo "$ALIAS" >> "$SHELL_CONFIG"

echo "Alias added to $SHELL_CONFIG"

# Step 3: Source the shell configuration file
source "$SHELL_CONFIG"

echo "Setup complete. You can now use the alias 'hateCISD' to run your script."