import os

from discord.ext import commands
import replicate
from dotenv import load_dotenv
from async_wrap_iter import async_wrap_iter

# When Poetry 1.2 is released, could use this: https://github.com/mpeteuil/poetry-dotenv-plugin
load_dotenv()

bot = commands.Bot(
    command_prefix="!",
    description="Runs models on Replicate! https://github.com/replicate/replicate-discord-bot",
)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.command()
async def pixray(ctx, *, prompt):
    """Run pixray/text2image"""
    msg = await ctx.send(f"“{prompt}”\n> Starting...")

    model = replicate.models.get("pixray/text2image")

    iterator = model.predict(prompts=prompt)
    # wrap in async iterator so it works with discord-py's async/await
    iterator = async_wrap_iter(iterator)

    async for image in iterator:
        await msg.edit(content=f"“{prompt}”\n{image}")


bot.run(os.environ["DISCORD_TOKEN"])
