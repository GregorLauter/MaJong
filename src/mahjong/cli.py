"""Small terminal interface; all settlement rules live in the engine."""

from .engine import MahjongGame, validate_hand_value


def get_players() -> list[str]:
    players = []
    print("Enter players in initial East/South/West/North seating order.")
    for wind in ("East", "South", "West", "North"):
        while True:
            name = input(f"{wind}: ").strip()
            if not name:
                print("Player names must be non-empty.")
            elif name in players:
                print("Player names must be unique.")
            else:
                players.append(name)
                break
    return players


def get_score(player: str) -> int:
    while True:
        try:
            value = int(input(f"Hand value for {player}: "))
        except ValueError:
            print("Please enter a whole number.")
            continue
        try:
            validate_hand_value(player, value)
        except ValueError as error:
            print(error)
            continue
        return value


def get_winner(players: tuple[str, ...]) -> str:
    for number, player in enumerate(players, 1):
        print(f"{number}. {player}")
    while True:
        try:
            number = int(input("Who won? [1-4]: "))
            if 1 <= number <= 4:
                return players[number - 1]
        except ValueError:
            pass
        print("Please enter a number from 1 to 4.")


def show_scores(label: str, scores: dict[str, int]) -> None:
    print(f"\n{label}")
    for player, value in scores.items():
        print(f"{player}: {value:+d}")
    print(f"Control sum: {sum(scores.values())}")


def main() -> None:
    print("CLASSICAL CHINESE MAHJONG CALCULATOR")
    print(
        "Press Ctrl-C or Ctrl-D to finish. Only completed rounds are counted."
    )
    game = None
    try:
        game = MahjongGame(get_players())
        while True:
            print(f"\nROUND {game.round_number + 1}")
            print(f"Current East: {game.east}")
            print(f"East win streak: {game.east_win_streak}/4")
            scores = {player: get_score(player) for player in game.players}
            winner = get_winner(game.players)
            try:
                result = game.play_round(scores, winner)
            except ValueError as error:
                print(f"Invalid round: {error} Re-enter this round.")
                continue
            show_scores("ROUND CHANGES", result["changes"])
            show_scores("CUMULATIVE TOTALS", result["totals"])
            print(f"Next East: {game.east}")
            if input("Play another round? [Y/n]: ").strip().lower() in (
                "n",
                "no",
            ):
                break
    except (EOFError, KeyboardInterrupt):
        print("\nGame ended.")
    if game is not None:
        show_scores("FINAL TOTALS", game.totals)


if __name__ == "__main__":
    main()
