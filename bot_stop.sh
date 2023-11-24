kill -n 9 $(ps aux | grep run_bot.sh | head -n 1 | tr -s ' ' | cut -d ' ' -f 2) | kill -n 9 $(ps aux | grep News_parser/main.py | head -n 1 | tr -s ' ' | cut -d ' ' -f 2)
