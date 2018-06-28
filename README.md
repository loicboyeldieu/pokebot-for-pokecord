# pokebot-for-pokecord

**Description:**

The role of this bot is to catch Pokémons on Pokécord (Discord bot) by automatically guessing their name and typing it in the chat. Additionnal features are: xp to lvl 100, remotely control the bot to execute pokécord commands, find the best stats pokemon among all given name.

**Current Version:**

The current version only catch legendary pokemons to avoid being ban by capturing to many of them too quickly.

**Installation:** 
- Clone this project
- Change the _libs/constants.py_ file with your config
> BOT_CHANNEL: The channel name in which the bot will be typing and catching pokemons.
> INFO_CHANNEL: The channel name where bot informations will be typed (for exemple, to alert you when you have catched a legendary one)
> CATCH_CHANNELS: Any other channels where you wish the bot to catch pokemons. 
> CAPTAINS: User names the bot will listen to for orders and tasks
- In a terminal, run: `python3 pokebot.py <YOUR_DISCORD_USER_TOKEN>`

**Orders and Tasks:**
Orders: captains can type orders to control the bot remotely. Orders has to be type in the _INFO_CHANNEL_. The bot will then type whatever is written after the "ord=" pattern. For exemple if you want to know what pokemons your bot has captured so far, type (with your captain account):
> ord=p!pokemons

Tasks: 
- Start typing randon message in _BOT_CHANNEL_ to xp selected pokemon.
> task=pex

- Stop typing randon message in _BOT_CHANNEL_.
> task=stoppex

- Get stats for all <pokemonName> caught
> task=stats <pokemonName>
