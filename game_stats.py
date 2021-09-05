class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start the game in an active state
        self.game_active = False


    def reset_stats(self):
        """Initialized statistics that can be changed during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
