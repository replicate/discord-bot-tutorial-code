import os

import async_wrap_iter
import interactions
import replicate
from dotenv import load_dotenv
from async_wrap_iter import async_wrap_iter

# When Poetry 1.2 is released, could use this: https://github.com/mpeteuil/poetry-dotenv-plugin
load_dotenv()
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
DISCORD_SCOPE = os.environ.get("DISCORD_SCOPE")
if DISCORD_SCOPE:
    DISCORD_SCOPE = int(DISCORD_SCOPE)

bot = interactions.Client(token=DISCORD_TOKEN)


@bot.command(
    name="pixray",
    description="Run pixray.",
    scope=DISCORD_SCOPE,
    options=[
        interactions.Option(
            name="prompt",
            description="text prompt",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def pixray(ctx: interactions.CommandContext, prompt: str):
    msg = await ctx.send("Starting...")

    model = replicate.models.get("pixray/text2image")

    iterator = model.predict(prompts=prompt)
    # wrap in async iterator so it works with discord-py's async/await
    iterator = async_wrap_iter(iterator)

    async for image in iterator:
        msg._client = bot._http  # HACK: why??
        await msg.edit(image)


print("starting bot...")
bot.start()
