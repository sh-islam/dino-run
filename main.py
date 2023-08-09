import sys
import random
import pygame

# Init pygame and pygame variables
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("MapleStory JUMP!")

game_speed = 10
game_font = pygame.font.Font("./assets/Maplestory_Bold.ttf", 20)
ground_x_pos = 70
ground_y_pos = 550
obstacle_x_pos = 1000
player_score = 0
game_over = False


# Classes
# Character class
class Character(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.running_sprites = []
        self.jump_sprites = []

        for i in range(4):
            running_image_path = f"./assets/walking_{i}.png"
            # Flips only x (see True,False), scales both x and y
            running_image = pygame.transform.flip(
                pygame.transform.scale(pygame.image.load(running_image_path), (
                    int(0.7 * pygame.image.load(running_image_path).get_width()),
                    int(0.7 * pygame.image.load(running_image_path).get_height())
                )), True, False
            )
            self.running_sprites.append(running_image)

        jump_image_path = "./assets/jumping.png"
        jump_image = pygame.transform.flip(
            pygame.transform.scale(pygame.image.load(jump_image_path), (
                int(0.7 * pygame.image.load(jump_image_path).get_width()),
                int(0.7 * pygame.image.load(jump_image_path).get_height())
            )), True, False
        )
        self.jump_sprites.append(jump_image)

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        # self.rect = pygame.Rect(self.x_pos, self.y_pos, 100, 200)
        # # Create the resized rectangle with the new position
        # self.rect = pygame.Rect(50, 420, 75, 125)

        self.walk_anim_speed = 0.2
        self.is_jumping = False
        self.jump_count = 0
        self.max_jumpCount = 2
        self.gravity = 0.55
        self.jump_height = 65  # Adjust this value to control the jump height
        self.jump_vel = -((2 * self.jump_height) / self.gravity) ** 0.5

    def update(self):
        self.animate()
        if self.is_jumping:
            self.jump()
        self.rect.center = (self.x_pos, self.y_pos)

    def animate(self):
        if self.is_jumping:
            self.image = self.jump_sprites[0]
        else:
            self.current_image += self.walk_anim_speed
            if self.current_image >= 3:
                self.current_image = 0
            self.image = self.running_sprites[int(self.current_image)]

    def jump(self):
        self.y_pos += self.jump_vel
        self.jump_vel += self.gravity


        if self.y_pos >= ground_y_pos:
            self.y_pos = ground_y_pos
            self.is_jumping = False
            self.jump_count = 0


# Cloud class
class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos):
        super().__init__()
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        # Randomly choose a scale factor
        self.size = random.uniform(0.4, 2.0)
        # Set the size through transform.scale method
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.size),
                                                         int(self.image.get_height() * self.size)))

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        # Redraws the cloud by 1px left every time it's updated (which is in while true)
        self.rect.x -= 1


# Snail class
class Snail(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = pygame.image.load("./assets/snail.png")
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def update(self):
        self.rect.x -= 4


# Mushroom class
class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.running_sprites = []
        self.jump_sprites = []

        # Load running sprites
        for i in range(3):
            running_image_path = f"./assets/mush_{i}.png"
            running_image = pygame.image.load(running_image_path)
            self.running_sprites.append(running_image)

        # Load jump sprite
        jump_image_path = "./assets/mush_jump_0.png"
        jump_image = pygame.image.load(jump_image_path)
        self.jump_sprites.append(jump_image)

        # Set initial positions, images, and other variables
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.jump_vel = None
        self.is_jumping = False
        self.jump_count = 0
        self.walk_anim_speed = 0.1
        self.gravity = 0.8  # This controls how high it jumps as no velocity is set
        self.jump_timer = 0
        self.jump_interval = 1.5  # Jump interval in seconds

    def update(self):
        original_x = self.rect.x  # Store the original x position
        self.animate()
        self.jump()
        self.rect.x = original_x  # Restore the original x position
        self.rect.x -= 6  # Move horizontally

    def animate(self):
        if self.is_jumping:
            self.image = self.jump_sprites[0]
        else:
            self.current_image += self.walk_anim_speed
            if self.current_image >= 3:
                self.current_image = 0
            self.image = self.running_sprites[int(self.current_image)]

    def jump(self):
        if not self.is_jumping:
            self.jump_timer += 1
            if self.jump_timer >= self.jump_interval * 60:  # Convert seconds to frames (60 FPS)
                self.jump_timer = 0
                self.is_jumping = True
                self.jump_vel = -15  # Set initial jump velocity

        if self.is_jumping:
            self.y_pos += self.jump_vel
            self.jump_vel += self.gravity  # Apply gravity
            self.jump_count += 1

            if self.y_pos >= 597:  # Reached the ground
                self.y_pos = 597
                self.is_jumping = False
                self.jump_count = 0

            self.rect.center = (self.x_pos, self.y_pos)  # Update the sprite's position


# Create buttons to show in game over menu
class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y):
        super().__init__()
        self.font = pygame.font.Font(None, 40)
        self.text = text
        self.image = self.font.render(self.text, True, (0, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))


yes_button = Button("Yes", 550, 400)
no_button = Button("No", 730, 400)
button_group = pygame.sprite.Group(yes_button, no_button)

# Ground platform image
ground = pygame.image.load("./assets/ground.png")
ground_x = 0
ground_y = 550
# Cloud images
cloud = pygame.image.load("./assets/cloud.png")
cloud = pygame.transform.scale(cloud, (200, 80))

# Groups
char_sprites_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()
snail_sprites_group = pygame.sprite.Group()
mush_sprites_group = pygame.sprite.Group()

# Character object (which always appears, all other objects appear according to events)
character = Character(ground_x_pos, ground_y_pos)
char_sprites_group.add(character)

# Events
cloud_event = pygame.USEREVENT
# pygame.time.set_timer(cloud_event, 3500) # creates a cloud event every 3.5s
pygame.time.set_timer(cloud_event, random.randint(4000, 15000))  # create a cloud event randomly from 3-10s
spawn_event = pygame.USEREVENT
pygame.time.set_timer(spawn_event, random.randint(1000, 2500))


# Restart game function
def restart_game():
    global game_over, player_score, ground_x, ground_y, character
    # Reset game state variables
    game_over = False
    player_score = 0
    # Reset ground position
    ground_x = 0
    ground_y = 550
    # Clear sprite groups
    cloud_group.empty()
    snail_sprites_group.empty()
    mush_sprites_group.empty()
    char_sprites_group.empty()  # Empty old character, make a new one and add to sprite group
    character = Character(ground_x_pos, ground_y_pos)
    char_sprites_group.add(character)


# Run/quit loop
while True:

    clock.tick(60)  # Running at 60fps
    screen.fill("Sky blue")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == cloud_event:
            current_cloud_y = random.randint(50, 500)  # get cloud height position randomly
            current_cloud = Cloud(cloud, 1500, current_cloud_y)  # '1500' to spawn 300px before entering screen res
            cloud_group.add(current_cloud)

        if event.type == spawn_event:
            mob_options = ['snail', 'mush', 'pig']
            event_name = random.choice(mob_options)

            if event_name == 'snail':
                current_snail = Snail(1350, 610)
                snail_sprites_group.add(current_snail)
                # snail_sprites_group.update()
                # snail_sprites_group.draw(screen)

            if event_name == "mush":
                current_mush = Mushroom(1525, 597)
                mush_sprites_group.add(current_mush)

        # When space is pressed, char in jump state, apply upward velocity
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if character.jump_count < character.max_jumpCount:
                    character.is_jumping = True
                    character.jump_vel = -((2 * character.jump_height) / character.gravity) ** 0.5
                    character.jump_count += 1

    if not game_over:

        player_score += 0.1
        player_score_font = pygame.font.Font("./assets/Maplestory_Bold.ttf", 12)  # Change the font size here
        player_score_surface = player_score_font.render(str(int(player_score)), True, "black")

        # Move ground image horizontally across screen
        ground_x -= game_speed
        # Reset ground when it goes off the screen
        if ground_x <= -1280:
            ground_x = 0
        # Draw ground
        screen.blit(ground, (ground_x, ground_y))
        # As ground_x decreases, ground image is moved across screen by resetting to 0 to create infinite scrolling
        # effect
        screen.blit(ground, (ground_x + 1280, ground_y))

        # Update and draw grouped objects (note the ordering--last group that is drawn appears top most)
        cloud_group.update()
        cloud_group.draw(screen)
        snail_sprites_group.update()
        snail_sprites_group.draw(screen)
        char_sprites_group.update()
        char_sprites_group.draw(screen)
        mush_sprites_group.update()
        mush_sprites_group.draw(screen)
        screen.blit(player_score_font.render(f"Score: {int(player_score)}", True, "black"), (1100, 10))
        pygame.display.update()  # Updates the display

    if pygame.sprite.spritecollide(character, snail_sprites_group, False, pygame.sprite.collide_mask) or \
            pygame.sprite.spritecollide(character, mush_sprites_group, False, pygame.sprite.collide_mask):
        game_over_lines = ["Game Over!", "Restart?"]
        y = 200
        line_spacing = 40

        for line in game_over_lines:
            game_over_text = game_font.render(line, True, "black")
            game_over_rect = game_over_text.get_rect(center=(640, y))
            screen.blit(game_over_text, game_over_rect)
            y += line_spacing

        score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
        score_rect = score_text.get_rect(center=(640, y + line_spacing))
        screen.blit(score_text, score_rect)

        game_over = True

        # Draw buttons
        button_group.draw(screen)
        pygame.display.update()

        # Button event handling
        button_clicked = False
        while not button_clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if yes_button.rect.collidepoint(event.pos):
                            restart_game()
                            button_clicked = True
                        elif no_button.rect.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
