import discord
from json import dumps

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

with open("creds/discordsecret.key") as keyfile:
    client.run("Njg1ODYwODQzOTAwMTA4ODUx.XmOzrw.Z9awb0iurUzQs83i8_J6N23mPTg")
