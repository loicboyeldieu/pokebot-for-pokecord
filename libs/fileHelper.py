import json

def readFile(fileName):
    with open(fileName, 'r') as file:
        return json.load(file)

def exportFile(fileName, data):
    with open(fileName, 'w') as file:
        file.write(json.dumps(data))
