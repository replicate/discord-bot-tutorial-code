import asyncio
import httpx
import interactions
import os

REPLICATE_API_TOKEN = os.environ["REPLICATE_API_TOKEN"]
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

bot = interactions.Client(token=DISCORD_TOKEN)


@bot.command(
    name="replicate", description="Run a model on Replicate.", scope=968264728080162857
)
async def my_first_command(ctx: interactions.CommandContext):
    msg = await ctx.send("Starting...")
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.replicate.com/v1/models/pixray/text2image/versions/f6ca4f09e1cad8c4adca2c86fd1f4c9121f5f2e6c2f00408ab19c4077192fd23/predictions",
            json={"input": {"prompts": "hello world"}},
            headers={"Authorization": f"Token {REPLICATE_API_TOKEN}"},
        )
        prediction_id = resp.json()["id"]

        while True:
            print("poll...")
            output_filename = None
            resp = await client.get(
                f"https://api.replicate.com/v1/models/pixray/text2image/versions/f6ca4f09e1cad8c4adca2c86fd1f4c9121f5f2e6c2f00408ab19c4077192fd23/predictions/{prediction_id}",
                headers={"Authorization": f"Token {REPLICATE_API_TOKEN}"},
            )

            prediction = resp.json()
            print(prediction)

            if prediction["output"]:
                if prediction["output"][-1] != output_filename:
                    output_filename = prediction["output"][-1]
                    with open("out.png", "wb") as f:
                        async with client.stream(
                            "GET",
                            f"https://replicate.com/api/models/pixray/text2image/files/{output_filename}",
                            headers={"Authorization": f"Token {REPLICATE_API_TOKEN}"},
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
