# Replicate Discord bot

[Follow the instructions here to create an application in Discord.](https://discordpy.readthedocs.io/en/stable/discord.html) You'll want to give it permissions to create messages.

Add your Discord app token and Replicate API key to `.env`:

    REPLICATE_API_TOKEN=...
    DISCORD_TOKEN=...

You'll also need an API key from Replicate.

Then, run the bot like this:

    poetry run python bot.py

## Deploy

You can use Fly to deploy the bot to the cloud.

[Follow this guide.](https://fly.io/docs/speedrun/). In short, you'll need to run:

    flyctl launch
    flyctl deploy
    flyctl secrets set REPLICATE_API_TOKEN=... DISCORD_TOKEN=...
