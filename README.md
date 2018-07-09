# giveawaybot

Give Away Contest Discord Bot

[![PyPI](https://img.shields.io/pypi/v/discord.py.svg)](https://pypi.python.org/pypi/discord.py/)
[![PyPI](https://img.shields.io/badge/python-v3.6-blue.svg)](https://www.python.org/downloads/)

giveawaybot.py is a discord bot to perform member giveaway functions. The main purpose is to manage member crypto addresses for fun giveaways. 

This has only been tested with python3.6.

The bot commands are (assuming a ? prefix):

1. ?help - available for all bots
2. ?enterme <address> - creates or updates an address entry for the member and logs the entry
3. ?showme <membername> - shows the address value for the entered membername
4. ?pickwinner - Randomly select the winner (also logs a win snapshot log of the current entries)
5. ?clearentries - Logs an win snapshot, clears the entry dictionary and clear the entry log

## Installing

1. Create your bot, add bot user, record your bot token and authorize your bot to your server (as per discord apps processing).
2. Download/clone giveawaybot.py and giveawaybot_config_example.ini
3. Copy or rename giveawaybot_config_example.ini to giveawaybot_config.ini
4. Update the config values for your server (will enter token from step 1)
5. Load both file on your server and run the script


## Config File

- [MAIN]
	- BotPrefix = ?! - List of special characters for bot command prefix, 1 to many, no separators, this is "?" and "!".
	- BotUserToken = DiscordToken - This is the tokens for the bot user when you create the bot
	- WinLogName = pickwinner.log - this is the name of the log file - with no path will reside in current directory
	- AdminRole = gabAdmin - Assign this role to memeber who will be able to pickwinner or clearentries (@everyone will allow all)
	- EntryLogName = userentries.log - this is the name of the entries log file - with no path will reside in current directory
	- SeedCount = 0 - for testing purposes you can seed entries at start up. 

## Requirements

- Python 3.6 
- discord.py v0.16.12
- Python modules (should be included in standard library)
	- datetime
	- secrets
	- random
	- configparser

To install discord.py
```
python3 -m pip install -U discord.py
```
