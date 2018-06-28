import imagehash
import re
import requests
from PIL import Image
from io import BytesIO

def saveHash(message, embed, hashScores):
    pattern = re.compile(r"Base stats for (.+).")
    search = embed['footer']['text']
    pokemonName = pattern.findall(search)[0]
    print(pokemonName)
    url = embed["image"]["url"]
    pokeHash = getHash(url)
    hashScores[pokeHash] = pokemonName
    print(pokemonName + " : " + str(pokeHash))
    exportFile('../resources/hashScores.txt', hashScores)

def getHash(url):
    response = requests.get(url)
    im = Image.open(BytesIO(response.content))
    mhash = imagehash.average_hash(im)
    return str(mhash)
