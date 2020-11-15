import os
import time

SIZE = 9

# Initialise la table de jeu
def initTable():
	return [[' '] * 9 for i in range(9)]

# Génère un sudoku facile
def loadSudoku(table):
	table[0][0] = 5
	table[1][0] = 6
	table[3][0] = 8
	table[4][0] = 4
	table[5][0] = 7
	
	table[0][1] = 3
	table[2][1] = 9
	table[6][1] = 6
	
	table[2][2] = 8
	
	table[1][3] = 1
	table[4][3] = 8
	table[7][3] = 4
	
	table[0][4] = 7
	table[1][4] = 9
	table[3][4] = 6
	table[5][4] = 2
	table[7][4] = 1
	table[8][4] = 8
	
	table[1][5] = 5
	table[4][5] = 3
	table[7][5] = 9

	table[6][6] = 2

	table[2][7] = 6
	table[6][7] = 8
	table[8][7] = 7

	table[3][8] = 3
	table[4][8] = 1
	table[5][8] = 6
	table[7][8] = 5
	table[8][8] = 9

	return table

#Génère un sudoku moyen
def loadSudoku2(table):

	table[3][0] = 7
	table[4][0] = 2

	table[0][1] = 6
	table[4][1] = 1
	table[7][1] = 4

	table[4][2] = 5
	table[3][2] = 3
	table[4][2] = 8

	table[3][3] = 6
	table[6][3] = 4
	table[7][3] = 7

	table[1][5] = 2
	table[5][5] = 3
	table[6][5] = 8
	table[7][5] = 5

	table[0][6] = 4
	table[2][6] = 9
	table[5][6] = 1
	table[6][6] = 6

	table[0][7] = 1

	table[0][8] = 5
	table[6][8] = 2
	table[8][8] = 9

	return table


# Affiche la sudoku
def display(table):
	#os.system('clear')
	for i in range(SIZE):
		for j in range(SIZE):
			if (j)%3 == 0 and j != 0: 
				print("\033[32;1m||\033[0m", table[i][j], end=" ")
			else:
				print('\033[37;1m|\033[0m', table[i][j], end=" ")
		print("\033[37;1m|\033[0m")
		if i != SIZE-1 and (i+1)%3 != 0: print('\033[37;1m---------------------------------------\033[0m')
		elif i != SIZE-1 and (i+1)%3 == 0: print('\033[32;1m_______________________________________\033[0m')

	#time.sleep(0.1)

# Check la colonne, renvoie vrai si la valeur à son homologue
def checkCol(table, oldI, oldJ):
	for i in range(9):
		if table[oldI][oldJ] == table[i][oldJ] and oldI != i:
			return True
	return False

# Check la ligne, renvoie vrai si la valeur à son homologue
def checkLig(table, oldI, oldJ):
	for j in range(9):
		if table[oldI][oldJ] == table[oldI][j] and oldJ != j:
			return True
	return False

# Check si la table est remplie en parcourant chaque case du tableau
def checkFill(table):
	for i in table:
		for j in i:
			if j == ' ':
				return False
	return True

# Check si la somme des termes d'un carré est égale à 45
def checkSquare(table):
	for i in range(1,8,3):
		valeur = 0
		for j in range(1,8,3):
			valeur = table[i-1][j-1] + table[i-1][j] + table[i-1][j+1] + table[i][j-1] + table[i][j] + table[i][j+1] + table[i+1][j-1] + table[i+1][j] + table[i+1][j+1]
			if valeur != 45:
				return False
	return True

# Check si le sudoku est bien remplie
def gameWin(table):
	if checkFill(table):          
		for i in range(SIZE):
			for j in range(SIZE):
				if checkLig(table, i, j) and checkCol(table, i, j):
					return False
		return checkSquare(table)
	return False

# Check la présence d'un chiffre dans une ligne
def checkNumberLig(table, j, number):
	return not(number in table[j])

# Check la présence d'un chiffre dans une colonne
def checkNumberCol(table, i, number):
	for col in range(SIZE):
		if number == table[col][i]:
			return False
	return True
	
# Check la présence d'un chuffre dans son carré
def checkNumberSquare(table, i, j, number):
	
	# On cherche la position du j
	if (j + 1) in [1,4,7]:
		newJ = j + 1
	elif (j - 1) in [1,4,7]:
		newJ = j - 1
	else:
		newJ = j

	# On cherche la position du i
	if (i + 1) in [1,4,7]:
		newI = i + 1
	elif (i - 1) in [1,4,7]:
		newI = i - 1
	else:
		newI = i

	for a in range (newI-1, newI+2):
		for b in range (newJ-1, newJ+2):
			if table[a][b] == number:
				return False
	return True


# Check les chiffres possibles dans la colonne, dans la ligne et dans le carré
def movesAvailable(table, i, j):
	move = []
	for number in range(1,10,1):
		if checkNumberLig(table, i, number) and checkNumberCol(table, j, number) and checkNumberSquare(table, i, j, number):
			move.append(number)
	return move


# Résout le sudoku
def backtracking(table, i, j):

	# Condition de sortie
	if gameWin(table):
		return True


	#On parcourt la possibilité des cas 
	if table[i][j] == ' ': 	
		for move in movesAvailable(table, i, j):
			if not(move):
				return False
			table[i][j] = move

			if i == 8 and j == 8:
				if gameWin(table):
					return True
			else:
				retour = backtracking(table, (i+1)%SIZE, j+1 if not((i+1)%SIZE) and i != 0 else j)
				if retour:
					return True
				else: 
					table[i][j] = ' '
	else:
		retour = backtracking(table, (i+1)%SIZE, j+1 if not((i+1)%SIZE) and i != 0 else j)
		if retour:
				return True

	return False	

def sudoku():

	table = initTable()
	table = loadSudoku2(table)


	display(table)
	print("Work in progress ..")
	_ = backtracking(table, 0, 0)
	display(table)

	
	if gameWin(table):
		print("Vous avez résolu le sudoku")
	else:
		print("Votre sudoku n'est pas valide")

