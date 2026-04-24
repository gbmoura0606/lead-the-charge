import os
import time
from typing import Any

import httpx


class RiotApiService:
    def __init__(self):
        self.api_key = os.getenv("RIOT_API_KEY", "")
        self.platform_region = os.getenv("RIOT_PLATFORM_REGION", "euw1")
        self.match_region = os.getenv("RIOT_MATCH_REGION", "europe")
        self.game_name = os.getenv("RIOT_GAME_NAME", "wave culture")
        self.tag_line = os.getenv("RIOT_TAG_LINE", "EUW")
        self.max_matches = int(os.getenv("RIOT_MATCH_COUNT", "20"))
        self.request_pause_seconds = float(os.getenv("RIOT_REQUEST_PAUSE_SECONDS", "0.15"))

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def _headers(self) -> dict[str, str]:
        return {"X-Riot-Token": self.api_key}

    def _get(self, url: str, params: dict[str, Any] | None = None) -> Any:
        with httpx.Client(timeout=20) as client:
            response = client.get(url, headers=self._headers(), params=params)
            response.raise_for_status()
            payload = response.json()

        time.sleep(self.request_pause_seconds)
        return payload

    def fetch_account(self) -> dict[str, Any]:
        url = (
            f"https://{self.match_region}.api.riotgames.com/riot/account/v1/accounts"
            f"/by-riot-id/{self.game_name}/{self.tag_line}"
        )
        return self._get(url)

    def fetch_summoner(self, puuid: str) -> dict[str, Any]:
        url = f"https://{self.platform_region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
        return self._get(url)

    def fetch_match_ids(self, puuid: str) -> list[str]:
        url = f"https://{self.match_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        return self._get(url, params={"start": 0, "count": self.max_matches})

    def fetch_match_details(self, match_id: str) -> dict[str, Any]:
        url = f"https://{self.match_region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        return self._get(url)
