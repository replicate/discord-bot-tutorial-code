# Replicate Discord bot

A Discord bot that runs things on Replicate.

<img width="475" alt="Screen Shot 2022-05-30 at 18 04 27" src="https://user-images.githubusercontent.com/40906/171073432-f34a77a2-4b1c-489f-b9e5-8b55b1357522.png">

Try it out in #art on the Replicate Discord server: https://discord.gg/replicate

## Development environment

[Follow the instructions here to create an application in Discord.](https://discordpy.readthedocs.io/en/stable/discord.html) You'll want to give it permissions to create messages.

Add your Discord app token and Replicate API key to `.env`:

    REPLICATE_API_TOKEN=...
    DISCORD_TOKEN=...

You'll also need an API key from Replicate.

Then, run the bot like this:

    poetry run python bot.py

## Deploy

You can use Fly to deploy the bot to the cloud.

[Follow this guide.](https://fly.io/docs/speedrun/) In short, you'll need to run:

    flyctl launch
    flyctl deploy
    flyctl secrets set REPLICATE_API_TOKEN=... DISCORD_TOKEN=...
