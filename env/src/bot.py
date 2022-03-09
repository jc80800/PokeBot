import os

import discord
from dotenv import load_dotenv
import poke_api, trainer

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MONGOPASS = os.getenv('MONGO_PASS')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    
    print(f'{client.user} has connected to {guild.name}:{guild.id}')
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_field = message.content.split()
    if message_field[0] == '!pokemon':

        if message_field[1] == "pokemon":
            if len(message_field) < 3:
                await message.channel.send("Improper command! Usage: { !pokemon pokemon name {moves} }")
            else:
                embedVar = poke_api.get_information(message_field[2])
                await message.channel.send(embed=embedVar)

        elif message_field[1] == "generation":
            if len(message_field) < 3:
                await message.channel.send("Improper command! Usage: { !pokemon generation {number} }")
            else:
                text = poke_api.get_generation_api(message_field[2])
                await message.channel.send(text)
        elif message_field[1] == "trainer":
            if len(message_field) < 3 or message_field[2] not in ["roll", "info", "collection"]: 
                await message.channel.send("Improper command! Usage: { !pokemon trainer attribute }")
            else:
                lst = trainer.parse(message_field, MONGOPASS, message.author)
                for embedVar in lst:
                    await message.channel.send(embed=embedVar)


client.run(TOKEN)