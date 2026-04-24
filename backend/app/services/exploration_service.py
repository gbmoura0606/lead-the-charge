from collections import Counter
from datetime import datetime

from app.services.data_hub_service import get_matches, get_summoner


def _extract_participant(match: dict, puuid: str):
    participants = match.get('info', {}).get('participants', [])
    for participant in participants:
        if participant.get('puuid') == puuid:
            return participant
    return None


def _sort_by_game_end_desc(matches: list[dict]) -> list[dict]:
    return sorted(matches, key=lambda item: item.get('info', {}).get('gameEndTimestamp', 0), reverse=True)


def _legacy_row(match: dict) -> dict:
    return {
        'id': match.get('id'),
        'gameCreation': None,
        'gameEndTimestamp': None,
        'gameDuration': (match.get('duration_minutes') or 0) * 60,
        'queueId': None,
        'champion': match.get('champion'),
        'role': match.get('role'),
        'win': match.get('result') == 'Win',
        'kills': match.get('kills'),
        'deaths': match.get('deaths'),
        'assists': match.get('assists'),
    }


def list_matches() -> list[dict]:
    summoner_payload = get_summoner()
    puuid = summoner_payload.get('data', {}).get('puuid')

    compact = []
    for match in _sort_by_game_end_desc(get_matches()):
        if 'metadata' not in match:
            compact.append(_legacy_row(match))
            continue

        participant = _extract_participant(match, puuid) if puuid else None
        info = match.get('info', {})
        compact.append(
            {
                'id': match.get('metadata', {}).get('matchId'),
                'gameCreation': info.get('gameCreation'),
                'gameEndTimestamp': info.get('gameEndTimestamp'),
                'gameDuration': info.get('gameDuration'),
                'queueId': info.get('queueId'),
                'champion': participant.get('championName') if participant else None,
                'role': participant.get('teamPosition') if participant else None,
                'win': participant.get('win') if participant else None,
                'kills': participant.get('kills') if participant else None,
                'deaths': participant.get('deaths') if participant else None,
                'assists': participant.get('assists') if participant else None,
            }
        )

    return compact


def get_match_detail(match_id: str) -> dict | None:
    for match in get_matches():
        if match.get('metadata', {}).get('matchId') == match_id or match.get('id') == match_id:
            return match
    return None


def basic_stats() -> dict:
    rows = [row for row in list_matches() if row.get('id')]
    if not rows:
        return {
            'totalGames': 0,
            'wins': 0,
            'losses': 0,
            'winrate': 0.0,
            'averageKda': 0.0,
            'gamesOverTime': [],
            'winLossOverTime': [],
        }

    wins = sum(1 for row in rows if row.get('win'))
    total = len(rows)
    losses = total - wins
    average_kda = sum(
        ((row.get('kills') or 0) + (row.get('assists') or 0)) / max((row.get('deaths') or 0), 1)
        for row in rows
    ) / total

    games_per_day: Counter[str] = Counter()
    winloss_points = []

    for row in rows:
        ts = row.get('gameEndTimestamp') or row.get('gameCreation')
        if ts:
            day = datetime.utcfromtimestamp(ts / 1000).strftime('%Y-%m-%d')
        else:
            day = 'unknown'
        games_per_day[day] += 1
        winloss_points.append({'date': day, 'win': bool(row.get('win'))})

    return {
        'totalGames': total,
        'wins': wins,
        'losses': losses,
        'winrate': round((wins / total) * 100, 1),
        'averageKda': round(average_kda, 2),
        'gamesOverTime': [{'date': date, 'games': count} for date, count in sorted(games_per_day.items())],
        'winLossOverTime': winloss_points,
    }


def champion_stats() -> list[dict]:
    rows = [row for row in list_matches() if row.get('champion')]
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        grouped.setdefault(row['champion'], []).append(row)

    response = []
    for champion, entries in grouped.items():
        games = len(entries)
        wins = sum(1 for entry in entries if entry.get('win'))
        response.append(
            {
                'champion': champion,
                'games': games,
                'wins': wins,
                'winrate': round((wins / games) * 100, 1),
            }
        )

    return sorted(response, key=lambda item: item['games'], reverse=True)
