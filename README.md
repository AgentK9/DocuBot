# DocuBot - A JavaScout Project
DocuBot is a discord bot intended for FIRST Robotics teams to use for documenting their conversations on discord for later use in engineering documentation.
## How to install
1. Install dependencies
2. Clone repository
3. Enable APIs
4. Authorize Bot
5. Configure
6. Run
### 1. Install Dependencies
* google-api-python-client 
* google-auth-httplib2
* google-auth-oauthlib
* discord.py
#### Command
```bash
python3 -m pip install -U discord.py google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
### 2. Clone Repository
Either press the green button in the upper right hand corner of this page or run this command:
```bash
git clone https://github.com/AgentK9/DocuBot.git
```
### 3. Enable APIs
Go [here](https://developers.google.com/drive/api/v3/quickstart/python) and click the button which says "Enable the Drive API".
One may also need to enable the document API as well [here](https://developers.google.com/docs/api/quickstart/js)
Get the credentials (credentials.json as well as a drive key and a docs key) and put them in a folder named creds in the project folder
### 4. Authorize Bot
Go [here](https://discordpy.readthedocs.io/en/latest/discord.html#discord-intro) to create a bot for your server, and copy the key into the config.json file.
You'll also need to invite the bot to your server (admin permissions required)
### 5. Configure
Make two folders in your google drive:
* A folder for your actual meeting entries
* A folder for your discord discussion logs

You will also need to make two google docs which will serve as templates for both your log and entry logs
For each of these, you will need to put their IDs in the [config.json](json/config.json) file.
### 6. Run
Run the bot with `python3 docstart.py`
## Commands
### $hello
#### Description:
Test to make sure that the bot works
#### Result:
The bot will reply in the same channel with "Hello!"
### $print {X}?
#### Parameters
##### Integer X {Optional}
#### Description:
The bot will print all logged messages if X is not specified.
Otherwise, it will print the last X messages.
#### Result:
The bot will reply in the same channel with the last X (or all) messages logged and "X message(s) successfully printed"
### $clear {X}?
#### Parameters
##### Integer X {Optional}
#### Description:
The bot will clear all logged messages from the log if X is not specified.
Otherwise, it will clear the last X messages.
#### Result:
The bot will clear the last X (or all) messages from the log, and reply in the channel with "The last X message(s) successfully cleared"
### $meeting
#### Description
Copies the log template into the specified log folder and writes the saved messages to that document.
Also copies a new technical entry to the specified folder and names it today's date and day.
Finally clears message log.
#### Result:
When documents have been created, sends messages to channel with the links to the created documents.
Also notifies the user that the message log has been cleared.


