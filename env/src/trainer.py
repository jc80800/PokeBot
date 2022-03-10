"""
Main file that implements the "gatcha" game for pokemon
Users are able to roll random pokemon and will be saved to their profile
"""

import os

import discord
from dotenv import load_dotenv
import poke_api, random
import pymongo

TOTAL_POKEMON = 898


def parse(message_field, MONGOPASS, author):
    mongo = pymongo.MongoClient(f"mongodb+srv://mongodbjc:{MONGOPASS}@cluster0.jbrvv.mongodb.net/Cluster0?retryWrites=true&w=majority")
    db = mongo.pokemon

    if message_field[2] == "roll":
        random_id = random.randint(1, TOTAL_POKEMON)
        embedVar = poke_api.get_information(random_id)
        lst = db.trainer.find({})
        exist = False
        for document in lst:
            if author.id == document["author"] and random_id == document["card"]:
                db.trainer.update_one({"_id" : document["_id"]}, {"$inc" : {"amount" : 1}} )
                exist = True
                break
        if not exist:
            pokemon_card = {
                'author' : author.id,
                'card' : random_id,
                'amount' : 1
            }
            db.trainer.insert_one(pokemon_card)
        return [embedVar]

    elif message_field[2] == "collection":
        lst = db.trainer.find({"author" : author.id})
        result = []
        for document in lst:
            embedVar = poke_api.get_information(document["card"])
            embedVar.add_field(name="Amount", value=document["amount"], inline=False)
            result.append(embedVar)
        return result
    else:
        return ["Invalid command!"]
        





