#!/bin/bash

if [ "$1" = "train" ]; then
    echo "Running training..."
    python training.py "${@:2}"
elif [ "$1" = "serve" ]; then
    echo "Starting prediction service..."
    python predict.py
else
    echo "Invalid command. Use 'train' or 'serve'."
    exit 1
fi