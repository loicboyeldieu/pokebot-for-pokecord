# Name          : pokebot.py
# Author        : Loïc Boyeldieu @L01c
# Description   : A bot for Discord Pokécord to automatically capture Pokémons,
#                 xp them and remotely control commands from another account.
# Date          : 28-06-2018

import discord
import asyncio
import time
import json
import hashlib
import traceback
import re
import sys

from random import randint

import libs.constants as constants
import libs.discordUtils as discordUtils
import libs.fileHelper as fileHelper
import libs.hashUtils as hashUtils

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    global hashScores
    global pokemonCatched
    global legendary

    hashScores = fileHelper.readFile(constants.HASHSCORES_PATH)
    legendary = set(fileHelper.readFile(constants.LEGENDARY_PATH))

    pexTask = client.loop.create_task(auto_typing())

@client.event
async def on_message(message):
    global hashScores
    global pokemonCatched
    global legendary
    global pexTask

    try :
        server = message.server
        channel = message.channel
        embeds = message.embeds
        author = message.author
        content = message.content

        if author.name == "Pokécord":
            await auto_catch_pokemons(server, channel, embeds, author, content)

        elif author.name in constants.CAPTAINS:
            await orders_from_captains(server, channel, embeds, author, content)
    except Exception:
        print(constants.ERROR_ON_MESSAGE_RECEIVED)
        traceback.print_exc()

async def auto_typing():
    channels = discordUtils.getChannel(client, constants.BOT_CHANNEL)
    while True:
        try:
            for channel in channels:
                length = randint(1, 15)
                alphabet = 'abcdefghijklmnopqrstuvwxyz  '
                msg = "m:"
                msg += "".join([alphabet[randint(0, len(alphabet)-1)] for x in range(length)])
                await client.send_message(channel, msg)
            await asyncio.sleep(2)
        except Exception:
            print("Error writing message")

async def auto_catch_pokemons(server, channel, embeds, author, content):
    global hashScores
    global pokemonCatched
    global legendary
    global pexTask
    if channel.name in constants.CATCH_CHANNELS:
         for e in embeds:
             if "title" in e and constants.POKEMON_APPEAR_MESSAGE in e['title']:
                 url = e["image"]["url"]
                 hashcode = hashUtils.getHash(url)
                 pokeName = hashScores[hashcode]
                 print(pokeName + " has appeared")
                 if pokeName in legendary:
                     catchMessage = 'p!catch ' + pokeName
                     await client.send_message(channel, catchMessage)
                     print(" ##### - Legendary pokemon catched: " + pokeName)
                     await client.send_message(discordUtils.getChannel(client, constants.INFO_CHANNEL)[0], constants.LEGENDARY_CATCHED_MESSAGE)
                     await client.send_message(discordUtils.getChannel(client, constants.INFO_CHANNEL)[0], "p!info " + pokeName)

async def orders_from_captains(server, channel, embeds, author, content):
    global hashScores
    global pokemonCatched
    global legendary
    global pexTask
    if content.startswith('ord='):
        print("Order received: " + content.split('=')[1])
        order = content.split('=')[1]
        await client.send_message(getChannel(client, constants.INFO_CHANNEL)[0], order)
    elif content.startswith('task='):
        print("Task received: " + content.split('=')[1])
        task = content.split('=')[1]
        if task == "pex":
            if pexTask == None:
                pexTask = client.loop.create_task(auto_typing())
        elif task == "stoppex":
            if pexTask != None:
                pexTask.cancel()
                pexTask = None
        elif "stats" in task:
            pName = task.split(" ")[1]
            await get_best_stats_for_pokemon(pName, server)

async def get_current_and_last_captured_pokemon(channel, server):
    msg = None

    def check(message):
        return message.embeds[0].content == True #TODO

    while msg == None:
        await client.send_message(channel, "p!info")
        msg = await client.wait_for_message(channel=channel, author=getAuthor("Pokécord", server), check=check)

    currentPattern = re.compile("r(\d+)\/")
    lastPattern = re.compile(r"\/(\d+)")
    current = re.match(currentPattern, msg)
    last = re.match(lastPattern, msg)
    return current, last


async def get_best_stats_for_pokemon(pName, server):
    channel = discordUtils.getChannel(client, constants.INFO_CHANNEL)
    await client.send_message(channel[0], "#TASK - Stats task started")
    await asyncio.sleep(2)

    current, last = await get_current_and_last_captured_pokemon(channel[0], server)

    msg = None

    def check(msg):
        print(msg.embeds[0])
        return msg.embeds[0]['title'] == 'Your pokémon:'

    def getIds(description):
        lines = description.split("\n")
        for l in lines:
            n = l.split("Number: ")[1]
            yield int(n)

    while(msg==None):
        await client.send_message(channel[0], "p!pokemon --name " + pName)
        author = discordUtils.getAuthor("Pokécord", server)
        print(author.name)
        msg = await client.wait_for_message(timeout=10, author=author, check=check)

    description = msg.embeds[0]['description']
    ids = list(getIds(description))
    await asyncio.sleep(2)
    for i in ids:
        await client.send_message(channel[0], "p!select " + str(i))
        await asyncio.sleep(3)
        await client.send_message(channel[0], "p!info")
        await asyncio.sleep(3)

    await client.send_message(channel[0], "p!select " + current)
    await asyncio.sleep(2)
    await client.send_message(channel[0], "#TASK - Stats task finished")


# Initialisation

hashScores = {}
pokemonCatched = {}
legendary = {}
pexTask = None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(constants.ARGUMENTS_ERROR)
        sys.exit(1)

    token = sys.argv[1]
    client.run(token, bot=False)
