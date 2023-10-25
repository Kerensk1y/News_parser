# Parsing news websites
&emsp;Sending updates is done in a pre-defined file in the Telegram channel called **'t0ken.py'**. It should contain two variables:
**'channel_id'** (the channel identifier, including '@') and **'API_KEY'** (the key for interacting with the bot). The storage
of the last sent news from each website is recorded in an automatically created corresponding **'.txt'** file as a basic database.

&emsp;The project consists of two files (the third one, 't0ken.py', as mentioned above, needs to be created manually).
The **'web_pages'** file contains information about how parsing is done. In **'main.py'**, all the other algorithms
necessary for the correct functioning are included.
