import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from bullet_alien import AlienBullet 
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from random import randint
from random import uniform
from shooter import ShooterAlien


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store the game stats.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.shooters = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()

        # Make the play button
        self.play_button = Button(self, "Play")

        
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_alien_bullets()

                if self.shooters:
                    self._update_alien_timer()

            self._update_screen()
        

    def _check_events(self):
        """Respond to keyboard and mouse presses."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game statistics
            self.settings.initialize_dynamic_settings()
            self._start_game()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

        

    def _start_game(self):
        """Start a new game."""
        # Reset the game statistics
        self.stats.reset_stats()
        self.stats.game_active = True

        # Get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        # Create the new fleet and center the ship. 
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Create the alien bullet timer
        self._reset_alien_timer()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            if self.sb.write_high_score:
                self.stats.write_high_score()
            sys.exit() # Exits the game with q key press.
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._start_game() # Start the game with 'p' press.


    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

        self._check_bullet_collisions()


    def _check_bullet_collisions(self):
        """Respond to bullet-alien collisions."""

        # Check for any bullets that have hit aliens
        # If so, delete both bullet and alien
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()

        # Repopulate alien fleet once all are killed.
        if not self.aliens:
            # Increase the level
            self.stats.level += 1
            self.sb.prep_level()

            self.bullets.empty() # Destroy existing bullets
            self._create_fleet()
            self.settings.increase_speed()

                
    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()


        # Look for alien-ship collisions. 
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            print("Ship hit!!")

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()


    def _ship_hit(self):
        """Respond to the ship getting hit by an alien."""

        if self.stats.ships_left > 0:
            # Decrement the number of ships left and update the scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(1)
        else: 
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _update_alien_timer(self):
        """Increment the remaining time until another alien shoots."""
        self.alien_timer -= self.settings.dt

        if self.alien_timer <= 0:
            print("Timer zero.")
            self._fire_alien_bullet()
            self._reset_alien_timer() 


    def _fire_alien_bullet(self):
        """Fire a single bullet from a random shooter alien."""
        # First choose a random shooter alien to shoot from. 
        for shooter in self.shooters:
            print("Alien shoots bullet.")
            new_bullet = AlienBullet(self, shooter.rect.x, shooter.rect.y,
                    shooter.rect.width, shooter.rect.height)
            self.alien_bullets.add(new_bullet)


    def _update_alien_bullets(self):
        """Update the positions of the alien bullets and get rid of old bullets."""
        self.alien_bullets.update()

        # Get rid of bullets off screen
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)


    def _reset_alien_timer(self):
        """Reset the alien shooting countdown."""
        self.alien_timer = uniform(2, 20)


    def _check_aliens_bottom(self):
        """Check to see if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship was hit.
                self._ship_hit()
                print("An alien reached the bottom of the screen!")
                break



    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row. 
        # Spacing between each is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height
            ) - ship_height)
        number_rows = (available_space_y // (2 * alien_height)) - 1 

        # Create a limit for the number of rows and columns based on what level
        if self.stats.level <= number_rows:
            number_rows = self.stats.level

        # Create full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

        # Loop to add any shooter aliens to their own shooter group.
        for alien in self.aliens:
            if alien.can_shoot == True:
                self.shooters.add(alien)


        
    def _create_alien(self, alien_number, row_number):
        # Create an alien or shooter alien (1 in 10) and place it in row.
        if(randint(1, 10)) == 1:
            alien = ShooterAlien(self)
        else:
            alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2*alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2*alien_height * row_number
        self.aliens.add(alien)


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet down and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
        """Updates images on screen, flip to new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        
        # Draw all bullets to screen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Draw the scoreboard
        self.sb.show_score()

        # Draw the play button if the game is inactive. 
        if not self.stats.game_active:
            self.play_button.draw_button()


        pygame.display.flip()
          
        
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
