from collections import defaultdict

from app.models.match import Match
from app.models.stats import ChampionStats, RoleStats, StatsResponse, SummaryStats


_WIN_RESULT = "Win"


def calculate_kda(match: Match) -> float:
    return (match.kills + match.assists) / max(match.deaths, 1)


def _build_champion_stats(groups: dict[str, list[Match]]) -> list[ChampionStats]:
    rows: list[ChampionStats] = []
    for champion, entries in groups.items():
        games = len(entries)
        wins = sum(1 for match in entries if match.result == _WIN_RESULT)
        rows.append(
            ChampionStats(
                champion=champion,
                games=games,
                wins=wins,
                winrate=round((wins / games) * 100, 1) if games else 0.0,
                average_kda=round(sum(calculate_kda(match) for match in entries) / games, 2) if games else 0.0,
            )
        )
    return sorted(rows, key=lambda item: item.games, reverse=True)


def _build_role_stats(groups: dict[str, list[Match]]) -> list[RoleStats]:
    rows: list[RoleStats] = []
    for role, entries in groups.items():
        games = len(entries)
        wins = sum(1 for match in entries if match.result == _WIN_RESULT)
        rows.append(
            RoleStats(
                role=role,
                games=games,
                wins=wins,
                winrate=round((wins / games) * 100, 1) if games else 0.0,
                average_kda=round(sum(calculate_kda(match) for match in entries) / games, 2) if games else 0.0,
            )
        )
    return sorted(rows, key=lambda item: item.games, reverse=True)


def calculate_stats(matches: list[Match]) -> StatsResponse:
    total_games = len(matches)
    wins = sum(1 for match in matches if match.result == _WIN_RESULT)
    losses = total_games - wins
    winrate = round((wins / total_games) * 100, 1) if total_games else 0.0
    average_kda = round(sum(calculate_kda(match) for match in matches) / total_games, 2) if total_games else 0.0

    champion_groups: dict[str, list[Match]] = defaultdict(list)
    role_groups: dict[str, list[Match]] = defaultdict(list)

    for match in matches:
        champion_groups[match.champion].append(match)
        role_groups[match.role].append(match)

    return StatsResponse(
        summary=SummaryStats(
            total_games=total_games,
            wins=wins,
            losses=losses,
            winrate=winrate,
            average_kda=average_kda,
        ),
        champion_performance=_build_champion_stats(champion_groups),
        role_performance=_build_role_stats(role_groups),
    )
