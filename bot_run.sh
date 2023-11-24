#!/bin/bash

LOG_FILE="bot_log.txt"

echo "Bot started at: $(date)" >> "$LOG_FILE"

while true; do
    {
        python3 ~/news_parser/main.py
        echo "---------------------------"
        echo "Bot crashed at: $(date)"
        echo "Restarting in 10 seconds..."
    } >> "$LOG_FILE"
    sleep 10
done
