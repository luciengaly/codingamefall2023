class GameSummaryManager:
    def __init__(self):
        self.lines = []
        self.players_errors = {}
        self.players_summary = {}

    def get_summary(self):
        return self.__str__()

    def clear(self):
        self.lines.clear()
        self.players_errors.clear()
        self.players_summary.clear()

    def to_string(self):
        return (
            self.format_errors()
            + "\n"
            + self.format_summary()
            + "\n"
            + "\n".join(self.lines)
        )

    def add_error(self, player, error):
        key = player.nickname_token
        if key not in self.players_errors:
            self.players_errors[key] = []
        self.players_errors[key].append(error)

    def add_player_summary(self, key, summary):
        if key not in self.players_summary:
            self.players_summary[key] = []
        self.players_summary[key].append(summary)

    def format_errors(self):
        return "\n".join(
            f"{player}: {errors[0]} + {len(errors) - 1} other error{'s' if len(errors) > 2 else ''}"
            for player, errors in self.players_errors.items()
        )

    def format_summary(self):
        return "\n".join(
            summary
            for summaries in self.players_summary.values()
            for summary in summaries
        )
