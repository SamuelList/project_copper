import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
import random
from weapon import Weapon


class Level:
	def __init__(self):
		# get the display surface
		self.display_surface = pygame.display.get_surface()
		
		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		
		# sprite setup
		self.create_map()
		
	def create_attack(self):
		Weapon(self.player, [self.visible_sprites])
		
		
		
		
	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('map/map_Grass.csv'),
			'object': import_csv_layout('map/map_Objects.csv'),
		}
		graphics = {
			'grass': import_folder('graphics/grass'),
			'objects': import_folder('graphics/objects'),
		}
		for style, layout in layouts.items():
			# create the map
			for row_index, row in enumerate(layout):
				for col_index, tile in enumerate(row):
					if tile != '-1':
						x = col_index * TILE_SIZE
						y = row_index * TILE_SIZE
						
						if style == 'boundary':
							Tile((x, y), (self.obstacle_sprites), 'invisible')
							
						if style == 'grass':
							# create grass tile
							random_grass = random.choice(graphics['grass'])
							Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'grass', random_grass)
							
						if style == 'object':
							# create objects
							if tile in get_path('graphics/objects'):
								object_path = f'graphics/objects/{tile}.png'
								surface = pygame.image.load(object_path).convert_alpha()
								Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'object', surface)

		self.player = Player((2000, 1430), (self.visible_sprites), self.obstacle_sprites, self.create_attack)
					
			
			
	def run(self):
		# update and delete the game
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		debug(self.player.status)
		debug(self.player.speed, 660, 10)
		
		# show sprint value
		debug(f'Sprint {int(self.player.sprint)}%', 690, 10)

		
		
class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		
		# general setup
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()
		
		# creating floor
		self.floor_surface = pygame.image.load('graphics/tilemap/Small school 1.2.bmp').convert()
		self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

	def custom_draw(self, player):
		# getting the offset
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height
		
		# draw floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surface, floor_offset_pos)
		
		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, offset_pos)
