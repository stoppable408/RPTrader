import discord
from dotenv import load_dotenv
from modules import parserUtils, Player, db
import re, os, random
from importlib import reload

load_dotenv()
TOKEN = os.getenv('AUTH_TOKEN')
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
@client.event
async def on_message(message):
    if "restart!" in message.content:
            reload(Player)
            reload(parserUtils)
            reload(db)
            await message.add_reaction("👍")
    else:
        await parserUtils.parseMessage(message,client)
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)