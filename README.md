# Parsing news websites :newspaper:
Sending updates is done in a pre-defined file in the Telegram channel called **'t0ken.py'** :incoming_envelope:

It should contain two variables:
_'channel_id'_ (the channel identifier, including '@') and _'API_KEY'_ (the key for interacting with the bot). The storage
of the last sent news from each website is recorded in an automatically created corresponding **'.txt'** file as a basic database.

&emsp;The project consists of two files (the third one, **'t0ken.py'**, as mentioned above, needs to be created manually).
The **'web_pages.py'** file contains information about how parsing is done. In **'main.py'**, all the other algorithms
necessary for the correct functioning are included.

:pushpin: Used Python modules required for installation: _requests, bs4, pyTelegramBotAPI_

:pushpin: Used Built-in Python modules: _time, os, logging_

:pushpin: _the project is written in Python 3.10_
