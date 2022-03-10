"""
Main file for API access and creates an embed message for bot to send
"""

from dis import disco
from aiohttp import request
import requests
import json
import discord

def get_information(pokemon_name):

    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/")
    if response.status_code == 404:
        return f"Pokemon {pokemon_name} is invalid!"
    
    result = response.json()
    poke_name, id, weight, height, stats, moves = result["name"], result["id"], result["weight"], result["height"], result["stats"], result["moves"]

    front_default_img = result["sprites"]["front_default"]

    stat_text = ""
    for stat in stats:
        base_stat = stat["base_stat"]
        name = stat["stat"]["name"]
        stat_text += f"{str.title(name)} : {base_stat}\n"

    embedVar = discord.Embed(title=str.title(poke_name), description="Something Here for now", color=0x00ff00)
    embedVar.add_field(name="ID", value=id, inline=True)
    embedVar.add_field(name="Weight", value=f"{round(weight / 4.536, 1)}lb", inline=True)
    embedVar.add_field(name="Height", value=f"{height * 10}cm", inline=True)
    embedVar.add_field(name="Stats", value=stat_text, inline=False)
    embedVar.set_thumbnail(url=front_default_img)

    return embedVar

"""
Function for bot to grab all pokemon from a specific generation
"""
def get_generation_api(generation):
    response = requests.get(f"https://pokeapi.co/api/v2/generation/{generation}/")
    if response.status_code == 404:
        return f"Generation {generation} is invalid!"

    result = []
    for pokemon in response.json()["pokemon_species"]:
        result.append(pokemon["name"])
    return result

