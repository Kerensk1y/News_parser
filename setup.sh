api_key="USER INPUT"
read -p "Enter your bot API key: " api_key
ch_id="USER INPUT"
read -p "Enter your channel id: " ch_id

echo -e "API_KEY='$api_key'\nchannel_id='$ch_id'" > ~/news_parser/t0ken.py

mkdir -p ~/news_parser/db

chmod +x ~/news_parser/bot_run.sh
chmod +x ~/news_parser/bot_stop.sh
