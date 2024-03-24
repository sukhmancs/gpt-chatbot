import discord
from gpt import MathBot

class MyClient(discord.Client):
    """Class to represent the Client (bot user)"""

    def __init__(self):
        """This is the constructor. Sets the default 'intents' for the bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        """Called when the bot is fully logged in."""
        print('Logged on as', self.user)

    async def on_message(self, message):
        """Called whenever the bot receives a message. The 'message' object
        contains all the pertinent information."""

        # don't respond to ourselves
        if message.author == self.user:
            return

        # check message content and respond accordingly
        if message.content == 'ping':
            await message.channel.send('pong')
        
        # reset dialog
        if message.content.lower() == "reset":
            mathbot.reset_dialog()
            await message.channel.send("Dialog reset.")                    
            return
        
        # handle any other message
        response = mathbot.get_response(message.content, model="both")
        # check if the response is a tuple
        if isinstance(response, tuple):
            await message.channel.send(f"Turbo: {response[0]}\nDavinci: {response[1]}")
        else:
            await message.channel.send(response)        

## Set up and log in
client = MyClient()
with open("openai_key.txt") as file:
    key = file.read()
mathbot = MathBot(key)

with open("discord_token.txt") as file:
    token = file.read()

client.run(token)