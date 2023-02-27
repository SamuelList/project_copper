import pygame
from settings import *
from debug import debug
from support import *


class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacle_sprites, create_attack):
		super().__init__(groups)
		self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(0, -26)
		
		self.direction = pygame.math.Vector2()
		
		# movement
		self.speed = player_speed
		self.sprint = sprint_max
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None
		self.create_attack = create_attack
		
		# graphic setup
		self.import_player_assets()
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.10
		self.poop = 'my balls'
		

		self.obstacle_sprites = obstacle_sprites
		
	def get_status(self):
		
		# player idle
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'
				
		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle', '_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack', '')
		
	def import_player_assets(self):
		character = 'graphics/player/'
		self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'up_idle': [], 'down_idle': [],
		                   'left_idle': [], 'right_idle': [], 'up_attack': [], 'down_attack': [], 'left_attack': [],
		                   'right_attack': []}
		
		for animation in self.animations.keys():
			full_path = character + animation
			self.animations[animation] = import_folder(full_path)
		print(self.animations['down'])
		
	def input(self):
		# get the pressed keys
		keys = pygame.key.get_pressed()
		if not self.attacking:
			# check for input
			if keys[pygame.K_w]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_s]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0
			
			if keys[pygame.K_a]:
				self.direction.x = -1
				self.status = 'left'
			elif keys[pygame.K_d]:
				self.direction.x = 1
				self.status = 'right'
			else:
				self.direction.x = 0
				
			# sprint
			# if self.sprint > 0 and 'idle' not in self.status:
			# 	if keys[pygame.K_LSHIFT]:
			# 		self.speed = sprint_speed
			# 		self.animation_speed = (sprint_speed / 26.66)
			# 		self.sprint -= sprint_drain
			# 		if self.sprint <= 0:
			# 			self.speed = player_speed
			# 			self.animation_speed = (player_speed / 26.66)
			# 	else:
			# 		self.speed = player_speed
			# 		self.animation_speed = (player_speed / 26.66)

				
		# attack
		if keys[pygame.K_SPACE]:
			self.attacking = True
			self.attack_time = pygame.time.get_ticks()
			self.create_attack()
	
		# magic
		if keys[pygame.K_e]:
			self.attacking = True
			self.attack_time = pygame.time.get_ticks()
			print('magic')
			
	def move(self, speed):
		if self.direction.magnitude() != 0:
			# normalize the direction
			self.direction = self.direction.normalize()
			
		# move the player
		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center
		
	def collision(self, direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0:  # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:  # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0:  # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:  # moving up
						self.hitbox.top = sprite.hitbox.bottom
						
	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False
				# self.attack_time = None
		
	def animate(self):
		# get the current animation
		animation = self.animations[self.status]
		
		# loop over the frame indexes
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
		
		# set the image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center=self.hitbox.center)
		
	def update(self):
		self.input()
		self.move(self.speed)
		self.cooldowns()
		self.get_status()
		self.animate()
		if self.sprint < sprint_max:
			self.sprint += sprint_recharge
		