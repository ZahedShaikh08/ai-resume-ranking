#!/bin/bash

# Diagnostic information
echo "----- STARTUP DEBUG INFO -----"
echo "Current PATH: $PATH"
echo "Python version: $(python --version)"
echo "Gunicorn location: $(which gunicorn)"
echo "Working directory: $(pwd)"
echo "Directory contents:"
ls -la
echo "------------------------------"

# Start the application
python -m gunicorn --worker-tmp-dir /dev/shm app:app