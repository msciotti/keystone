## Keystone

A Discord bot for tracking World of Warcraft mythic+ keystones. Made with the [disco](https://github.com/b1naryth1ef/disco) library.

## How to Run

1. Go to https://discordapp.com/developers/applications/me
2. Create an application & retrieve your bot token
3. Clone the repo & navigate to directory
4. `pip install disco-py`
5. Put your token in `config.yaml`
6. Remove/change [admin id restriction](https://github.com/msciotti/keystone/blob/master/plugins/keystone.py#L45) on importing/export
7. Run `python -m disco.cli --config config.yaml` in terminal

## Commands

| Command | Description |
|---------|-------------|
| help | explains how to use the bot|
| dungeons | returns a list of acceptable abbreviations |
| add | adds a key |
| remove | removes a key |
| list | lists current keys |

![](images/bot_example
.png)