#!/bin/bash

directory=$(find ~/ -type d -name "news_parser" | head -n 1 | tr -d '\n')

# Находим и завершаем процесс, связанный с /bin/bash ./bot_run.sh
bot_run_pid=$(ps aux | grep "/bin/bash ./bot_run.sh" | grep -v grep | awk '{print $2}')

if [ -n "$bot_run_pid" ]; then
    echo "Killing process with PID $bot_run_pid"
    kill $bot_run_pid
else
    echo "Process /bin/bash ./bot_run.sh is not running"
fi

# Находим и завершаем процесс, связанный с python3 /root/Desktop/news_parser/main.py
python_pid=$(ps aux | grep "python3 $directory/main.py" | grep -v grep | awk '{print $2}')

if [ -n "$python_pid" ]; then
    echo "Killing process with PID $python_pid"
    kill $python_pid
else
    echo "Process python3  $directory/main.py is not running"
fi
