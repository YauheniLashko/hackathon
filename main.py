import pygame
from random import randint

pygame.init()

pygame.time.set_timer(pygame.USEREVENT, 1500)

WIDTH = 1200
HEIGHT = 800
FPS = 60
RED = (255, 255, 255)
game_score = 0
print_score = pygame.font.Font(None, 70)
pygame.display.set_caption("COSMOS GAME")
WIN = True
mw = pygame.display.set_mode((WIDTH, HEIGHT))
space = pygame.image.load('picture/space.jpg').convert()
back = pygame.transform.scale(space, (WIDTH, HEIGHT))

clock = pygame.time.Clock()


class Hero(pygame.sprite.Sprite):
    def __init__(self, picture, speed, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(picture), (50, 50)).convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = x
        self.rect.y = y

    def fire(self):
        bullet = Bullet('picture/bullet.png', 10, self.rect.centerx, self.rect.top)
        bullets.add(bullet)


class Bullet(Hero):
    def __init__(self, picture, speed, x, y):
        super().__init__(picture, speed, x, y)
        self.image = pygame.transform.scale(pygame.image.load(picture), (10, 10)).convert_alpha()

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > HEIGHT:
            self.kill()


class Enemy(pygame.sprite.Sprite):

    def __init__(self, picture, speed, x, group):
        super().__init__()
        self.image = picture
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed
        self.add(group)

    def update(self):
        global WIN
        if self.rect.y < HEIGHT:
            self.rect.y += self.speed
        else:
            self.kill()
            create_enemy(enemies)
            WIN = False


def create_enemy(group):
    enemy_image = pygame.transform.scale(pygame.image.load('picture/alien.png'), (50, 50)).convert_alpha()
    x = randint(20, WIDTH - 20)
    speed = randint(3, 5)

    return Enemy(enemy_image, speed, x, group)


enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
spaceship = Hero('picture/spaceship.png', 10, WIDTH // 2, HEIGHT - 70)
create_enemy(enemies)
def stats():
    global game_score
    for enemy in enemies:
        for bullet in bullets:
            if enemy.rect.colliderect(bullet.rect):
                game_score += 100
while True:
    stats()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.USEREVENT:
            create_enemy(enemies)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spaceship.fire()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        spaceship.rect.x -= spaceship.speed
    elif keys[pygame.K_RIGHT]:
        spaceship.rect.x += spaceship.speed



    mw.blit(back, (0, 0))
    score_text = print_score.render(str(game_score), True, RED)
    mw.blit(score_text, (0,0))
    pygame.sprite.groupcollide(enemies, bullets, True, True)
    enemies.draw(mw)
    bullets.draw(mw)
    mw.blit(spaceship.image, spaceship.rect)


    clock.tick(FPS)

    enemies.update()
    bullets.update()
    if not WIN:
        mw.blit(pygame.transform.scale(pygame.image.load('picture/game_over.jpg'), (WIDTH, HEIGHT)), (0, 0))

    pygame.display.update()