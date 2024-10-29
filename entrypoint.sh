#!/bin/bash

# Command to train or serve
if [ "$1" = "train" ]; then
    echo "Running training..."
    python training.py "${@:2}"
else
    echo "Starting prediction service..."
    python predict.py
fi
