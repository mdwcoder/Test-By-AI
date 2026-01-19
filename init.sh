#!/bin/bash

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
CLI_PATH="$PROJECT_DIR/test_by_ai/cli.py"
ALIAS_NAME="test-by-ai"

# Detect Shell
SHELL_NAME=$(basename "$SHELL")
RC_FILE=""

case "$SHELL_NAME" in
    bash)
        RC_FILE="$HOME/.bashrc"
        ;;
    zsh)
        RC_FILE="$HOME/.zshrc"
        ;;
    fish)
        RC_FILE="$HOME/.config/fish/config.fish"
        ;;
    *)
        echo "Unsupported shell: $SHELL_NAME. Please add the alias manually."
        exit 1
        ;;
esac

echo "Detected shell: $SHELL_NAME"
echo "Target rc file: $RC_FILE"

# Create .venv if not exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists."
fi

# Install dependencies
echo "Installing dependencies..."
"$VENV_DIR/bin/pip" install -r "$PROJECT_DIR/requirements.txt"

# Register Alias
ALIAS_CMD=""
if [ "$SHELL_NAME" = "fish" ]; then
    ALIAS_CMD="alias $ALIAS_NAME 'python3 $CLI_PATH'"
else
    # Check if we should use absolute path to python in venv or just rely on 'python' if sourced?
    # Requirement: "alias test-by-ai="python /ruta/absoluta/.../cli.py""
    # It's safer to use the venv python directly in the alias to avoid activation issues
    ALIAS_CMD="alias $ALIAS_NAME=\"$VENV_DIR/bin/python3 $CLI_PATH\""
fi

if grep -q "$ALIAS_NAME=" "$RC_FILE" 2>/dev/null; then
    echo "Alias already present in $RC_FILE"
else
    echo "Adding alias to $RC_FILE..."
    echo "" >> "$RC_FILE"
    echo "# test-by-ai alias" >> "$RC_FILE"
    echo "$ALIAS_CMD" >> "$RC_FILE"
fi

echo "--------------------------------------------------"
echo "Success! Environment created and dependencies installed."
echo "Alias '$ALIAS_NAME' added to $RC_FILE"
echo "Please reload your shell to use the command:"
echo "  source $RC_FILE"
echo "--------------------------------------------------"
