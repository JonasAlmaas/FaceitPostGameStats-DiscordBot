from prettytable import PrettyTable

from discord.channel import TextChannel
from discord.ext.commands import Bot
from discord import Intents
from discord import Embed

from faceit_api import FaceitAPI


class DiscordBot:

    def __init__(
        self,
        channel_id: int,
        player_faceit_id: str,
        match_count: int,
        faceit_api: FaceitAPI,
    ) -> None:
        self.channel_id = channel_id
        self.player_faceit_id = player_faceit_id
        self.match_count = match_count
        self.faceit_api = faceit_api

        bot_intents = Intents().all()
        self.bot = Bot(intents=bot_intents, command_prefix='!')

    async def run(self, token: str):
        await self.bot.start(token, reconnect=True)

    async def close(self):
        await self.bot.close()

    def event(self, coro):
        self.bot.event(coro)

    async def post_discord_message(self):
        faceit_match_history = self.faceit_api.get_player_history()
        if faceit_match_history is None:
            return

        faceit_player_details = self.faceit_api.get_player_info()
        if faceit_player_details is None:
            return

        channel = self.bot.get_channel(self.channel_id)
        if not isinstance(channel, TextChannel):
            return

        await channel.purge(limit=500)

        for match in reversed(faceit_match_history['items']):
            if match['game_id'] != 'csgo':
                continue

            match_stats = self.faceit_api.get_match_stats(match['match_id'])
            if match_stats is None:
                continue

            round = match_stats['rounds'][0]
            found_player = False
            for team in round['teams']:
                if found_player:
                    break

                for player in team['players']:
                    if player['player_id'] != self.player_faceit_id:
                        continue

                    embed = Embed(
                        title=f'{faceit_player_details["nickname"]}\'s Faceit stats',
                        color=0xff0000,
                    )

                    embed.set_thumbnail(url=faceit_player_details['avatar'])
                    embed.set_footer(text='For more information visit fuckamirz.co.uk')

                    embed.add_field(
                        name=f'{round["round_stats"]["Map"]} - {round["round_stats"]["Score"]}',
                        value='',
                        inline=False,
                    )

                    if team['team_id'] == round["round_stats"]["Winner"]:
                        embed.color = 0x00ff00

                    kills = player['player_stats']['Kills']
                    assists = player['player_stats']['Assists']
                    deaths = player['player_stats']['Deaths']
                    mvps = player['player_stats']['MVPs']
                    kd = player['player_stats']['K/D Ratio']
                    headshots = player['player_stats']['Headshots']
                    headshot_percentage = player['player_stats']['Headshots %']

                    embed.add_field(name=f'Kills', value=f'{kills}', inline=True)
                    embed.add_field(name=f'Assists', value=f'{assists}', inline=True)
                    embed.add_field(name=f'Deaths', value=f'{deaths}', inline=True)
                    embed.add_field(name=f'MVPs', value=f'{mvps}', inline=True)
                    embed.add_field(name=f'K/D Ratio', value=f'{kd}', inline=True)
                    embed.add_field(name=f'Headshots', value=f'{headshots}', inline=True)
                    embed.add_field(name=f'Headshots %', value=f'{headshot_percentage}', inline=True)

                    await channel.send(embed=embed)

                    found_player = True
                    break

            print('Loading...')

        last_match = faceit_match_history['items'][0]
        if last_match['game_id'] == 'csgo':
            match_stats = self.faceit_api.get_match_stats(last_match['match_id'])
            if match_stats is not None:

                round = match_stats['rounds'][0]
                for team in round['teams']:
                    table = PrettyTable()
                    table.field_names = ['', 'K', 'A', 'D', 'MVP', 'HS', 'HS%', 'K/D']

                    for player in team['players']:
                        table.add_row([
                            player['nickname'],
                            player['player_stats']['Kills'],
                            player['player_stats']['Assists'],
                            player['player_stats']['Deaths'],
                            player['player_stats']['MVPs'],
                            player['player_stats']['Headshots'],
                            player['player_stats']['Headshots %'],
                            player['player_stats']['K/D Ratio'],
                        ])

                    embed = Embed(
                        description=f'```{table.get_string()}```',
                        color=0xff0000,
                    )

                    if team['team_id'] == round["round_stats"]["Winner"]:
                        embed.color = 0x00ff00

                    await channel.send(embed=embed)

        embed = Embed(
            title=
            f'{faceit_player_details["nickname"]}\'s current elo is {faceit_player_details["games"]["csgo"]["faceit_elo"]}',
            color=0xff00ff,
        )
        await channel.send(embed=embed)
