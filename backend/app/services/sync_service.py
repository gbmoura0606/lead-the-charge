from app.services.data_hub_service import get_matches, save_summoner, upsert_match
from app.services.riot_api_service import RiotApiService


class SyncService:
    def __init__(self):
        self.riot = RiotApiService()

    def sync(self) -> dict:
        if not self.riot.configured:
            return {
                "ok": False,
                "message": "RIOT_API_KEY is not set. Add it to your environment before syncing.",
                "fetched": 0,
            }

        account = self.riot.fetch_account()
        puuid = account.get("puuid")
        summoner = self.riot.fetch_summoner(puuid)

        save_summoner({"account": account, "summoner": summoner, "puuid": puuid})

        existing_ids = {
            match.get("metadata", {}).get("matchId")
            for match in get_matches()
            if match.get("metadata", {}).get("matchId")
        }

        fetched = 0
        for match_id in self.riot.fetch_match_ids(puuid):
            if match_id in existing_ids:
                continue
            detail = self.riot.fetch_match_details(match_id)
            upsert_match(detail)
            fetched += 1

        return {
            "ok": True,
            "message": "Sync completed",
            "fetched": fetched,
        }
