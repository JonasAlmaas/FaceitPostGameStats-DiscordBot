import time
import os
from subprocess import Popen

if __name__ == '__main__':

    env = os.environ.copy()
    env['FACEIT_API_KEY'] = ''
    env['FACEIT_PLAYER_ID'] = ''
    env['NUMBERS_OF_MATCHES'] = '20'
    env['BOT_TOKEN'] = ''
    env['BOT_CHANNEL_ID'] = ''

    Popen('uvicorn main:api --reload', shell=True, env=env)

    while True:
        time.sleep(100)
