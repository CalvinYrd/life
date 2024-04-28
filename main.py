from os import (
	name as os_name,
	system, mkdir, listdir
)
from os.path import exists as file_exists
from json import (
	loads as json_decode,
	dumps as json_encode
)
from re import (
	compile as re_compile,
	match as re_match,
	error as re_error
)
from copy import deepcopy
from time import sleep
from msvcrt import getch

# teste la validité d'un regex
def regex_match(regex, string):
	try:
		re_compile(regex)
		return re_match(regex, string)
	except re_error:
		return False

# teste la validité d'un nom de fichier (syntaxe + existance)
def filename_is_valid(path):
	path = path.replace("\\", "/")
	filename = path.split("/")[-1]
	return regex_match(r"^[^./\\]+$", filename)

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
white_color = rgb((255, 255, 255, "color"))
black_bg = rgb((0, 0, 0, "background"))
red_bg = rgb((255, 0, 0, "background"))
red_color = rgb((255, 0, 0, "color"))
grey_bg = rgb((20, 20, 20, "background"))

# dessine une grille
def draw_grid(grid, iteration, fps, cursor = None):
	new_grid = deepcopy(grid)
	res = ""

	for line_index in range(len(grid)):
		# dessin de chaque cellule
		for cell_index in range(len(grid[line_index])):
			# cas du curseur
			if (cursor != None and line_index == cursor["y"] and cell_index == cursor["x"]): col = red_bg
			# cellule vivante
			elif (new_grid[line_index][cell_index]): col = white_bg
			# cellule morte
			else: col = black_bg

			# dessin cellule
			res += col + "  "

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

		res += "\n"+grey_bg

	if (iteration != None): output = f"Génération n°{iteration + 1}\n"
	else: output = f"Tappez <x> pour quitter l'éditeur \nTappez <+> pour sauvegarder le modèle\n"
	output += res

	clear()
	print(output)
	sleep(1 / fps)
	return new_grid

# efface l'ecran
if (os_name == "nt"):
	clear = lambda: system("cls")
else:
	clear = lambda: system("clear")

try:
	# variables de base
	iteration = 1
	fps = 60

	# generation de la grille
	grid = []
	width = height = 65
	for i in range(height): grid.append([0 for i in range(width)])

	w = h = 0 # coordonnées du curseur
	k = None  # touche

	while (k != "x"):
		try:
			draw_grid(grid, None, fps, {"x": w, "y": h})
			print(f"x : {w} . y : {h}")
			k = getch().decode()

			# mapping touches
			if (k == "d"): w += 1
			elif (k == "q"): w -= 1
			elif (k == "z"): h -= 1
			elif (k == "s"): h += 1
			elif (k in (" ", "\r")):
				if (grid[h][w] == 1): grid[h][w] = 0
				else: grid[h][w] = 1
			elif (k == "+"):
				# créer le dossier des sauvegardes s'il n'éxiste pas
				if (not file_exists("saves")): mkdir("saves")
				clear()
				valid = False

				while (not valid):
					save = input("Saisissez le nom de la sauvegarde :\n> ")
					save = "saves/"+save+".json"

					# si le nom est valide on créé et remplit la sauvegarde
					valid = filename_is_valid(save)
					input(valid)

					if (valid):
						input(json_encode(grid))
						# ...

					else:
						clear()
						print(f"{red_color}Le nom est invalide ou déjà éxistant{white_color}\n")

		except UnicodeDecodeError:
			continue

	# démarrage de la vie
	while (True):
		grid = draw_grid(grid, iteration, fps)
		iteration += 1

except KeyboardInterrupt:
	print(black_bg)
	clear()
