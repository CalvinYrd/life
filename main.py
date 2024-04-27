from os import (
	name as os_name,
	system
)
from copy import deepcopy
from time import sleep

# retourne une création de couleur rgb
def rgb(colors):
	# vérification des paramètres
	for p in (colors[:-1]):
		if (type(p) != int):
			raise Exception('La valeur "'+p+'" doit être de type <int>')
		elif (p > 255 or p < 0):
			raise Exception('La valeur "'+p+'" est trop petite ou trop grande: les paramètres "r", "g" et "b" doivent tous être compris entre 0 et 255')

	if (colors[-1] not in ("color", "background")):
		raise Exception('Le dernier paramètre est invalide, il doit être soit "color" ou "background"')
	else:
		x = str([38 if colors[-1] == "color" else 48][0])
		return f'\x1b[{x};2;{colors[0]};{colors[1]};{colors[2]}m'

white_bg = rgb((255, 255, 255, "background"))
black_bg = rgb((0, 0, 0, "background"))

# dessine une grille
def draw_grid(grid, iteration, fps):
	global white_bg, black_bg
	new_grid = deepcopy(grid)
	res = ""

	for line_index in range(len(grid)):
		for cell_index in range(len(grid[line_index])):
			# dessin de chaque cellule
			if (new_grid[line_index][cell_index]): res += white_bg + "  "
			else: res += black_bg + "  "

			# compter le nombre de celulles voisines mortes et vivantes
			around_cells = 0

			# parcourir les voisins
			for y in range(line_index - 1, line_index + 2):
				for x in range(cell_index - 1, cell_index + 2):
					# s'assurer qu'on est pas out of range et ignorer la cellule actuelle (non voisine) et incrémenter les celulles vivantes si vivant
					if (
						(y != line_index or x != cell_index)
						and 0 <= y < len(grid) and 0 <= x < len(grid[y])
						and grid[y][x] == 1
					):
						around_cells += 1

			# recalcul du nouvel état des cellules
			# si la cellulle est morte et que exactement 3 voisines sont vivantes, celle-ci nait
			if (grid[line_index][cell_index] == 0 and around_cells == 3):
				new_grid[line_index][cell_index] = 1

			# si la cellule est vivante et qu'il y a plus de 3 ou moins de 2 voisines vivantes, celle-ci meurt (sur/sous population)
			if (grid[line_index][cell_index] == 1 and (around_cells > 3 or around_cells < 2)):
				new_grid[line_index][cell_index] = 0

		res += "\n"

	clear()
	print(f"Itération : {iteration + 1}\n{res}")
	sleep(1 / fps)
	return new_grid

# efface l'ecran
if (os_name == "nt"):
	clear = lambda: system("cls")
else:
	clear = lambda: system("clear")

# variables de base
width = height = 50
iteration = 3000
fps = 60

# generation de la grille
grid = []
for i in range(height): grid.append([0 for i in range(width)])

# définition de départ
grid[15][15] =\
grid[15][16] =\
grid[15][17] =\
grid[14][17] =\
grid[13][16] =\
1

# démarrage de la vie
for iteration in range(iteration):
	grid = draw_grid(grid, iteration, fps)
