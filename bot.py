from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
import os
import replicate

load_dotenv()

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    description="Runs models on Replicate!",
    intents=intents,
    proxy=os.environ["PROXY"] if "PROXY" in os.environ else None,
)


@bot.command()
async def dream(ctx, *, prompt):
    """Generate an image from a text prompt using the stable-diffusion model"""
    msg = await ctx.send(f"“{prompt}”\n> Generating...")

    model = replicate.models.get(os.environ["REPLICATE_MODEL"])
    image = model.predict(prompt=prompt)[0]

    await msg.edit(content=f"“{prompt}”\n{image}")


bot.run(os.environ["DISCORD_TOKEN"])
