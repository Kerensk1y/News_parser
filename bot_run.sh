#!/bin/bash

LOG_FILE="bot_log.txt"

echo "Bot started at: $(date)" >> "$LOG_FILE"

directory=$(find ~/ -type d -name "news_parser" | head -n 1 | tr -d '\n')

if [ -n "$directory" ]
then
    while true; do
        {
            python3 $directory/main.py
            echo "---------------------------"
            echo "Bot crashed at: $(date)"
            echo "Restarting in 10 seconds..."
        } >> "$LOG_FILE"
        sleep 10
    done
fi
