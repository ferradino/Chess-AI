from const import *
import pygame
pygame.init()

# Create window and title
window = pygame.display.set_mode((WIDTH, HEIGHT))
window.fill(BLACK)
pygame.display.set_caption("Chess")

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)
        # Check if user clicked the exit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        pygame.display.update()


if __name__ == "__main__":
    main()