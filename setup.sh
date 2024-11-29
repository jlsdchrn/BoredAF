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

# Add alias to shell configuration
ALIAS_COMMAND="alias myscript='python3 myscript.py'"
if ! grep -Fxq "$ALIAS_COMMAND" "$SHELL_CONFIG"; then
    echo "$ALIAS_COMMAND" >> "$SHELL_CONFIG"
    echo "Alias added to $SHELL_CONFIG"
else
    echo "Alias already exists in $SHELL_CONFIG"
fi

# Run Zsh-specific setup
if [ "$SHELL_TYPE" == "zsh" ]; then
    if ! command -v zsh > /dev/null; then
        echo "Error: Zsh is not installed. Install Zsh and try again."
        exit 1
    fi
    
    # Execute Zsh-specific commands using a subshell
    zsh -c "zstyle ':completion:*' completer _complete"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to configure Zsh completion."
        exit 1
    fi
    echo "Zsh completion configured successfully."
fi

# Reload shell configuration
if [ "$SHELL_TYPE" == "bash" ]; then
    source "$SHELL_CONFIG"
elif [ "$SHELL_TYPE" == "zsh" ]; then
    zsh -c "source $SHELL_CONFIG"
fi

echo "Setup completed successfully for $SHELL_TYPE."
