    def draw_transparent_circle(self, surface, center, radius, color=(0, 0, 0, 128)):
        """
        Draw a 50% transparent black circle on the given Pygame surface.

        Parameters:
        - surface: Pygame surface to draw the circle on.
        - center: Tuple (x, y) representing the center of the circle.
        - radius: Radius of the circle.
        - color: Optional. The color and transparency of the circle. Default is 50% transparent black.
        """
        # Create a new surface with per-pixel alpha transparency
        transparent_surface = pygame.Surface(
            (radius*2, radius*2), pygame.SRCALPHA)

        # Draw the circle on the new transparent surface
        pygame.draw.circle(transparent_surface, color,
                           (radius, radius), radius)

        # Blit (copy) the transparent surface onto the main surface at the given center position
        # Adjust the blit position so that the circle is centered at the given center
        surface.blit(transparent_surface, (center[0]-radius, center[1]-radius))

    def draw(self, surface, game_manager):
        # draw the first marble
        if self.first_marble is not None:
            center = Board.get_circle_center(
                self.first_marble[0], self.first_marble[1])
            self.draw_transparent_circle(
                surface, center, 100, color=(255, 0, 0))
        if self.second_marble is not None:
            center = Board.get_circle_center(
                self.second_marble[0], self.second_marble[1])
            self.draw_transparent_circle(surface, center, 100)

        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(100, 100, 150, 100))
