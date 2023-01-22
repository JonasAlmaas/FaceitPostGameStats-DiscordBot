import requests

FACEIT_API_URL = 'https://open.faceit.com/data/v4/'


class FaceitAPI:
    """ Faceit API wrapper class """

    def __init__(self, api_key: str, player_id: str, number_of_matches: int):
        self.api_key = api_key
        self.player_id = player_id
        self.number_of_matches = number_of_matches

    def get(self, url: str) -> requests.Response:
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }
        full_url = f'{FACEIT_API_URL}{url}'
        return requests.get(full_url, headers=headers)

    def get_player_history(self) -> dict | None:
        response = self.get(f'players/{self.player_id}/history?game=csgo&limit={self.number_of_matches}')

        if response.status_code != 200:
            print(f'Error while getting player history: {response.text}')
            return

        return response.json()
        # return MatchHistory(**response.json())

    def get_player_info(self) -> dict | None:
        response = self.get(f'players/{self.player_id}')

        if response.status_code != 200:
            print(f'Error while getting player info: {response.text}')
            return

        return response.json()

    def get_match_stats(self, match_id) -> dict | None:
        response = self.get(f'matches/{match_id}/stats')

        if response.status_code != 200:
            print(f'Error while getting match stats: {response.text}')
            return

        return response.json()
