#!/bin/bash

set -e

# Function to handle errors
handle_error() {
    echo "Error: $1" >&2
    exit 1
}

# Check if Poetry is already installed
if command -v poetry &> /dev/null; then
    echo "Poetry is already installed."
    poetry --version
else
    # User confirmation for installation
    read -p "Poetry is not installed. Do you want to install it? (Y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        echo "Operation cancelled."
        exit 0
    fi

    # Install Poetry
    echo "Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 - || handle_error "Failed to install Poetry"

    # Add Poetry to PATH
    echo "Adding Poetry to PATH..."
    export PATH="$HOME/.local/bin:$PATH"

    # Verify installation
    echo "Verifying Poetry installation..."
    poetry --version || handle_error "Poetry installation failed"
fi

# Check if dependencies are installed
if poetry check --no-interaction &> /dev/null; then
    echo "Dependencies are up to date."
    read -p "Do you want to run 'poetry install' anyway? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Running 'poetry install'..."
        poetry install || handle_error "Failed to run 'poetry install'"
    fi
else
    echo "Dependencies are not installed or out of date. Running 'poetry install'..."
    poetry install || handle_error "Failed to run 'poetry install'"
fi

echo "Running: poetry run $command"
poetry run app || handle_error "Failed to run Poetry command"

echo "Operation completed successfully."