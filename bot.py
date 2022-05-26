from async_wrap_iter import async_wrap_iter
from discord.ext import commands
from dotenv import load_dotenv
import os
import replicate


load_dotenv()

bot = commands.Bot(
    command_prefix="!",
    description="Runs models on Replicate! https://github.com/replicate/replicate-discord-bot",
)


@bot.command()
async def pixray(ctx, *, prompt):
    """Run pixray/text2image"""
    msg = await ctx.send(f"“{prompt}”\n> Starting...")

    model = replicate.models.get("pixray/text2image")

    # wrap in async_wrap_iter() so it works with discord-py's async/await
    async for image in async_wrap_iter(model.predict(prompts=prompt)):
        await msg.edit(content=f"“{prompt}”\n{image}")


bot.run(os.environ["DISCORD_TOKEN"])
