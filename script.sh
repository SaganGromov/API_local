#!/bin/bash

# Check if a message was provided
if [ -z "$1" ]; then
  echo "Usage: $0 \"Your Morse code message here\""
  exit 1
fi

# Navigate to the morse directory
cd morse || exit

# Run the Morse code command with the provided message
echo "$1" | python3 play.py -f 750 --wpm 10

