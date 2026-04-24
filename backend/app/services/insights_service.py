from app.models.match import Match


_WIN_RESULT = "Win"


def generate_insights(matches: list[Match]) -> list[str]:
    insights: list[str] = []

    if not matches:
        return ["No matches available to generate insights."]

    by_champion: dict[str, list[Match]] = {}
    for match in matches:
        by_champion.setdefault(match.champion, []).append(match)

    best_champion = None
    best_champion_wr = -1.0
    for champion, entries in by_champion.items():
        if len(entries) < 2:
            continue
        wins = sum(1 for entry in entries if entry.result == _WIN_RESULT)
        winrate = wins / len(entries)
        if winrate > best_champion_wr:
            best_champion = champion
            best_champion_wr = winrate

    if best_champion:
        insights.append(
            f"You perform best on {best_champion} with {best_champion_wr * 100:.1f}% winrate in your recent sample."
        )

    win_deaths = [match.deaths for match in matches if match.result == _WIN_RESULT]
    loss_deaths = [match.deaths for match in matches if match.result != _WIN_RESULT]
    if win_deaths and loss_deaths:
        avg_win_deaths = sum(win_deaths) / len(win_deaths)
        avg_loss_deaths = sum(loss_deaths) / len(loss_deaths)
        if avg_loss_deaths - avg_win_deaths >= 2:
            insights.append(
                f"Your deaths are significantly higher in losses ({avg_loss_deaths:.1f}) than wins ({avg_win_deaths:.1f})."
            )

    short_games = [match for match in matches if match.duration_minutes <= 32]
    long_games = [match for match in matches if match.duration_minutes > 32]
    if short_games and long_games:
        short_winrate = sum(1 for match in short_games if match.result == _WIN_RESULT) / len(short_games)
        long_winrate = sum(1 for match in long_games if match.result == _WIN_RESULT) / len(long_games)
        if short_winrate - long_winrate >= 0.15:
            insights.append(
                f"Your winrate drops in longer games: {short_winrate * 100:.1f}% in short games vs {long_winrate * 100:.1f}% in long games."
            )

    if not insights:
        insights.append("Performance is stable; gather more games for stronger trend detection.")

    return insights
