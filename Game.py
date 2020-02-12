import random
import datetime
import pygame
import sys
import Loader
from Asteroid_big import Asteroid_big
from Asteroid_medium import Asteroid_medium
from Asteroid_small import Asteroid_small
from Deus_ex import Deus_ex
from Player import Player
import Menu
import math
import time
import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
import Menu
import Howmany
import threading
import Loader
from threading import Timer


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    START = 2
    ONEPL = 3
    TWOPL = 4
    THREEPL = 5
    FOURPL = 6


screen_size = [1280, 720]
level = 1
eex = 0

# Korekcija ugla
def correct_angle_minus(angle):
    new_direction = [0, 0]
    deg_angle = math.degrees(angle)
    new_direction[0] = math.cos(angle - math.radians(random.randint(0, 20)))
    new_direction[1] = -math.sin(angle - math.radians(random.randint(0, 20)))

    return new_direction

# Korekcija ugla
def correct_angle_plus(angle):
    # corrects angle to be +45deg
    new_direction = [0, 0]

    new_direction[0] = math.cos(angle + math.radians(random.randint(0, 20)))
    new_direction[1] = -math.sin(angle + math.radians(random.randint(0, 20)))

    return new_direction

# Učitavanje asteroida u listu i vracanje popunjene liste
def load_asteroids(number):
    asteroids = []
    for x in range(number):
        new_asteroid = spawn_asteroid()
        asteroids.append(new_asteroid)
    return asteroids

# Spavnovanje asteroida na ekranu
def spawn_asteroid():
    position = random.randint(1, 2)
    x_pos = 0
    y_pos = 0
    if position == 1:
        x_pos = -50
        y_pos = random.randint(0, screen_size[1] - 1)
    elif position == 2:
        x_pos = random.randint(0, screen_size[0] - 1)
        y_pos = -50
    asteroid = Asteroid_big([x_pos, y_pos], screen_size, random.uniform(1 + math.log(level), 1.2 + math.log(level)),
                            [random.uniform(-1, 1),
                             random.uniform(-1, 1)])
    return asteroid

# Spavnovanje Deus Ex-a sa specificinim koordinatama
def spawn_deus_ex(randx, randy):
    deus_ex = Deus_ex([randx, randy])
    return deus_ex

# Spavnovanje Deus Ex-a sa random koordinatama
def spawn_random_deus_ex():
    randx = random.randint(26, 1254)
    randy = random.randint(26, 694)
    deus_ex = spawn_deus_ex(randx, randy)
    return deus_ex


class AsteroidsGame:
    UPDATE = pygame.USEREVENT

    def __init__(self):
        self.init_pygame()
        self.setup_screen()
        self.clock = pygame.time.Clock()
        self.clock1 = pygame.time.Clock()
        self.players = []
        self.lock = threading.Lock()
        self.igraca = Howmany.igraci
        self.scoreboard_active = 0
        if self.igraca == 1:
            self.players.append(Player((screen_size[0] // 2, screen_size[1] // 2), screen_size, "Player 1", 1))
        elif self.igraca == 2:
            self.players.append(Player((screen_size[0] // 2, screen_size[1] // 2), screen_size, "Player 1", 1))
            self.players.append(Player((screen_size[0] // 2, screen_size[1] // 2), screen_size, "Player 2", 2))
        elif self.igraca == 3:
            self.players.append(Player((screen_size[0] // 2, screen_size[1] // 2), screen_size, "Player 1", 1))
            self.players.append(Player((screen_size[0] // 2, screen_size[1] // 2), screen_size, "Player 2", 2))
            self.players.append(Player((screen_size[0] // 2, screen_size[1] // 2), screen_size, "Player 3", 3))
        elif self.igraca == 4:
            self.players.append(Player((screen_size[0] // 2, screen_size[1] // 2), screen_size, "Player 1", 1))
            self.players.append(Player((screen_size[0] // 2, screen_size[1] // 2), screen_size, "Player 2", 2))
            self.players.append(Player((screen_size[0] // 2, screen_size[1] // 2), screen_size, "Player 3", 3))
            self.players.append(Player((screen_size[0] // 2, screen_size[1] // 2), screen_size, "Player 4", 4))

        self.asteroids = load_asteroids(2)
        self.deus_ex = []
        self.deus_ex.append(spawn_random_deus_ex())
        # self.active_bullets = []
        self.fire_time = []
        self.fire_time.append(datetime.datetime.now())
        self.fire_time.append(datetime.datetime.now())
        self.fire_time.append(datetime.datetime.now())
        self.fire_time.append(datetime.datetime.now())
        self._draw_threaded()

    def init_pygame(self):
        fps = 60
        pygame.time.set_timer(self.UPDATE, 1000 // fps)

        pygame.init()

    def setup_screen(self):
        self.screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
        pygame.display.set_caption("Asteroids")
        self.image = Loader.load_image("Background.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [0, 0]
        self.backgroundcolor = 255, 255, 255

    def _draw_threaded(self):
        self.drawer_thread = threading.Thread(target=self.draw)
        self.drawer_thread.daemon = True
        self.drawer_thread.start()

    # F-ja za crtanje na ekran
    def draw(self):

        while self.scoreboard_active != 1:
            self.screen.fill(self.backgroundcolor)
            self.screen.blit(self.image, self.rect)
            self.lock.acquire()
            for player in self.players:
                player.draw_on_screen(self.screen)
            # ova linija crta hitbox igraca
            # pygame.draw.rect(self.screen, (255, 0, 0), self.player.hitbox, 2)
            self.draw_all_asteroids()
            self.draw_all_bullets()
            self.draw_deus_ex()
            # ispisivanje nivoa
            pygame.font.init()
            myfont = pygame.font.SysFont('Arial', 30)
            textsurface = myfont.render('Level: ' + str(level), False, (0, 0, 0), (255, 255, 255))
            self.screen.blit(textsurface, (600, 5))

            if self.does_player_exist(1):
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 28)
                textsurface = myfont.render('Player: ' + str(next((x for x in self.players if x.id == 1), None).name),
                                            False, (0, 0, 0),
                                            next((x for x in self.players if x.id == 1), None).color)
                self.screen.blit(textsurface, (5, 5))
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 25)
                textsurface = myfont.render('Score: ' + str(next((x for x in self.players if x.id == 1), None).score),
                                            False, (0, 0, 0),
                                            next((x for x in self.players if x.id == 1), None).color)
                self.screen.blit(textsurface, (5, 55))
                lives = pygame.font.SysFont('Arial', 23)
                textsurl = lives.render('Lives: ' + str(next((x for x in self.players if x.id == 1), None).lives),
                                        False, (0, 0, 0), next((x for x in self.players if x.id == 1), None).color)
                self.screen.blit(textsurl, (5, 105))

            if self.does_player_exist(2):
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 28)
                textsurface = myfont.render('Player: ' + str(next((x for x in self.players if x.id == 2), None).name),
                                            False, (0, 0, 0),
                                            next((x for x in self.players if x.id == 2), None).color)
                self.screen.blit(textsurface, (screen_size[0] - 160, 5))
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 25)
                textsurface = myfont.render('Score: ' + str(next((x for x in self.players if x.id == 2), None).score),
                                            False, (0, 0, 0),
                                            next((x for x in self.players if x.id == 2), None).color)
                self.screen.blit(textsurface, (screen_size[0] - 160, 55))
                lives = pygame.font.SysFont('Arial', 23)
                textsurl = lives.render('Lives: ' + str(next((x for x in self.players if x.id == 2), None).lives),
                                        False, (0, 0, 0), next((x for x in self.players if x.id == 2), None).color)
                self.screen.blit(textsurl, (screen_size[0] - 160, 105))

            if self.does_player_exist(3):
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 28)
                textsurface = myfont.render('Player: ' + str(next((x for x in self.players if x.id == 3), None).name),
                                            False, (0, 0, 0),
                                            next((x for x in self.players if x.id == 3), None).color)
                self.screen.blit(textsurface, (5, screen_size[1] - 40))
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 25)
                textsurface = myfont.render('Score: ' + str(next((x for x in self.players if x.id == 3), None).score),
                                            False, (0, 0, 0),
                                            next((x for x in self.players if x.id == 3), None).color)
                self.screen.blit(textsurface, (5, screen_size[1] - 90))
                lives = pygame.font.SysFont('Arial', 23)
                textsurl = lives.render('Lives: ' + str(next((x for x in self.players if x.id == 3), None).lives),
                                        False, (0, 0, 0), next((x for x in self.players if x.id == 3), None).color)
                self.screen.blit(textsurl, (5, screen_size[1] - 140))

            if self.does_player_exist(4):
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 28)
                textsurface = myfont.render('Player: ' + str(next((x for x in self.players if x.id == 4), None).name),
                                            False, (0, 0, 0),
                                            next((x for x in self.players if x.id == 4), None).color)
                self.screen.blit(textsurface, (screen_size[0] - 140, screen_size[1] - 40))
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 25)
                textsurface = myfont.render('Score: ' + str(next((x for x in self.players if x.id == 4), None).score),
                                            False, (0, 0, 0),
                                            next((x for x in self.players if x.id == 4), None).color)
                self.screen.blit(textsurface, (screen_size[0] - 140, screen_size[1] - 90))
                lives = pygame.font.SysFont('Arial', 23)
                textsurl = lives.render('Lives: ' + str(next((x for x in self.players if x.id == 4), None).lives),
                                        False, (0, 0, 0), next((x for x in self.players if x.id == 4), None).color)
                self.screen.blit(textsurl, (screen_size[0] - 140, screen_size[1] - 140))
            pygame.display.flip()
            self.lock.release()
            self.clock.tick(120)
    # Crtanje metaka
    def draw_all_bullets(self):  # added
        for player in self.players:
            if len(player.bullets) > 0:
                for bullet in player.bullets:
                    bullet.draw_on_screen(self.screen)
                    # ova linija crta hitbox metka but dont use it!
                    # pygame.draw.rect(self.screen, (255, 0, 0), bullet.hitbox, 2)
    # Crtanje asteroida
    def draw_all_asteroids(self):
        for asteroid in self.asteroids:
            asteroid.draw_on_screen(self.screen)
            # ova linija crta hitboxove asteroida
            # pygame.draw.rect(self.screen, (255, 0, 0), asteroid.hitbox, 2)
    # Crtanje Deus Ex-a
    def draw_deus_ex(self):
        for deus_ex in self.deus_ex:
            deus_ex.draw_on(self.screen)
    # Provera da li je prošlo 2 sekunde od stvaranje Deus Ex-a, ako jeste aktivira se njeno dejstvo
    def check_deus_ex(self):
        for deus_ex in self.deus_ex:
            deus_ex.now = time.time()
            if deus_ex.now > deus_ex.future:
                deus_ex.transform()

    # Provera da li je player u godmode-u (Dobija godmode kad umre i traje 2 sekunde)
    def check_player_godmode(self):
        for player in self.players:
            player.now = time.time()
            if player.now > player.future:
                if player.godmode == 1:
                    player.godmode = 0

    # F-ja za simulaciju pomeranja asteroida i metaka
    def move_entities(self):
        for player in self.players:
            player.move()
            if len(player.bullets) > 0:
                for bullet in player.bullets:
                    bullet.move()
            for asteroid in self.asteroids:
                asteroid.move()

    # F-ja za skaliranje sa nivoom
    def level_up(self):
        global level
        level = level + 1
        deus_ex = spawn_random_deus_ex()
        self.deus_ex.append(deus_ex)
        self.asteroids = load_asteroids(1 + level)
        for player in self.players:
            player.max_speed = player.max_speed * 1.2
            player.score += 1000

    # F-ja za proveravanje pogotka i koji igrač je pogodio
    def hits(self):

        for player in self.players:
            bullets_to_remove = []
            asteroids_to_add = []
            asteroids_to_remove = []
            score_to_add = 0
            for bullet in player.bullets:
                for ast in self.asteroids:
                    if ast.hitbox[1] + ast.hitbox[3] > bullet.direction_xy[1] > ast.hitbox[1]:
                        if ast.hitbox[0] < bullet.direction_xy[0] < ast.hitbox[0] + ast.hitbox[2]:
                            print('hit')

                            bullets_to_remove.append(bullet)
                            asteroids_to_remove.append(ast)
                            if ast.asteroid_type == "big":
                                angle_of_asteroid = math.atan2(ast.direction_xy[1], ast.direction_xy[0])
                                angle_in_degs = math.degrees(angle_of_asteroid)
                                corrected_angle = math.radians((-angle_in_degs) % 360)
                                new_direction_plus = correct_angle_plus(corrected_angle)
                                new_direction_minus = correct_angle_minus(corrected_angle)

                                asteroid1 = Asteroid_medium([ast.position[0] + 10, ast.position[1] + 10], screen_size,
                                                            ast.speed, new_direction_plus)
                                asteroid2 = Asteroid_medium([ast.position[0] - 10, ast.position[1] - 10], screen_size,
                                                            ast.speed,
                                                            new_direction_minus)

                                # asteroids_to_add.append(asteroid1)
                                t = Timer(1, asteroids_to_add.append(asteroid1))
                                t.start()

                                asteroids_to_add.append(asteroid2)
                                # t = Timer(0.3, asteroids_to_add.append(asteroid2))
                                # t.start()

                            if ast.asteroid_type == "medium":
                                angle_of_asteroid = math.atan2(ast.direction_xy[1], ast.direction_xy[0])
                                angle_in_degs = math.degrees(angle_of_asteroid)
                                corrected_angle = math.radians((-angle_in_degs) % 360)
                                new_direction_plus = correct_angle_plus(corrected_angle)
                                new_direction_minus = correct_angle_minus(corrected_angle)

                                asteroid1 = Asteroid_small([ast.position[0] + 7, ast.position[1] + 7], screen_size,
                                                           ast.speed, new_direction_plus)
                                asteroid2 = Asteroid_small([ast.position[0] - 7, ast.position[1] - 7], screen_size,
                                                           ast.speed,
                                                           new_direction_minus)

                                # asteroids_to_add.append(asteroid1)
                                t = Timer(1, asteroids_to_add.append(asteroid1))
                                t.start()

                                asteroids_to_add.append(asteroid2)

                            score_to_add += ast.score_value
            for bullet_to_remove in bullets_to_remove:
                try:
                    player.bullets.remove(bullet_to_remove)
                    break
                except ValueError:
                    pass
            for ast_to_remove in asteroids_to_remove:
                try:
                    self.asteroids.remove(ast_to_remove)
                    break
                except ValueError:
                    pass

            for ast_to_add in asteroids_to_add:
                self.asteroids.append(ast_to_add)
            if not self.asteroids:
                self.level_up()
            player.score += score_to_add

    # F-ja za proveravanje sa kim se igrač sudario
    def player_collision(self):
        igr = Howmany.igraci
        global eex
        players_to_remove = []
        self.lock.acquire()
        for player in self.players:

            if player.godmode == 0:
                for ast in self.asteroids:
                    if ast.hitbox[1] + ast.hitbox[3] > player.position[1] > ast.hitbox[1]:
                        if ast.hitbox[0] < player.position[0] < ast.hitbox[0] + ast.hitbox[2]:
                            player.godmode = 1
                            player.now = time.time()
                            player.future = player.now + 2
                            print('collision')
                            player.lives -= 1
                            if player.lives <= 0:
                                players_to_remove.append(player)
                                eex = eex + 1
                            player.position[0] = screen_size[0] // 2
                            player.position[1] = screen_size[1] // 2
                            break
            for deus_ex in self.deus_ex:
                if deus_ex.hitbox[1] + deus_ex.hitbox[3] > player.position[1] > deus_ex.hitbox[1]:
                    if deus_ex.hitbox[0] < player.position[0] < deus_ex.hitbox[0] + deus_ex.hitbox[2]:
                        if deus_ex.state == 1:
                            bonus = random.choice([1, 2, 3, 4])
                            if bonus == 1:
                                player.score += 1000
                            if bonus == 2:
                                player.lives += 1
                            if bonus == 3:
                                player.score -= 2000
                            if bonus == 4:
                                player.lives -= 1

                            self.deus_ex.remove(deus_ex)
                        print('collision with deus_ex')

        for pra in players_to_remove:
            Howmany.score.append(pra.score)
        for player in players_to_remove:
            self.players.remove(player)
        self.lock.release()
        if eex == igr:
            Howmany.kraj = 1

    # Izbacivanje metka iz liste metaka
    def remove_bullets(self):
        for player in self.players:
            for bullet in player.bullets:
                if bullet.direction_xy[0] < -1 or bullet.direction_xy[1] < -1 or bullet.direction_xy[0] > 1280 or \
                        bullet.direction_xy[1] > 720:
                    print('removed')
                    player.bullets.remove(bullet)

    # Provera da li postoji igrač sa datim id-jem
    def does_player_exist(self, player_id):
        obj = next((x for x in self.players if x.id == player_id), None)
        if obj is None:
            return False
        else:
            return True

    def run(self):
        run2 = True
        while run2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run2 = False
                elif event.type == AsteroidsGame.UPDATE:
                    if Howmany.kraj == 1:
                        self.endScreen()
                    else:
                        keys_pressed = pygame.key.get_pressed()

                        # Pomeranje levo i desno za sve igrače
                        if keys_pressed[pygame.K_RIGHT] and self.does_player_exist(1):
                            next((x for x in self.players if x.id == 1), None).turn("right")
                            # next((x for x in self.players if x.id == 1), None).turn("right")
                        if keys_pressed[pygame.K_d] and self.does_player_exist(2):
                            next((x for x in self.players if x.id == 2), None).turn("right")
                            # next((x for x in self.players if x.id == 2), None).turn("right")
                        if keys_pressed[pygame.K_KP6] and self.does_player_exist(3):
                            next((x for x in self.players if x.id == 3), None).turn("right")
                            # next((x for x in self.players if x.id == 3), None).turn("right")
                        if keys_pressed[pygame.K_l] and self.does_player_exist(4):
                            next((x for x in self.players if x.id == 4), None).turn("right")
                            # next((x for x in self.players if x.id == 4), None).turn("right")

                        if keys_pressed[pygame.K_LEFT] and self.does_player_exist(1):
                            next((x for x in self.players if x.id == 1), None).turn("left")
                            # next((x for x in self.players if x.id == 1), None).turn("left")
                        if keys_pressed[pygame.K_a] and self.does_player_exist(2):
                            next((x for x in self.players if x.id == 2), None).turn("left")
                            # next((x for x in self.players if x.id == 2), None).turn("left")
                        if keys_pressed[pygame.K_KP4] and self.does_player_exist(3):
                            next((x for x in self.players if x.id == 3), None).turn("left")
                            # next((x for x in self.players if x.id == 3), None).turn("left")
                        if keys_pressed[pygame.K_j] and self.does_player_exist(4):
                            next((x for x in self.players if x.id == 4), None).turn("left")
                            # next((x for x in self.players if x.id == 4), None).turn("left")

                        # Pomeranje pravo za sve igrače
                        if self.does_player_exist(1):
                            if keys_pressed[pygame.K_UP] and self.does_player_exist(1):
                                next((x for x in self.players if x.id == 1), None).isMoving = True
                                if next((x for x in self.players if x.id == 1), None).speed < next(
                                        (x for x in self.players if x.id == 1), None).max_speed:
                                    next((x for x in self.players if x.id == 1), None).speed += 0.5
                                    if next((x for x in self.players if x.id == 1), None).speed > next(
                                            (x for x in self.players if x.id == 1), None).max_speed:
                                        next((x for x in self.players if x.id == 1), None).speed = next(
                                            (x for x in self.players if x.id == 1), None).max_speed
                            else:
                                next((x for x in self.players if x.id == 1), None).isMoving = False
                                if next((x for x in self.players if x.id == 1), None).speed > 0:
                                    next((x for x in self.players if x.id == 1), None).speed -= 0.5
                                    if next((x for x in self.players if x.id == 1), None).speed < 0:
                                        next((x for x in self.players if x.id == 1), None).speed = 0
                        if self.does_player_exist(2):
                            if keys_pressed[pygame.K_w]:
                                next((x for x in self.players if x.id == 2), None).isMoving = True
                                if next((x for x in self.players if x.id == 2), None).speed < next(
                                        (x for x in self.players if x.id == 2), None).max_speed:
                                    next((x for x in self.players if x.id == 2), None).speed += 0.5
                                    if next((x for x in self.players if x.id == 2), None).speed > next(
                                            (x for x in self.players if x.id == 2), None).max_speed:
                                        next((x for x in self.players if x.id == 2), None).speed = next(
                                            (x for x in self.players if x.id == 2), None).max_speed
                            else:
                                next((x for x in self.players if x.id == 2), None).isMoving = False
                                if next((x for x in self.players if x.id == 2), None).speed > 0:
                                    next((x for x in self.players if x.id == 2), None).speed -= 0.5
                                    if next((x for x in self.players if x.id == 2), None).speed < 0:
                                        next((x for x in self.players if x.id == 2), None).speed = 0
                        if self.does_player_exist(3):
                            if keys_pressed[pygame.K_KP8]:
                                next((x for x in self.players if x.id == 3), None).isMoving = True
                                if next((x for x in self.players if x.id == 3), None).speed < next(
                                        (x for x in self.players if x.id == 3), None).max_speed:
                                    next((x for x in self.players if x.id == 3), None).speed += 0.5
                                    if next((x for x in self.players if x.id == 3), None).speed > next(
                                            (x for x in self.players if x.id == 3), None).max_speed:
                                        next((x for x in self.players if x.id == 3), None).speed = next(
                                            (x for x in self.players if x.id == 3), None).max_speed
                            else:
                                next((x for x in self.players if x.id == 3), None).isMoving = False
                                if next((x for x in self.players if x.id == 3), None).speed > 0:
                                    next((x for x in self.players if x.id == 3), None).speed -= 0.5
                                    if next((x for x in self.players if x.id == 3), None).speed < 0:
                                        next((x for x in self.players if x.id == 3), None).speed = 0
                        if self.does_player_exist(4):
                            if keys_pressed[pygame.K_i]:
                                next((x for x in self.players if x.id == 4), None).isMoving = True
                                if next((x for x in self.players if x.id == 4), None).speed < next(
                                        (x for x in self.players if x.id == 4), None).max_speed:
                                    next((x for x in self.players if x.id == 4), None).speed += 0.5
                                    if next((x for x in self.players if x.id == 4), None).speed > next(
                                            (x for x in self.players if x.id == 4), None).max_speed:
                                        next((x for x in self.players if x.id == 4), None).speed = next(
                                            (x for x in self.players if x.id == 4), None).max_speed
                            else:
                                next((x for x in self.players if x.id == 4), None).isMoving = False
                                if next((x for x in self.players if x.id == 4), None).speed > 0:
                                    next((x for x in self.players if x.id == 4), None).speed -= 0.5
                                    if next((x for x in self.players if x.id == 4), None).speed < 0:
                                        next((x for x in self.players if x.id == 4), None).speed = 0

                        # Pucanje za sve igrače
                        if keys_pressed[pygame.K_RETURN] and self.does_player_exist(1):
                            new_time = datetime.datetime.now()
                            if new_time - self.fire_time[0] > datetime.timedelta(seconds=0.15):
                                next((x for x in self.players if x.id == 1), None).shoot()
                                self.fire_time[0] = new_time
                        if keys_pressed[pygame.K_LSHIFT] and self.does_player_exist(2):
                            new_time = datetime.datetime.now()
                            if new_time - self.fire_time[1] > datetime.timedelta(seconds=0.15):
                                next((x for x in self.players if x.id == 2), None).shoot()
                                self.fire_time[1] = new_time
                        if keys_pressed[pygame.K_KP_ENTER] and self.does_player_exist(3):
                            new_time = datetime.datetime.now()
                            if new_time - self.fire_time[2] > datetime.timedelta(seconds=0.15):
                                next((x for x in self.players if x.id == 3), None).shoot()
                                self.fire_time[2] = new_time
                        if keys_pressed[pygame.K_SPACE] and self.does_player_exist(4):
                            new_time = datetime.datetime.now()
                            if new_time - self.fire_time[3] > datetime.timedelta(seconds=0.15):
                                next((x for x in self.players if x.id == 4), None).shoot()
                                self.fire_time[3] = new_time

            self.move_entities()
            # self.draw()
            self.hits()
            self.player_collision()
            self.remove_bullets()
            self.check_deus_ex()
            self.check_player_godmode()
            self.clock1.tick(120)

    def endScreen(self):
        self.scoreboard_active = 1
        a = 0
        for ast in self.asteroids:
            self.asteroids.remove(ast)
        for de in self.deus_ex:
            self.deus_ex.remove(de)
        self.screen.fill(0)
        if Howmany.igraci == 1:
            while (a < 7):
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 72)
                textsurface = myfont.render("Game Over", False, (0, 0, 0), (255, 255, 255))
                self.screen.blit(textsurface, (450, 100))
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 28)
                textsurface = myfont.render("Player 1: " + str(Howmany.score[0]), False, (0, 0, 0), (255, 255, 255))
                self.screen.blit(textsurface, (550, 200))
                pygame.display.flip()
                a = a + 1
                time.sleep(1)
        elif Howmany.igraci == 2:
            while (a < 7):
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 72)
                textsurface = myfont.render("Game Over", False, (0, 0, 0), (255, 255, 255))
                self.screen.blit(textsurface, (450, 100))
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 28)
                textsurface = myfont.render("Player 1: " + str(Howmany.score[0]), False, (0, 0, 0), (255, 255, 255))
                self.screen.blit(textsurface, (550, 200))
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 28)
                textsurface = myfont.render("Player 2: " + str(Howmany.score[1]), False, (0, 0, 0), (255, 255, 255))
                self.screen.blit(textsurface, (550, 250))
                pygame.display.flip()
                a = a + 1
                time.sleep(1)
        elif Howmany.igraci == 3:
            while (a < 7):
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 72)
                textsurface = myfont.render("Game Over", False, (0, 0, 0), (255, 255, 255))
                self.screen.blit(textsurface, (450, 100))
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 28)
                textsurface = myfont.render("Player 1: " + str(Howmany.score[0]), False, (0, 0, 0), (255, 255, 255))
                self.screen.blit(textsurface, (550, 200))
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 28)
                textsurface = myfont.render("Player 2: " + str(Howmany.score[1]), False, (0, 0, 0), (255, 255, 255))
                self.screen.blit(textsurface, (550, 250))
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 28)
                textsurface = myfont.render("Player 3: " + str(Howmany.score[2]), False, (0, 0, 0), (255, 255, 255))
                self.screen.blit(textsurface, (550, 300))
                pygame.display.flip()
                a = a + 1
                time.sleep(1)
        elif Howmany.igraci == 4:
            while (a < 7):
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 72)
                textsurface = myfont.render("Game Over", False, (0, 0, 0), (255, 255, 255))
                self.screen.blit(textsurface, (450, 100))
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 28)
                textsurface = myfont.render("Player 1: " + str(Howmany.score[0]), False, (0, 0, 0), (255, 255, 255))
                self.screen.blit(textsurface, (550, 200))
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 28)
                textsurface = myfont.render("Player 2: " + str(Howmany.score[1]), False, (0, 0, 0), (255, 255, 255))
                self.screen.blit(textsurface, (550, 250))
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 28)
                textsurface = myfont.render("Player 3: " + str(Howmany.score[2]), False, (0, 0, 0), (255, 255, 255))
                self.screen.blit(textsurface, (550, 300))
                pygame.font.init()
                myfont = pygame.font.SysFont('Arial', 28)
                textsurface = myfont.render("Player 4: " + str(Howmany.score[3]), False, (0, 0, 0), (255, 255, 255))
                self.screen.blit(textsurface, (550, 350))
                pygame.display.flip()
                a = a + 1
                time.sleep(1)
        pygame.quit()
        sys.exit()
        # Menu.main()
