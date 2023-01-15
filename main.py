import pygame
from pygame import mixer
from player import Player

mixer.init()
pygame.init()

# game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("COMBAT")

#framerte
clock = pygame.time.Clock()
FPS = 60

#fighter variables
KNIGHT_SIZE = 162
KNIGHT_SCALE = 4
KNIGHT_OFFSET = [72, 56]
KNIGHT_DATA = [KNIGHT_SIZE, KNIGHT_SCALE, KNIGHT_OFFSET]
DEMON_SIZE = 250
DEMON_SCALE = 3
DEMON_OFFSET = [112, 107]
DEMON_DATA = [DEMON_SIZE, DEMON_SCALE, DEMON_OFFSET]


#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#fonts
count_font = pygame.font.Font("items/Fonts/turok.ttf", 80)
score_font = pygame.font.Font("items/Fonts/turok.ttf", 50)

# audio
pygame.mixer.music.load("items/audio/battle-of-the-dragons-8037.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("items/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("items/audio/magic.wav")
magic_fx.set_volume(0.75)


#background image
bg_image = pygame.image.load("items/images/background/background 1.png").convert_alpha()

#characters image
knight_sheet = pygame.image.load("items/images/Knight/kinght.png").convert_alpha()
demon_sheet = pygame.image.load("items/images/demon/Demon.png").convert_alpha()

# victory image
victory_img = pygame.image.load("items/images/background/win.jpeg").convert_alpha()

#steps in animation
KNIGHT_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
DEMON_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# colors
GREEN = (118,238,0)
WHITE = (255, 255, 255)
BLUE = (0,0,255)
OLIVE = (128,128,0)

# fighter instances
player_1 = Player(1, 200, 310, False, KNIGHT_DATA, knight_sheet, KNIGHT_ANIMATION_STEPS, sword_fx)
player_2 = Player(2, 700, 310, True, DEMON_DATA, demon_sheet, DEMON_ANIMATION_STEPS, magic_fx)


#drawing text
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#drawing background
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#character health
def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, BLUE, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, WHITE, (x, y, 400, 30))
  pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))

# fighter instances
player_1 = Player(1, 200, 310, False, KNIGHT_DATA, knight_sheet, KNIGHT_ANIMATION_STEPS, sword_fx)
player_2 = Player(2, 700, 310, True, DEMON_DATA, demon_sheet, DEMON_ANIMATION_STEPS, magic_fx)

# game loop
run = True
while run:

  clock.tick(FPS)


  draw_bg()

  # player health
  draw_health_bar(player_1.health, 20, 20)
  draw_health_bar(player_2.health, 580, 20)
  draw_text("KNIGHT: " + str(score[0]), score_font, OLIVE, 20, 60)
  draw_text("DEMON: " + str(score[1]), score_font, OLIVE, 580, 60)

  if intro_count <= 0:

    player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_2, round_over)
    player_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_1, round_over)
  else:

    draw_text(str(intro_count), count_font, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)

    if (pygame.time.get_ticks() - last_count_update) >= 1000:
      intro_count -= 1
      last_count_update = pygame.time.get_ticks()

  #update fighters
  player_1.update()
  player_2.update()

  # draw characters
  player_1.draw(screen)
  player_2.draw(screen)

  #check for player defeat
  if round_over == False:
    if player_1.alive == False:
      score[1] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
    elif player_2.alive == False:
      score[0] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
  else:

    screen.blit(victory_img, (360, 150))
    if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
      round_over = False
      intro_count = 3
      player_1 = Player(1, 200, 310, False, KNIGHT_DATA, knight_sheet, KNIGHT_ANIMATION_STEPS, sword_fx)
      player_2 = Player(2, 700, 310, True, DEMON_DATA, demon_sheet, DEMON_ANIMATION_STEPS, magic_fx)

    # event
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  # display
  pygame.display.update()

# exit game
pygame.quit()