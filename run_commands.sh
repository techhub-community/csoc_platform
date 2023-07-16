#!/bin/bash

# Check if a command is provided
if [ -z "$1" ]; then
    echo "Please provide a command to execute."
    exit 1
fi

# Set the additional settings
additional_settings="--settings=csoc_backend.settings.local"

# Run the manage.py command with additional settings and user-provided parameters
python manage.py "$@" $additional_settings
