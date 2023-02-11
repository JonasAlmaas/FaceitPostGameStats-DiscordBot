import os
from fastapi import FastAPI, Request

FACEIT_API_KEY = os.environ['FACEIT_API_KEY']
FACEIT_PLAYER_ID = os.environ['FACEIT_PLAYER_ID']
NUMBERS_OF_MATCHES = int(os.environ['NUMBERS_OF_MATCHES'])
BOT_TOKEN = os.environ['BOT_TOKEN']
BOT_CHANNEL_ID = int(os.environ['BOT_CHANNEL_ID'])

from faceit_api import FaceitAPI
from bot import DiscordBot

faceit_api = FaceitAPI(FACEIT_API_KEY, FACEIT_PLAYER_ID, NUMBERS_OF_MATCHES)

api = FastAPI(
    title='Faceit Stats Discord Bot',
    version='1.0.0',
)


@api.get("/")
async def root():
    return 'I am alive!'


@api.post("/onMatchFinished")
async def onMatchFinished(request: Request):
    bot = DiscordBot(BOT_CHANNEL_ID, FACEIT_PLAYER_ID, NUMBERS_OF_MATCHES, faceit_api)

    @bot.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(bot.bot))
        await bot.post_discord_message()
        await bot.close()

    await bot.run(BOT_TOKEN)
