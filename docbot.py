import discord
from datetime import datetime
from json import loads, dumps
from docstart import append_text
from drivestart import copy

client = discord.Client()

messageLogPath = "json/messagelog.json"
with open("json/config.json") as configfile:
    config = loads(configfile.read())
datetime_format = "%m/%d/%y %H:%M:%S"



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith("$print"):
        # print last X messages
        # confirm if X is 0 to print all messages

        # get X
        try:
            x = int(message.content.split(' ')[-1])
        except ValueError:
            x = 0

        # get messages
        with open(messageLogPath, 'r') as mlog:
            logs = [None if not item else loads(item)["time"] + ' ' + loads(item)["author"] + ' ' + loads(item)["text"]
                    for item in mlog.read().split('\n')]
            if None in logs:
                logs.remove(None)

        # print results
        if x == 0:
            await message.channel.send('\n'.join(logs) + "\nsuccessfully printed " + str(len(logs)) + " message(s)")
        else:
            logs = logs[-x:]
            await message.channel.send('\n'.join(logs) + "\nsuccessfully printed " + str(len(logs)) + " message(s)")
    elif message.content.startswith("$meeting"):
        # create new meeting documents
        with open(messageLogPath, 'r') as mlog:
            # get logs and process them
            logs = [None if not item else loads(item) for item in mlog.read().split('\n')]
            logs.remove(None)
            for log in logs:
                log["time"] = datetime.strptime(log["time"], datetime_format)

            if len(logs) < 1:
                await message.channel.send("No messages to log. Skipping log creation.")
            else:
                log_name = ""
                if logs[0]["time"].date() == logs[-1]["time"].date():
                    log_name = logs[0]["time"].strftime("%Y/%m/%d, %a")
                id = copy(config["log_template_id"], log_name, config["log_folder_id"])
                url = "https://docs.google.com/document/d/" + id + "/edit"
                text = '\n'.join([log["time"].strftime(datetime_format) + ' ' + log["author"] + ' ' + log["text"]
                                  for log in logs])
                append_text(id, text)
                await message.channel.send("Log document successfully created here: " + url)
        notes_id = copy(config["meeting_notes_template_id"], datetime.now().strftime("%Y/%m/%d, %a"))
        url = "https://docs.google.com/document/d/" + notes_id + "/edit"
        await message.channel.send("Technical Entry document successfully created here: " + url)
        open(messageLogPath, 'w').close()
        await message.channel.send("Cleared message log.")
    elif message.content.startswith("$clear"):
        # clear log last X messages (confirm if X is 0, clear all)
        try:
            x = int(message.content.split(' ')[-1])
        except ValueError:
            x = 0

        if x == 0:
            open(messageLogPath, 'w').close()
            await message.channel.send("Successfully erased message log!")
        else:
            with open(messageLogPath, 'r') as mlog:
                logs = mlog.read().split("\n")
                if "" in logs:
                    logs.remove("")
                else:
                    print(logs)
                logs = logs[:-x]
            with open(messageLogPath, 'w') as mlog:
                mlog.write('\n'.join(logs) + '\n')
            await message.channel.send("Successfully erased last " + str(x) + " message(s) from the message log!")
    else:
        # log messages
        with open(messageLogPath, 'a') as mlog:
            messageObj = {
                "author": str(message.author.display_name),
                "text": message.content,
                "time": datetime.now().strftime(datetime_format)
            }

            mlog.write(dumps(messageObj) + '\n')
if __name__ == "__main__":
    with open("creds/discordsecret.key") as keyfile:
        client.run(config["client_key"])
