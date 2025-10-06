import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height, winning_score=5):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100
        self.winning_score = winning_score

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Move the ball first
        self.ball.move()

        # ✅ Immediately check for collision right after movement
        if self.ball.rect().colliderect(self.player.rect()) or self.ball.rect().colliderect(self.ai.rect()):
            self.ball.velocity_x *= -1

            # Optional: small position correction to prevent sticking
            if self.ball.velocity_x > 0:  # moving right
                self.ball.x = self.player.x + self.player.width
            else:  # moving left
                self.ball.x = self.ai.x - self.ball.width

        # Check for scoring (ball out of bounds)
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        # Update AI paddle position
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            winner = "Player Wins!" if self.player_score >= self.winning_score else "AI Wins!"

            # Display winner
            screen.fill((0, 0, 0))
            game_over_text = self.font.render(winner, True, (255, 255, 255))
            prompt_text = self.font.render("Press 3, 5, 7 for Best Of | ESC to Exit", True, (200, 200, 200))

            screen.blit(game_over_text, game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 40)))
            screen.blit(prompt_text, prompt_text.get_rect(center=(self.width // 2, self.height // 2 + 40)))
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
                        elif event.key in [pygame.K_3, pygame.K_5, pygame.K_7]:
                            # Reset scores and update target
                            if event.key == pygame.K_3:
                                self.winning_score = 2  # Best of 3 → 2 wins
                            elif event.key == pygame.K_5:
                                self.winning_score = 3  # Best of 5 → 3 wins
                            elif event.key == pygame.K_7:
                                self.winning_score = 4  # Best of 7 → 4 wins

                            self.player_score = 0
                            self.ai_score = 0
                            self.ball.reset()
                            waiting = False
