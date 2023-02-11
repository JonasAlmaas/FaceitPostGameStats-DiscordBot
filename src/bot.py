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
        faceit_player_details = self.faceit_api.get_player_info()
        if faceit_player_details is None:
            return

        channel = self.bot.get_channel(self.channel_id)
        if not isinstance(channel, TextChannel):
            return

        embed = Embed(
            title=f'{faceit_player_details["nickname"]} just finished a match on FACEIT',
            color=0xff5500,
        )
        embed.set_thumbnail(url=faceit_player_details['avatar'])
        embed.add_field(name='ELO', value=faceit_player_details["games"]["csgo"]["faceit_elo"], inline=True)
        await channel.send(embed=embed)

        faceit_match_history = self.faceit_api.get_player_history()
        if faceit_match_history is None:
            return

        # Scoreboard for last match
        last_match = faceit_match_history['items'][0]
        if last_match['game_id'] == 'csgo':
            match_stats = self.faceit_api.get_match_stats(last_match['match_id'])
            if match_stats is not None:

                _round = match_stats['rounds'][0]
                for team in _round['teams']:
                    scoreboard = []

                    for player in team['players']:
                        scoreboard.append({
                            'nickname': player['nickname'],
                            'Kills': int(player['player_stats']['Kills']),
                            'Assists': int(player['player_stats']['Assists']),
                            'Deaths': int(player['player_stats']['Deaths']),
                            'MVPs': int(player['player_stats']['MVPs']),
                            'Headshots': int(player['player_stats']['Headshots']),
                            'Headshots %': int(player['player_stats']['Headshots %']),
                            'K/D Ratio': float(player['player_stats']['K/D Ratio']),
                        })

                    # Sort by kills
                    sorted_scoreboard = sorted(scoreboard, key=lambda x: (x['Kills'], x['Assists']), reverse=True)

                    table = PrettyTable()
                    table.field_names = ['', 'K', 'A', 'D', 'MVP', 'HS', 'HS%', 'K/D']

                    for player in sorted_scoreboard:
                        table.add_row([
                            player['nickname'],
                            player['Kills'],
                            player['Assists'],
                            player['Deaths'],
                            player['MVPs'],
                            player['Headshots'],
                            player['Headshots %'],
                            player['K/D Ratio'],
                        ])

                    embed = Embed(
                        description=f'```{table.get_string()}```',
                        color=0xff0000,
                    )

                    if team['team_id'] == _round["round_stats"]["Winner"]:
                        embed.color = 0x00ff00

                    await channel.send(embed=embed)

        total_kills = 0
        total_headshot_perc = 0
        total_kd = 0
        total_kr = 0

        # Last 20 match stats
        for match in faceit_match_history['items']:
            print(f'Getting stats for mathc with id {match["match_id"]}')
            match_stats = self.faceit_api.get_match_stats(match['match_id'])
            if match_stats is not None:
                _round = match_stats['rounds'][0]
                for team in _round['teams']:
                    found_player = False

                    for player in team['players']:
                        if player['player_id'] == self.player_faceit_id:
                            found_player = True
                            total_kills += int(player['player_stats']['Kills'])
                            total_headshot_perc += int(player['player_stats']['Headshots %'])
                            total_kd += float(player['player_stats']['K/D Ratio'])
                            total_kr += float(player['player_stats']['K/R Ratio'])
                            break

                    if found_player:
                        break

        match_count = len(faceit_match_history['items'])

        stats_avrage_kills = round(total_kills / match_count)
        stats_avrage_headshot_perc = round(total_headshot_perc / match_count)
        stats_avrage_kd = round(total_kd / match_count, 1)
        stats_avrage_kr = round(total_kr / match_count, 1)

        embed = Embed(
            title='LAST 20 MATCHES STATISTICS',
            color=0xff5500,
        )

        embed.add_field(name='Avrage Kills', value=stats_avrage_kills, inline=True)
        embed.add_field(name='Avrage Headshot %', value=stats_avrage_headshot_perc, inline=True)
        embed.add_field(name='Avrage K/D', value=stats_avrage_kd, inline=True)
        embed.add_field(name='Avrage K/R', value=stats_avrage_kr, inline=True)

        await channel.send(embed=embed)
