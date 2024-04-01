## Parsing news from websites :newspaper:
Sending updates is done via Telegram API

This project enables you to send updates to a Telegram channel with bot. 

> ⚠️ Bot which API key you use in this project must be adminstrator of the channel which id you use. 

Furthermore, the project maintains a basic database by storing the last sent news from each website in an automatically generated corresponding _".txt"_ file.

## For the fast deploy on Linux you can try the following steps 🐳
1. Clone the project:
```
git clone https://github.com/Kerensk1y/News_parser.git
```
2. Install the requiered modules:
```
pip3 install -r requierments.txt
```
3. Allow execution for `setup.sh`:
```
cd news_parser
```
```
chmod +x setup.sh
chmod +x bot_run.sh
chmod +x bot_stop.sh
```
4. Run setup.sh and insert the _"channel_id"_ and _"API_KEY"_ variables:
```
./setup.sh
```
5. Run the `main.py` file in the background via `bot_run.sh`:
```
nohup ./bot_run.sh &
```
For stopping the process use:
```
./bot_stop.sh
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

1. **main.py**: This file contains all the algorithms necessary for the correct functioning of the project (contained in the project)

2. **web_pages.py**: This file contains the information on how web page parsing is accomplished (contained in the project)

3. **bot_run.sh**: sh script for restarting **"main.py"** if it crashed and log it (contained in the project)

4. **bot_log.txt**: file created via **"bot_run.sh"** it contains starting and restarting logs (created automatically)

5. **logger.log**: logs from telegram bot (updates, errors) (created automatically)

6. **setup.sh**: needed comands to start - insertion api key, channel id and create `db` directory (contained in the project)

7. **t0ken.py**: Variables for the interaction with your bot via API. As described above this file contains your own __API key__ and id of your channel (created automatically, filled by user)

8. **db**: directory used for the database storage (created automatically)
## Prerequisites 📚

:pushpin: Make sure you have the following Python modules installed to run this project:

- pyTelegramBotAPI (used v.4.14.0)
- BeautifulSoup4 (used v.4.12.2)
- requests (used v.2.31.0)

:pushpin: In addition, the project utilizes built-in Python modules, including:

- time
- os
- logging

## Python Version 🐍

This project is written in Python 3.10

## License 📄

This project is licensed under the [GNU General Public License v2.0](LICENSE.md) - see the [LICENSE.md](LICENSE.md) file for details.
