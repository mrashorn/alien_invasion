class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (200, 200, 200)
        self.bullets_allowed = 8
        self.alien_bullet_color = (204, 0, 0)
        
        # Alien settings
        self.fleet_drop_speed = 10  # normally set to 5 or 10
        self.dt = 0.01 # how fast the alien shooter timer counts down

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 0.7
        self.bullet_speed = 1.5
        self.alien_speed = 0.2
        self.alien_bullet_speed = 0.5

        # fleet direction 1 represents right, -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50


    def increase_speed(self):
        """Increase speed settings and score values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale) # so we only get integers

        
