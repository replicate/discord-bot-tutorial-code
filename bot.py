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
)


@bot.command()
async def dream(ctx, *, prompt):
    """Generate an image from a text prompt using the stable-diffusion model"""
    msg = await ctx.send(f"“{prompt}”\n> Generating...")
    model = replicate.models.get("stability-ai/stable-diffusion")
    try:
        image = model.predict(prompt=prompt)[0]
    except replicate.exceptions.ModelError as ex:
        if "NSFW" in str(ex): # model output was classified as NSFW
            await msg.edit(content="> NSFW detected. Please try again.")
        else: # something else went wrong, log to console so developer can debug
            print(ex)
            await msg.edit(content="> Error. Please try again.")
        return # return early upon failure
    await msg.edit(content=f"“{prompt}”\n{image}")


bot.run(os.environ["DISCORD_TOKEN"])
