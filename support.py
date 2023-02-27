from csv import reader
from os import walk
import pygame


def import_csv_layout(path):
	"""Import a csv file and return a list of lists."""
	terrain_map = []
	with open(path) as file:
		layout = reader(file, delimiter=',')
		for row in layout:
			terrain_map.append(row)
	return terrain_map


def import_folder(path):
	"""Import a folder and return a list of file names."""
	surface_list = []
	for _, __, img in walk(path):
		for image in img:
			full_path = path + '/' + image
			image_surface = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surface)
	return surface_list

def get_path(path):
	"""Import a folder and return a list of file names."""
	surface_list = []
	for _, __, img in walk(path):
		for item in img:
			image = item.split('.')[0]
			surface_list.append(image)

	return surface_list

# print(get_path('graphics/objects'))
