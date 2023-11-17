## Parsing news from websites :newspaper:
Sending updates is done in a __user-defined__ file in the Telegram channel called `t0ken.py`

This project enables you to send updates to a Telegram channel through a user-defined file called `t0ken.py`. This file should include two essential variables: _"channel_id"_ (the channel identifier, including "@") and _"API_KEY"_ (the key required for interacting with the Telegram bot). 

>Bot whose API key you use in this project must be adminstrator of the channel which id you use. 

Furthermore, the project maintains a basic database by storing the last sent news from each website in an automatically generated corresponding _".txt"_ file.

## For the fast deploy on Linux you can try the following steps 🐳
1. Clone the project:
```
git clone https://github.com/Kerensk1y/News_parser.git
```
2. Install the requiered modules:
```
pip3 install pyTelegramBotAPI BeautifulSoup4 requests
```
3. Create `t0ken.py` file and insert the _"channel_id"_ and _"API_KEY"_ variables:
```
echo -e "API_KEY="insert_your_API_key"\nchannel_id="insert_your_ch_id"" > News_parser/t0ken.py
```
4. Create database directory:
```
mkdir -p News_parser/db
```
5. Run the `main.py` file in the background via `run_bot.sh`:
```
nohup ./run_bot.sh &
```
For stopping the process use:
```
kill -n 9 $(ps aux | grep run_bot.sh | head -n 1 | tr -s ' ' | cut -d ' ' -f 2) | kill -n 9 $(ps aux | grep News_parser/main.py | head -n 1 | tr -s ' ' | cut -d ' ' -f 2)
```
Alternative 5th step with only starting the process:
```
nohup python3 -u main.py &
```
Then the stopping process is:
```
kill -n 9 $(ps aux | grep News_parser/main.py | head -n 1 | tr -s ' ' | cut -d ' ' -f 2)
```
## Project Files 📂

Here is a brief overview of the files:

1. **main.py**: This file contains all the algorithms necessary for the correct functioning of the project.

2. **web_pages.py**: This file contains the information on how web page parsing is accomplished.

3. **t0ken.py**: Variables for the interaction with your bot via API. As described above this file contains your own __API key__ and id of your channel (created by user)

4. **bot_run.sh**: sh script for restarting **"main.py"** if it crashed and log it

5. **bot_log.txt**: file created via **"bot_run.sh"** it contains starting and restarting logs (created automatically)

6. **logger.log**: logs from telegram bot (updates, errors) (created automatically)

7. **db**: directory used for the database storage (created by user)
## Prerequisites 📚

:pushpin: Make sure you have the following Python modules installed to run this project:

- pyTelegramBotAPI
- BeautifulSoup4
- requests

:pushpin: In addition, the project utilizes built-in Python modules, including:

- time
- os
- logging

## Python Version 🐍

This project is written in Python 3.10

## License 📄

This project is licensed under the [GNU General Public License v2.0](LICENSE.md) - see the [LICENSE.md](LICENSE.md) file for details.
