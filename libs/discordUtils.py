def getChannel(client, channelName):
    results = []
    for channel in client.get_all_channels():
        if channel.name == channelName:
            results.append(channel)
    return results

def getAuthor(server, authorName):
    for member in server.members:
        if member.name == authorName:
            return member
    return None
