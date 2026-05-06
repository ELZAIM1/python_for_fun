import pygame,sys,random,os
from pygame.math import Vector2

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class SNAKE:
	"""
	The SNAKE class handles the snake's appearance, movement, and sound effects.
	It manages the snake's body segments, direction, and graphics.
	"""
	def __init__(self):
		# Initialize snake body with 3 segments at starting position
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		# Initial direction (stationary)
		self.direction = Vector2(0,0)
		# Flag for when snake grows
		self.new_block = False

		# Load snake head graphics for different directions
		self.head_up = pygame.image.load(os.path.join(SCRIPT_DIR, 'Graphics/head_up.png')).convert_alpha()
		self.head_down = pygame.image.load(os.path.join(SCRIPT_DIR, 'Graphics/head_down.png')).convert_alpha()
		self.head_right = pygame.image.load(os.path.join(SCRIPT_DIR, 'Graphics/head_right.png')).convert_alpha()
		self.head_left = pygame.image.load(os.path.join(SCRIPT_DIR, 'Graphics/head_left.png')).convert_alpha()
		
		# Load tail graphics
		self.tail_up = pygame.image.load(os.path.join(SCRIPT_DIR, 'Graphics/tail_up.png')).convert_alpha()
		self.tail_down = pygame.image.load(os.path.join(SCRIPT_DIR, 'Graphics/tail_down.png')).convert_alpha()
		self.tail_right = pygame.image.load(os.path.join(SCRIPT_DIR, 'Graphics/tail_right.png')).convert_alpha()
		self.tail_left = pygame.image.load(os.path.join(SCRIPT_DIR, 'Graphics/tail_left.png')).convert_alpha()

		# Load body graphics for different orientations
		self.body_vertical = pygame.image.load(os.path.join(SCRIPT_DIR, 'Graphics/body_vertical.png')).convert_alpha()
		self.body_horizontal = pygame.image.load(os.path.join(SCRIPT_DIR, 'Graphics/body_horizontal.png')).convert_alpha()

		self.body_tr = pygame.image.load(os.path.join(SCRIPT_DIR, 'Graphics/body_tr.png')).convert_alpha()
		self.body_tl = pygame.image.load(os.path.join(SCRIPT_DIR, 'Graphics/body_tl.png')).convert_alpha()
		self.body_br = pygame.image.load(os.path.join(SCRIPT_DIR, 'Graphics/body_br.png')).convert_alpha()
		self.body_bl = pygame.image.load(os.path.join(SCRIPT_DIR, 'Graphics/body_bl.png')).convert_alpha()
		# Load crunch sound effect
		self.crunch_sound = pygame.mixer.Sound(os.path.join(SCRIPT_DIR, 'Sound/crunch.wav'))

	def draw_snake(self):
		# Update graphics for head and tail based on direction
		self.update_head_graphics()
		self.update_tail_graphics()

		# Draw each body segment
		for index,block in enumerate(self.body):
			x_pos = int(block.x * cell_size)
			y_pos = int(block.y * cell_size)
			block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

			if index == 0:  # Head
				screen.blit(self.head,block_rect)
			elif index == len(self.body) - 1:  # Tail
				screen.blit(self.tail,block_rect)
			else:  # Body segments
				previous_block = self.body[index + 1] - block
				next_block = self.body[index - 1] - block
				if previous_block.x == next_block.x:
					screen.blit(self.body_vertical,block_rect)
				elif previous_block.y == next_block.y:
					screen.blit(self.body_horizontal,block_rect)
				else:
					if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
						screen.blit(self.body_tl,block_rect)
					elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
						screen.blit(self.body_bl,block_rect)
					elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
						screen.blit(self.body_tr,block_rect)
					elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
						screen.blit(self.body_br,block_rect)

	def update_head_graphics(self):
		# Determine head graphic based on movement direction
		head_relation = self.body[1] - self.body[0]
		if head_relation == Vector2(1,0): self.head = self.head_left
		elif head_relation == Vector2(-1,0): self.head = self.head_right
		elif head_relation == Vector2(0,1): self.head = self.head_up
		elif head_relation == Vector2(0,-1): self.head = self.head_down

	def update_tail_graphics(self):
		# Determine tail graphic based on movement direction
		tail_relation = self.body[-2] - self.body[-1]
		if tail_relation == Vector2(1,0): self.tail = self.tail_left
		elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
		elif tail_relation == Vector2(0,1): self.tail = self.tail_up
		elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

	def move_snake(self):
		# Only move if direction is set (not stationary)
		if self.direction != Vector2(0,0):
			if self.new_block == True:
				# Grow snake by adding new head without removing tail
				body_copy = self.body[:]
				body_copy.insert(0,body_copy[0] + self.direction)
				self.body = body_copy[:]
				self.new_block = False
			else:
				# Normal movement: remove tail, add new head
				body_copy = self.body[:-1]
				body_copy.insert(0,body_copy[0] + self.direction)
				self.body = body_copy[:]

	def add_block(self):
		# Flag to grow snake on next move
		self.new_block = True

	def play_crunch_sound(self):
		# Play sound when eating fruit
		self.crunch_sound.play()

	def reset(self):
		# Reset snake to initial state
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(0,0)


class FRUIT:
	"""
	The FRUIT class manages the food that the snake eats.
	It handles positioning and drawing of the fruit.
	"""
	def __init__(self):
		# Initialize fruit at random position
		self.randomize()

	def draw_fruit(self):
		# Draw fruit as apple image
		fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
		screen.blit(apple,fruit_rect)

	def randomize(self):
		# Place fruit at random grid position
		self.x = random.randint(0,cell_number - 1)
		self.y = random.randint(0,cell_number - 1)
		self.pos = Vector2(self.x,self.y)

class MAIN:
	"""
	The MAIN class is the game controller.
	It manages game state, updates, drawing, and user interface.
	"""
	def __init__(self):
		# Initialize game objects
		self.snake = SNAKE()
		self.fruit = FRUIT()
		# Game state: 'menu', 'playing', 'game_over', 'instructions'
		self.state = 'menu'
		# Load saved high score
		self.high_score = self.load_high_score()
		# Pause state
		self.paused = False
		# Game speed (lower = faster)
		self.speed = 150  # milliseconds
		# Menu selection
		self.selected_option = 0
		# Sound toggle
		self.sound_enabled = True

	def update(self):
		# Main game update: move snake and check game conditions
		self.snake.move_snake()
		self.check_collision()
		self.check_fail()

	def draw_elements(self):
		# Draw all game elements
		self.draw_grass()
		self.fruit.draw_fruit()
		self.snake.draw_snake()
		self.draw_score()

	def check_collision(self):
		# Check if snake eats fruit
		if self.fruit.pos == self.snake.body[0]:
			# Move fruit and grow snake
			self.fruit.randomize()
			self.snake.add_block()
			if self.sound_enabled:
				self.snake.play_crunch_sound()

		# Ensure fruit doesn't spawn on snake
		for block in self.snake.body[1:]:
			if block == self.fruit.pos:
				self.fruit.randomize()

	def check_fail(self):
		# Check if snake hits wall or itself
		if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
			self.game_over()

		for block in self.snake.body[1:]:
			if block == self.snake.body[0]:
				self.game_over()
		
	def game_over(self):
		# Handle game over: update high score and change state
		score = len(self.snake.body) - 3
		if score > self.high_score:
			self.high_score = score
			self.save_high_score()
		self.state = 'game_over'

	def draw_grass(self):
		grass_color = (167,209,61)
		for row in range(cell_number):
			if row % 2 == 0: 
				for col in range(cell_number):
					if col % 2 == 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)
			else:
				for col in range(cell_number):
					if col % 2 != 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)			

	def draw_score(self):
		score_text = str(len(self.snake.body) - 3)
		score_surface = game_font.render(score_text,True,(56,74,12))
		score_x = int(cell_size * cell_number - 60)
		score_y = int(cell_size * cell_number - 40)
		score_rect = score_surface.get_rect(center = (score_x,score_y))
		apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
		bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

		pygame.draw.rect(screen,(167,209,61),bg_rect)
		screen.blit(score_surface,score_rect)
		screen.blit(apple,apple_rect)
		pygame.draw.rect(screen,(56,74,12),bg_rect,2)

	def draw_menu(self):
		# Draw menu background
		menu_surface = pygame.Surface((cell_number * cell_size, cell_number * cell_size))
		menu_surface.fill((175,215,70))
		
		# Title
		title_text = game_font.render('SNAKE GAME', True, (255,255,255))
		title_rect = title_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 3))
		menu_surface.blit(title_text, title_rect)
		
		# High Score
		hs_text = game_font.render(f'High Score: {self.high_score}', True, (255,255,255))
		hs_rect = hs_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 3 + 60))
		menu_surface.blit(hs_text, hs_rect)
		
		# Menu options
		options = [
			'Start Game',
			f'Difficulty: {self.get_difficulty_name()}',
			f'Sound: {"On" if self.sound_enabled else "Off"}',
			'Quit Game'
		]
		
		y_start = cell_number * cell_size // 2
		for i, option in enumerate(options):
			color = (255, 255, 255) if i == self.selected_option else (56, 74, 12)
			option_text = game_font.render(option, True, color)
			option_rect = option_text.get_rect(center=(cell_number * cell_size // 2, y_start + i * 40))
			menu_surface.blit(option_text, option_rect)
		
		# Instructions
		inst_text = game_font.render('Use UP/DOWN arrows, ENTER to select, I for How to Play', True, (255,255,255))
		inst_rect = inst_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size - 50))
		menu_surface.blit(inst_text, inst_rect)
		
		screen.blit(menu_surface, (0,0))

	def draw_game_over(self):
		# Draw game over background
		go_surface = pygame.Surface((cell_number * cell_size, cell_number * cell_size))
		go_surface.fill((175,215,70))
		
		# Game Over title
		go_text = game_font.render('GAME OVER', True, (255,255,255))
		go_rect = go_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 3))
		go_surface.blit(go_text, go_rect)
		
		# Score
		score = len(self.snake.body) - 3
		score_text = game_font.render(f'Final Score: {score}', True, (255,255,255))
		score_rect = score_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2))
		go_surface.blit(score_text, score_rect)
		
		# High Score
		hs_text = game_font.render(f'High Score: {self.high_score}', True, (255,255,255))
		hs_rect = hs_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2 + 30))
		go_surface.blit(hs_text, hs_rect)
		
		# Options
		restart_text = game_font.render('Press R to Restart', True, (255,255,255))
		restart_rect = restart_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2 + 50))
		go_surface.blit(restart_text, restart_rect)
		
		menu_text = game_font.render('Press M for Menu', True, (255,255,255))
		menu_rect = menu_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2 + 80))
		go_surface.blit(menu_text, menu_rect)
		
		quit_text = game_font.render('Press Q to Quit', True, (255,255,255))
		quit_rect = quit_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2 + 110))
		go_surface.blit(quit_text, quit_rect)
		
		screen.blit(go_surface, (0,0))

	def draw_instructions(self):
		# Draw instructions background
		inst_surface = pygame.Surface((cell_number * cell_size, cell_number * cell_size))
		inst_surface.fill((175,215,70))
		
		# Title
		inst_title = game_font.render('HOW TO PLAY', True, (255,255,255))
		inst_title_rect = inst_title.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 3))
		inst_surface.blit(inst_title, inst_title_rect)
		
		# Instructions text
		inst_lines = [
			'Use arrow keys to move the snake',
			'Eat the red apple to grow and score points',
			'Avoid hitting walls or yourself',
			'Press P to pause during game',
			'',
			'Difficulty: 1-Easy, 2-Medium, 3-Hard',
			'',
			'Press M to return to Menu'
		]
		
		y_offset = cell_number * cell_size // 2 - 50
		for line in inst_lines:
			if line:
				line_text = game_font.render(line, True, (255,255,255))
				line_rect = line_text.get_rect(center=(cell_number * cell_size // 2, y_offset))
				inst_surface.blit(line_text, line_rect)
			y_offset += 25
		
		screen.blit(inst_surface, (0,0))

	def load_high_score(self):
		try:
			with open('Snake/highscore.txt', 'r') as f:
				return int(f.read().strip())
		except:
			return 0

	def save_high_score(self):
		with open('Snake/highscore.txt', 'w') as f:
			f.write(str(self.high_score))

	def get_difficulty_name(self):
		if self.speed == 200:
			return 'Easy'
		elif self.speed == 150:
			return 'Medium'
		else:
			return 'Hard'

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40
cell_number = 20
# Set up display first
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
pygame.display.set_caption("Snake Game")  # Set window title
# Load apple for game (after display is created)
apple = pygame.image.load(os.path.join(SCRIPT_DIR, 'Graphics/apple.png')).convert_alpha()
clock = pygame.time.Clock()
try:
    game_font = pygame.font.Font(os.path.join(SCRIPT_DIR, 'Font/PoetsenOne-Regular.ttf'), 25)
except:
    game_font = pygame.font.SysFont(None, 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game = MAIN()

# Main game loop - runs at 60 FPS
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if main_game.state == 'playing':
			if event.type == SCREEN_UPDATE and not main_game.paused:
				main_game.update()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					main_game.paused = not main_game.paused
				if event.key == pygame.K_UP:
					if main_game.snake.direction.y != 1:
						main_game.snake.direction = Vector2(0,-1)
				if event.key == pygame.K_RIGHT:
					if main_game.snake.direction.x != -1:
						main_game.snake.direction = Vector2(1,0)
				if event.key == pygame.K_DOWN:
					if main_game.snake.direction.y != -1:
						main_game.snake.direction = Vector2(0,1)
				if event.key == pygame.K_LEFT:
					if main_game.snake.direction.x != 1:
						main_game.snake.direction = Vector2(-1,0)
		elif main_game.state == 'menu':
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					main_game.selected_option = (main_game.selected_option - 1) % 4
				if event.key == pygame.K_DOWN:
					main_game.selected_option = (main_game.selected_option + 1) % 4
				if event.key == pygame.K_RETURN:
					if main_game.selected_option == 0:  # Start Game
						pygame.time.set_timer(SCREEN_UPDATE, main_game.speed)
						main_game.state = 'playing'
					elif main_game.selected_option == 1:  # Difficulty
						if main_game.speed == 200:
							main_game.speed = 150
						elif main_game.speed == 150:
							main_game.speed = 100
						else:
							main_game.speed = 200
					elif main_game.selected_option == 2:  # Sound
						main_game.sound_enabled = not main_game.sound_enabled
					elif main_game.selected_option == 3:  # Quit
						pygame.quit()
						sys.exit()
				if event.key == pygame.K_i:
					main_game.state = 'instructions'
		elif main_game.state == 'instructions':
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_m:
					main_game.state = 'menu'
		elif main_game.state == 'game_over':
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					main_game.snake.reset()
					main_game.snake.direction = Vector2(1,0)  # Start moving right
					main_game.state = 'playing'
				if event.key == pygame.K_m:
					main_game.snake.reset()
					main_game.state = 'menu'
				if event.key == pygame.K_q:
					pygame.quit()
					sys.exit()

	if main_game.state == 'playing':
		screen.fill((175,215,70))
		main_game.draw_elements()
		if main_game.paused:
			# Draw pause overlay
			pause_surface = pygame.Surface((cell_number * cell_size, cell_number * cell_size))
			pause_surface.set_alpha(128)  # Semi-transparent
			pause_surface.fill((0,0,0))
			screen.blit(pause_surface, (0,0))
			pause_text = game_font.render('PAUSED', True, (255,255,255))
			pause_rect = pause_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2))
			screen.blit(pause_text, pause_rect)
	elif main_game.state == 'menu':
		main_game.draw_menu()
	elif main_game.state == 'game_over':
		main_game.draw_game_over()
	elif main_game.state == 'instructions':
		main_game.draw_instructions()
	
	pygame.display.update()
	clock.tick(60)