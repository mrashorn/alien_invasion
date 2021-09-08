from alien import Alien
import pygame

# Try to use the super().__init__() of alien
class ShooterAlien(Alien):
    """A class to represent an alien that shoots bullets towards the ship."""
    def __init__(self, ai_game):
        """Initialize shooter alien and inherit the attributes from Alien and Sprite."""
        super().__init__(ai_game)

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/shooting_alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left. 
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

        # Can the alien shoot back at the player?
        self.can_shoot = True





        
