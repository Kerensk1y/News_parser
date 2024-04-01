#!/bin/bash

# Находим папку news_parser
directory=$(find ~/ -type d -name "news_parser")

# Проверяем, найдена ли папка news_parser
if [ -n "$directory" ]
then
    # Изменяем права доступа ко всем скриптам внутри папки news_parser
    find $directory -type f -name "bot_run.sh" -exec chmod +x {} \;
    find $directory -type f -name "bot_stop.sh" -exec chmod +x {} \;

    # Создаем папку db внутри news_parser
    mkdir -p $directory/db

    api_key="USER INPUT"
    read -p "Enter your bot API key: " api_key
    ch_id="USER INPUT"
    read -p "Enter your channel id: " ch_id
    touch "$directory/t0ken.py"
    echo -e "API_KEY='$api_key'\nchannel_id='$ch_id'" > "$directory/t0ken.py"

else
    echo "Папка news_parser не найдена"
fi
