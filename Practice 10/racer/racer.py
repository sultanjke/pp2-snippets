from __future__ import annotations

import random
from pathlib import Path

import pygame


WINDOW_WIDTH = 420
WINDOW_HEIGHT = 700

ROAD_LEFT = 70
ROAD_RIGHT = 350
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT

LANE_COUNT = 3
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT
LANE_CENTERS = [ROAD_LEFT + LANE_WIDTH // 2 + (i * LANE_WIDTH) for i in range(LANE_COUNT)]

PLAYER_SIZE = (56, 96)
ENEMY_SIZE = (56, 96)
COIN_SIZE = (30, 30)

FPS = 60


def create_fallback_car(size: tuple[int, int], color: tuple[int, int, int]) -> pygame.Surface:
    """Create a simple car shape if image loading fails."""
    surface = pygame.Surface(size, pygame.SRCALPHA)
    width, height = size

    # Car body
    pygame.draw.rect(surface, color, (6, 10, width - 12, height - 20), border_radius=14)
    # Windshield
    pygame.draw.rect(surface, (220, 235, 245), (12, 18, width - 24, 24), border_radius=8)
    # Wheels
    pygame.draw.rect(surface, (25, 25, 25), (2, 18, 6, 22), border_radius=3)
    pygame.draw.rect(surface, (25, 25, 25), (width - 8, 18, 6, 22), border_radius=3)
    pygame.draw.rect(surface, (25, 25, 25), (2, height - 40, 6, 22), border_radius=3)
    pygame.draw.rect(surface, (25, 25, 25), (width - 8, height - 40, 6, 22), border_radius=3)
    return surface


def create_fallback_coin(size: tuple[int, int]) -> pygame.Surface:
    """Create a simple coin circle if image loading fails."""
    surface = pygame.Surface(size, pygame.SRCALPHA)
    center = (size[0] // 2, size[1] // 2)
    radius = min(size) // 2 - 2
    pygame.draw.circle(surface, (245, 199, 45), center, radius)
    pygame.draw.circle(surface, (255, 235, 120), center, radius - 5)
    pygame.draw.circle(surface, (210, 150, 25), center, radius, 2)
    return surface


def create_fallback_road(size: tuple[int, int]) -> pygame.Surface:
    """Create a basic road background if road image loading fails."""
    width, height = size
    surface = pygame.Surface(size)
    surface.fill((48, 48, 54))

    # Lane separators
    for lane_line_x in (LANE_WIDTH, LANE_WIDTH * 2):
        for y in range(0, height, 90):
            pygame.draw.rect(surface, (245, 245, 245), (lane_line_x - 3, y, 6, 52), border_radius=2)

    # Road edge lines
    pygame.draw.rect(surface, (230, 220, 80), (0, 0, 6, height))
    pygame.draw.rect(surface, (230, 220, 80), (width - 6, 0, 6, height))
    return surface


def load_asset_image(
    path: Path,
    size: tuple[int, int],
    fallback_kind: str,
    fallback_color: tuple[int, int, int] = (200, 200, 200),
) -> pygame.Surface:
    """Load image from file, or return fallback shape if file is missing/broken."""
    if path.exists():
        try:
            image = pygame.image.load(str(path)).convert_alpha()
            return pygame.transform.smoothscale(image, size)
        except Exception:
            pass

    if fallback_kind == "car":
        return create_fallback_car(size, fallback_color)
    if fallback_kind == "coin":
        return create_fallback_coin(size)
    return create_fallback_road(size)


class Player(pygame.sprite.Sprite):
    """Player car controlled by left/right lane switching."""

    def __init__(self, image: pygame.Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midbottom=(LANE_CENTERS[1], WINDOW_HEIGHT - 22))
        self.lane_index = 1

    def move_left(self) -> None:
        if self.lane_index > 0:
            self.lane_index -= 1
            self.rect.centerx = LANE_CENTERS[self.lane_index]

    def move_right(self) -> None:
        if self.lane_index < len(LANE_CENTERS) - 1:
            self.lane_index += 1
            self.rect.centerx = LANE_CENTERS[self.lane_index]


class Enemy(pygame.sprite.Sprite):
    """Enemy car that moves downward and respawns from the top."""

    def __init__(self, image: pygame.Surface, speed: int):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = speed
        self.reset_position()

    def reset_position(self) -> None:
        self.rect.centerx = random.choice(LANE_CENTERS)
        self.rect.y = random.randint(-520, -130)

    def update_speed(self, speed: int) -> None:
        self.speed = speed

    def move(self) -> None:
        self.rect.y += self.speed
        if self.rect.top > WINDOW_HEIGHT:
            self.reset_position()


class Coin(pygame.sprite.Sprite):
    """Coin that appears randomly in lanes and moves down the road."""

    def __init__(self, image: pygame.Surface, speed: int):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.centerx = random.choice(LANE_CENTERS)
        self.rect.y = random.randint(-620, -120)

    def update_speed(self, speed: int) -> None:
        self.speed = speed

    def move(self) -> None:
        self.rect.y += self.speed
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()


class RacerGame:
    """Beginner-friendly racer game with enemy collisions and coin collection."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Practice 10 - Racer")

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont("arial", 32, bold=True)
        self.hud_font = pygame.font.SysFont("consolas", 26, bold=True)
        self.info_font = pygame.font.SysFont("arial", 20)

        assets_dir = Path(__file__).resolve().parent / "assets"
        self.road_image = load_asset_image(
            assets_dir / "road.png",
            (ROAD_WIDTH, WINDOW_HEIGHT),
            fallback_kind="road",
        )
        self.player_image = load_asset_image(
            assets_dir / "player_car.png",
            PLAYER_SIZE,
            fallback_kind="car",
            fallback_color=(40, 120, 255),
        )
        self.enemy_image = load_asset_image(
            assets_dir / "enemy_car.png",
            ENEMY_SIZE,
            fallback_kind="car",
            fallback_color=(225, 64, 64),
        )
        self.coin_image = load_asset_image(
            assets_dir / "coin.png",
            COIN_SIZE,
            fallback_kind="coin",
        )

        self.player = Player(self.player_image)
        self.enemy_speed = 5
        self.enemy = Enemy(self.enemy_image, self.enemy_speed)

        self.enemies = pygame.sprite.Group(self.enemy)
        self.coins = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player, self.enemy)

        self.coins_collected = 0
        self.road_scroll = 0
        self.game_over = False

        # Custom timed events: one for speed increase, one for random coin spawns.
        self.INC_SPEED = pygame.USEREVENT + 1
        self.SPAWN_COIN = pygame.USEREVENT + 2
        pygame.time.set_timer(self.INC_SPEED, 5000)
        pygame.time.set_timer(self.SPAWN_COIN, 1400)

    def reset_round(self) -> None:
        """Restart game state after game over."""
        self.game_over = False
        self.coins_collected = 0
        self.road_scroll = 0

        self.enemy_speed = 5
        self.enemy.update_speed(self.enemy_speed)
        self.enemy.reset_position()

        self.player.lane_index = 1
        self.player.rect.centerx = LANE_CENTERS[self.player.lane_index]
        self.player.rect.bottom = WINDOW_HEIGHT - 22

        # Remove all active coins from groups.
        for coin in list(self.coins):
            coin.kill()

    def spawn_coin(self) -> None:
        # Randomly skip some timer ticks so coins feel less predictable.
        if random.random() < 0.3:
            return
        coin = Coin(self.coin_image, self.enemy_speed + 1)
        self.coins.add(coin)
        self.all_sprites.add(coin)

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == self.INC_SPEED and not self.game_over:
                self.enemy_speed += 1
                self.enemy.update_speed(self.enemy_speed)
                for coin in self.coins:
                    coin.update_speed(self.enemy_speed + 1)

            if event.type == self.SPAWN_COIN and not self.game_over:
                self.spawn_coin()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                # After losing, allow restart with R.
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_round()
                    continue

                if event.key == pygame.K_LEFT:
                    self.player.move_left()
                if event.key == pygame.K_RIGHT:
                    self.player.move_right()

        return True

    def update_game(self) -> None:
        self.enemy.move()
        for coin in self.coins:
            coin.move()

        # Player loses when touching an enemy car.
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.game_over = True
            return

        # Count collected coins and remove them from the screen.
        collected_now = pygame.sprite.spritecollide(self.player, self.coins, dokill=True)
        if collected_now:
            self.coins_collected += len(collected_now)

    def draw_background(self) -> None:
        self.screen.fill((54, 153, 56))

        # Scroll road texture to create movement feeling.
        if not self.game_over:
            self.road_scroll = (self.road_scroll + self.enemy_speed) % WINDOW_HEIGHT
        self.screen.blit(self.road_image, (ROAD_LEFT, self.road_scroll - WINDOW_HEIGHT))
        self.screen.blit(self.road_image, (ROAD_LEFT, self.road_scroll))

    def draw_hud(self) -> None:
        title = self.title_font.render("RACER", True, (245, 245, 245))
        self.screen.blit(title, (16, 14))

        speed_text = self.hud_font.render(f"Speed: {self.enemy_speed}", True, (245, 245, 245))
        self.screen.blit(speed_text, (16, 56))

        # Requirement: show collected coins in top-right corner.
        coin_text = self.hud_font.render(f"Coins: {self.coins_collected}", True, (255, 230, 90))
        coin_rect = coin_text.get_rect(topright=(WINDOW_WIDTH - 16, 22))
        self.screen.blit(coin_text, coin_rect)

        controls = self.info_font.render("Left/Right = move lane, R = restart, Esc = quit", True, (235, 235, 235))
        self.screen.blit(controls, (16, WINDOW_HEIGHT - 34))

    def draw(self) -> None:
        self.draw_background()

        # Draw all sprites after road so cars/coins appear on top.
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect)

        self.draw_hud()

        if self.game_over:
            self.draw_game_over_overlay()

    def draw_game_over_overlay(self) -> None:
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 10, 10, 165))
        self.screen.blit(overlay, (0, 0))

        over_text = self.title_font.render("GAME OVER", True, (255, 255, 255))
        coins_text = self.hud_font.render(f"Coins collected: {self.coins_collected}", True, (255, 235, 120))
        restart_text = self.info_font.render("Press R to restart", True, (255, 255, 255))
        quit_text = self.info_font.render("Press Esc to quit", True, (255, 255, 255))

        self.screen.blit(over_text, over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 55)))
        self.screen.blit(coins_text, coins_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 5)))
        self.screen.blit(restart_text, restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 35)))
        self.screen.blit(quit_text, quit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)))

    def run(self) -> None:
        running = True

        while running:
            running = self.handle_events()
            if not running:
                break

            if not self.game_over:
                self.update_game()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()


def run_racer_game() -> None:
    game = RacerGame()
    game.run()
