import pygame
import sys

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Marine Life Rescue Maze")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Define fonts
FONT = pygame.font.Font(None, 36)
BIG_FONT = pygame.font.Font(None, 72)  # Font for game end messages

# Load images
TURTLE_IMG = pygame.image.load("C:/Users/munga/Downloads/randall-ruiz-272502.jpg")
TURTLE_IMG = pygame.transform.scale(TURTLE_IMG, (80, 80))
DOLPHIN_IMG = pygame.image.load("C:/Users/munga/Downloads/Screen_Shot_2022-05-25_at_1.39.34_PM.png")
DOLPHIN_IMG = pygame.transform.scale(DOLPHIN_IMG, (80, 80))
NET_IMG = pygame.image.load("C:/Users/munga/Downloads/istockphoto-1397943458-612x612.jpg")
NET_IMG = pygame.transform.scale(NET_IMG, (80, 80))
OIL_IMG = pygame.image.load("C:/Users/munga/Downloads/Mauritius-oil-spill.jpg")
OIL_IMG = pygame.transform.scale(OIL_IMG, (80, 80))
WHALE_IMG = pygame.image.load("C:/Users/munga/Downloads/download.jpg")
WHALE_IMG = pygame.transform.scale(WHALE_IMG, (80, 80))
FISH_IMG = pygame.image.load("C:/Users/munga/Downloads/download (1).jpg")
FISH_IMG = pygame.transform.scale(FISH_IMG, (80, 80))
PERSON_IMG = pygame.image.load("C:/Users/munga/Downloads/331aae3dd6c79ba209c56f4ca7def4ea.jpg")  # Path to your person icon
PERSON_IMG = pygame.transform.scale(PERSON_IMG, (80, 80))  # Scale the person image to fit in the grid

# Load sounds
RESCUE_SOUND = pygame.mixer.Sound("C:/Users/munga/Downloads/mixkit-magic-marimba-2820.wav")
DANGER_SOUND = pygame.mixer.Sound("C:/Users/munga/Downloads/mixkit-arcade-retro-game-over-213.wav")

# Maze structure with multiple levels
LEVELS = [
   
    [
        ["S", "D", ".", ".", "#", ".", ".", "T"],
        [".", "#", ".", ".", "#", ".", ".", "."],
        [".", ".", ".", "M", ".", ".", "#", "."],
        ["#", ".", "O", ".", ".", "#", ".", "."],
        [".", ".", ".", ".", "N", ".", ".", "."],
        ["#", "#", ".", ".", ".", ".", ".", "."],
        ["T", ".", ".", ".", "#", ".", "D", "E"]
    ],
    [
        ["S", ".", "O", ".", ".", "T", ".", "D"],
        [".", ".", ".", "#", ".", ".", "#", "."],
        ["#", ".", ".", "M", ".", "N", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["O", ".", "#", "#", ".", ".", ".", "T"],
        [".", "D", ".", ".", ".", "N", ".", "."],
        ["#", ".", ".", ".", "#", ".", ".", "E"]
    ],
    [
        ["S", ".", "#", ".", ".", "T", ".", "D"],
        [".", "#", ".", "#", "O", ".", "N", "."],
        [".", "M", ".", ".", ".", "#", ".", "."],
        ["#", ".", ".", "O", ".", ".", ".", "."],
        [".", ".", "N", ".", ".", ".", ".", "T"],
        ["D", ".", ".", "#", ".", "#", ".", "."],
        ["#", ".", "#", "M", ".", "D", ".", "E"]
    ],
    [
        ["S", "D", "O", ".", ".", "#", ".", "T"],
        [".", ".", ".", "#", ".", "N", ".", "."],
        [".", "#", ".", "M", "#", ".", "O", "."],
        ["#", ".", "D", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "N", "."],
        ["T", ".", "#", "O", ".", ".", "#", "."],
        ["#", ".", "#", "M", ".", "D", ".", "E"]
    ],
    [
        ["#", ".", "N", "#", "#", "#", "#", "#"],
        ["#", "S", ".", "D", "#", ".", ".", "#"],
        ["O", ".", "#", ".", "N", ".", "E", "."],
        ["#", "N", "#", ".", ".", "W", ".", "#"],
        ["#", ".", "#", "#", "#", "#", ".", "W"],
        ["O", ".", ".", "F", ".", "O", ".", "#"],
        ["#", "T", ".", "#", ".", "#", ".", "."],
        ["#", "#", "O", "#", "#", "#", "#", "#"]
    ],
     [
        ["S", ".", ".", "T", ".", ".", "N", "D"],
        ["#", "#", "#", "#", "#", "#", "#", "."],
        [".", "M", "O", ".", ".", ".", "#", "."],
        ["O", "W", ".", "O", ".", ".", ".", "."],
        [".", "#", ".", ".", "O", "N", "#", "N"],
        [".", "F", ".", "#", "#", "#", "#", "."],
        ["#", ".", "N", ".", ".", ".", ".", "E"]
    ],
]

# Game settings
player_pos = [0, 0]
current_level = 0
score = 0
time_limit = 60  # 60 seconds per level
rescued_animals = []


# Function to draw the maze
def draw_maze(level):
    cell_size = 80
    for i, row in enumerate(level):
        for j, cell in enumerate(row):
            rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
            pygame.draw.rect(WIN, WHITE, rect)  # Draw white cells as background
            if cell == "#":
                pygame.draw.rect(WIN, BLACK, rect)  # Draw obstacles
            elif cell == "T":
                WIN.blit(TURTLE_IMG, rect)  # Draw turtle
            elif cell == "D":
                WIN.blit(DOLPHIN_IMG, rect)  # Draw dolphin
            elif cell == "O":
                WIN.blit(OIL_IMG, rect)  # Draw oil spill
            elif cell == "N":
                WIN.blit(NET_IMG, rect)  # Draw fishing net
            elif cell == "W":
                WIN.blit(WHALE_IMG, rect)  # Draw whale
            elif cell == "F":
                WIN.blit(FISH_IMG, rect)  # Draw fish
            elif cell == "E":
                pygame.draw.rect(WIN, YELLOW, rect)  # Draw the end point

    # Draw player as a person icon
    player_x, player_y = player_pos
    player_rect = pygame.Rect(player_y * cell_size, player_x * cell_size, cell_size, cell_size)
    WIN.blit(PERSON_IMG, player_rect.topleft)  # Draw the player icon at the top-left corner of the cell


# Function to handle player movement
def move_player(key, level):
    global player_pos
    x, y = player_pos
    if key == pygame.K_UP:  # Up
        new_pos = [x - 1, y]
    elif key == pygame.K_DOWN:  # Down
        new_pos = [x + 1, y]
    elif key == pygame.K_LEFT:  # Left
        new_pos = [x, y - 1]
    elif key == pygame.K_RIGHT:  # Right
        new_pos = [x, y + 1]
    else:
        return

    if (0 <= new_pos[0] < len(level)) and (0 <= new_pos[1] < len(level[0])):
        if level[new_pos[0]][new_pos[1]] != "#":
            player_pos = new_pos


# Function to check for interactions
def check_interaction(level):
    global score, rescued_animals
    x, y = player_pos
    current_cell = level[x][y]

    if current_cell in ["T", "D", "W", "F"]:
        if current_cell == "T":
            rescued_animals.append("Turtle")
            score += 10
        elif current_cell == "D":
            rescued_animals.append("Dolphin")
            score += 20
        elif current_cell == "W":
            rescued_animals.append("Whale")
            score += 30
        elif current_cell == "F":
            rescued_animals.append("Fish")
            score += 15

        level[x][y] = "."  # Remove the rescued animal from the level
        RESCUE_SOUND.play()  # Play the rescue sound
        return "rescued_animal"

    elif current_cell in ["N", "O"]:
        DANGER_SOUND.play()  # Play the danger sound
        return "danger"

    elif current_cell == "E":
        return "level_complete"


def display_message(message, color, size, y_offset):
    text = BIG_FONT.render(message, True, color)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    WIN.blit(text, rect)


# Main game loop
def main():
    global current_level, player_pos, score
    clock = pygame.time.Clock()
    level_start_time = pygame.time.get_ticks()

    while True:
        WIN.fill(BLACK)  # Clear the screen

        draw_maze(LEVELS[current_level])

        # Display score
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        WIN.blit(score_text, (10, 10))

        # Display time left
        elapsed_time = (pygame.time.get_ticks() - level_start_time) / 1000
        time_left = max(0, int(time_limit - elapsed_time))
        time_text = FONT.render(f"Time left: {time_left}s", True, WHITE)
        WIN.blit(time_text, (WIDTH - 150, 10))

        # Check if the level is complete
        interaction_result = check_interaction(LEVELS[current_level])
        if interaction_result == "level_complete":
            if current_level < len(LEVELS) - 1:
                current_level += 1
                player_pos = [0, 0]
                level_start_time = pygame.time.get_ticks()
            else:
                display_message("Congratulations! You won!", GREEN, 72, 0)
                pygame.display.flip()
                pygame.time.wait(3000)
                pygame.quit()
                sys.exit()

        # Check if time is up
        if time_left == 0:
            display_message("Time's up! You lost.", RED, 72, 0)
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                move_player(event.key, LEVELS[current_level])

        # Update the display
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()