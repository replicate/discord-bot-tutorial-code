import asyncio
from dotenv import load_dotenv
import httpx
import interactions
import os

# When Poetry 1.2 is released, could use this: https://github.com/mpeteuil/poetry-dotenv-plugin
load_dotenv()
REPLICATE_API_TOKEN = os.environ["REPLICATE_API_TOKEN"]
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
DISCORD_SCOPE = os.environ.get("DISCORD_SCOPE")
if DISCORD_SCOPE:
    DISCORD_SCOPE = int(DISCORD_SCOPE)

bot = interactions.Client(token=DISCORD_TOKEN)
headers = {"Authorization": f"Token {REPLICATE_API_TOKEN}"}


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
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.replicate.com/v1/models/pixray/text2image/predictions",
            json={"input": {"prompts": prompt}},
            headers=headers,
        )
        if resp.status_code != 201:
            await msg.edit(content=f"Error: {resp.status_code}")
            return
        prediction_id = resp.json()["id"]
        prediction_url = resp.json()["urls"]["get"]

        while True:
            print("poll...")
            output_url = None
            resp = await client.get(
                f"https://api.replicate.com" + prediction_url,
                headers=headers,
            )
            if resp.status_code != 200:
                await msg.edit(content=f"Error: {resp.status_code}. Retrying...")
                await asyncio.sleep(1.0)
                continue

            prediction = resp.json()
            print(prediction)

            if prediction["output"]:
                if prediction["output"][-1] != output_url:
                    output_url = prediction["output"][-1]
                    with open("out.png", "wb") as f:
                        async with client.stream(
                            "GET",
                            output_url,
                            headers=headers,
                        ) as response:
                            async for chunk in response.aiter_bytes():
                                f.write(chunk)
                    msg._client = bot._http  # HACK: why??
                    msg = await msg.edit(
                        content="", files=[interactions.File(filename="out.png")]
                    )
            else:
                msg._client = bot._http  # HACK: why??
                msg = await msg.edit(prediction["status"])

            if prediction["status"] in ["succeeded", "failed"]:
                break

            await asyncio.sleep(1.0)


print("starting...")
bot.start()
