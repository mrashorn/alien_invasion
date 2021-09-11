import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    """A class to manage bullets fired from the aliens."""

    def __init__(self, ai_game, shooter_x, shooter_y, shooter_width, shooter_height):
        """Create a bullet object at a shooter alien's position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.alien_bullet_color

        # Create an alien bullet at (0, 0) then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                self.settings.bullet_height)
        self.rect.midtop = (shooter_x + shooter_width/2, shooter_y + shooter_height/2)

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    
    def update(self):
        """Move the bullet down the screen."""
        # update the decimal position of the bullet
        self.y += self.settings.alien_bullet_speed
        # update the rect position
        self.rect.y = self.y

    
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
