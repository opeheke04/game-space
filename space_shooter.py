import pygame
import random
import math

# =========================
# INISIALISASI
# =========================
pygame.init()

WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()

# =========================
# WARNA
# =========================
BLACK = (5, 5, 20)
WHITE = (255, 255, 255)
PURPLE = (180, 60, 255)
RED = (255, 70, 70)
BLUE = (80, 180, 255)
YELLOW = (255, 230, 80)

# =========================
# PESAWAT PEMAIN
# =========================
player_x = WIDTH // 2
player_y = HEIGHT - 60

player_speed = 6

# =========================
# PELURU
# =========================
bullets = []
bullet_speed = 9

# =========================
# MUSUH
# =========================
enemies = []

for i in range(8):
    enemies.append({
        "x": random.randint(30, WIDTH - 30),
        "y": random.randint(-500, -50),
        "speed": random.uniform(1.5, 3)
    })

# =========================
# PARTIKEL LEDAKAN
# =========================
particles = []

# =========================
# SCORE & NYAWA
# =========================
score = 0
lives = 3

font = pygame.font.Font(None, 28)
big_font = pygame.font.Font(None, 50)

# =========================
# FUNGSI PESAWAT
# =========================
def draw_player(x, y):

    points = [
        (x, y - 25),
        (x - 18, y + 20),
        (x, y + 10),
        (x + 18, y + 20)
    ]

    pygame.draw.polygon(screen, BLUE, points)
    pygame.draw.polygon(screen, WHITE, points, 2)

    # Api mesin
    pygame.draw.polygon(
        screen,
        YELLOW,
        [
            (x - 7, y + 15),
            (x, y + 32),
            (x + 7, y + 15)
        ]
    )

# =========================
# FUNGSI MUSUH
# =========================
def draw_enemy(x, y):

    points = [
        (x, y + 20),
        (x - 18, y - 10),
        (x + 18, y - 10)
    ]

    pygame.draw.polygon(screen, RED, points)
    pygame.draw.polygon(screen, (255, 180, 180), points, 2)

# =========================
# BINTANG
# =========================
stars = []

for i in range(80):
    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 3)
    ])

# =========================
# PARTIKEL LEDAKAN
# =========================
def explosion(x, y):

    for i in range(20):

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 5)

        particles.append({
            "x": x,
            "y": y,
            "dx": math.cos(angle) * speed,
            "dy": math.sin(angle) * speed,
            "life": 30
        })

# =========================
# GAME LOOP
# =========================
running = True

while running:

    clock.tick(60)

    # =========================
    # EVENT
    # =========================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Tembak dengan SPACE
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                bullets.append({
                    "x": player_x,
                    "y": player_y - 25
                })

    # =========================
    # INPUT
    # =========================
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed

    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Batas layar
    player_x = max(20, min(WIDTH - 20, player_x))

    # =========================
    # GERAK PELURU
    # =========================
    for bullet in bullets[:]:

        bullet["y"] -= bullet_speed

        if bullet["y"] < 0:
            bullets.remove(bullet)

    # =========================
    # GERAK MUSUH
    # =========================
    for enemy in enemies:

        enemy["y"] += enemy["speed"]

        if enemy["y"] > HEIGHT + 30:

            enemy["y"] = random.randint(-200, -50)
            enemy["x"] = random.randint(30, WIDTH - 30)

    # =========================
    # TABRAKAN PELURU & MUSUH
    # =========================
    for bullet in bullets[:]:

        for enemy in enemies:

            distance = math.sqrt(
                (bullet["x"] - enemy["x"]) ** 2 +
                (bullet["y"] - enemy["y"]) ** 2
            )

            if distance < 25:

                explosion(enemy["x"], enemy["y"])

                score += 1

                bullet["remove"] = True

                enemy["x"] = random.randint(30, WIDTH - 30)
                enemy["y"] = random.randint(-300, -50)

                break

    # Hapus peluru yang mengenai musuh
    bullets = [
        b for b in bullets
        if not b.get("remove", False)
    ]

    # =========================
    # TABRAKAN MUSUH & PEMAIN
    # =========================
    for enemy in enemies:

        distance = math.sqrt(
            (player_x - enemy["x"]) ** 2 +
            (player_y - enemy["y"]) ** 2
        )

        if distance < 35:

            lives -= 1

            explosion(player_x, player_y)

            enemy["x"] = random.randint(30, WIDTH - 30)
            enemy["y"] = random.randint(-300, -50)

    # =========================
    # UPDATE PARTIKEL
    # =========================
    for particle in particles[:]:

        particle["x"] += particle["dx"]
        particle["y"] += particle["dy"]

        particle["life"] -= 1

        if particle["life"] <= 0:
            particles.remove(particle)

    # =========================
    # GAMBAR BACKGROUND
    # =========================
    screen.fill(BLACK)

    # Bintang bergerak
    for star in stars:

        star[1] += star[2]

        if star[1] > HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH)

        pygame.draw.circle(
            screen,
            WHITE,
            (star[0], star[1]),
            1
        )

    # =========================
    # GAMBAR PELURU
    # =========================
    for bullet in bullets:

        pygame.draw.rect(
            screen,
            WHITE,
            (
                bullet["x"] - 2,
                bullet["y"],
                4,
                15
            )
        )

    # =========================
    # GAMBAR MUSUH
    # =========================
    for enemy in enemies:
        draw_enemy(enemy["x"], enemy["y"])

    # =========================
    # GAMBAR PESAWAT
    # =========================
    draw_player(player_x, player_y)

    # =========================
    # GAMBAR LEDAKAN
    # =========================
    for particle in particles:

        pygame.draw.circle(
            screen,
            RED,
            (
                int(particle["x"]),
                int(particle["y"])
            ),
            3
        )

    # =========================
    # SCORE
    # =========================
    score_text = font.render(
        f"SCORE: {score}",
        True,
        WHITE
    )

    screen.blit(score_text, (10, 10))

    # =========================
    # NYAWA
    # =========================
    lives_text = font.render(
        f"LIVES: {'♥ ' * lives}",
        True,
        (255, 80, 150)
    )

    screen.blit(
        lives_text,
        (WIDTH - 120, 10)
    )

    # =========================
    # GAME OVER
    # =========================
    if lives <= 0:

        game_over = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        screen.blit(
            game_over,
            (
                WIDTH // 2 - game_over.get_width() // 2,
                HEIGHT // 2 - 30
            )
        )

        pygame.display.update()

        pygame.time.delay(2000)

        running = False

    pygame.display.update()

pygame.quit()