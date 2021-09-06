class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start the game in an active state
        self.game_active = False

        # Read the high score file and set the high score.
        high_score_file = open("high_score.txt")
        high_score_text = high_score_file.read()
        self.high_score = int(high_score_text)
        high_score_file.close()
        # could write an exception here if the high score file is not a number
        # to make it just say 0 instead.



    def reset_stats(self):
        """Initialized statistics that can be changed during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1


    def write_high_score(self):
        """Writes the new high score to the high score file."""
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(self.score))
        high_score_file.close()

