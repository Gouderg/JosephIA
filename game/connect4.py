from player import Player
import os

#Initialise la table de jeu
def initTable():
	return [[' '] * 7 for i in range(7)]
	'''return [['o', 'o', 'o', 'x', 'x', 'o', 'o'], 
			['o', 'x', 'o', 'x', 'o', 'x', 'x'], 
			['x', 'x', 'x', 'o', 'o', 'o', 'x'], 
			['x', 'o', 'x', 'x', 'x', 'o', 'o'], 
			['x', 'o', 'o', 'x', 'o', 'x', 'x'], 
			['o', 'x', 'o', 'x', 'o', 'o', 'x'], 
			[' ', ' ', ' ', ' ', ' ', ' ', ' ']]'''

#Affiche le jeu
def display(table):
	#os.system('clear')
	for i in range(7):
		print('|',table[6-i][0],'|',table[6-i][1],'|',table[6-i][2],'|',table[6-i][3],'|',table[6-i][4],'|',table[6-i][5],'|',table[6-i][6],'|')
		if i != 6: print('-----------------------------')
	print('  1   2   3   4   5   6   7')

#Prends le choix de l'utilisateur
def takePlace(table):
	while True:
		place = input("\nVeuillez saisir une position: ")
		if len(place) == 1 and ord(place) >= 49 and ord(place) <= 55:
			if(checkPlace(table,int(place)) != None):
				return int(place)			
			print("Colonne pleine")
		print("Utilisez les chiffres entre 1-7")

#Regarde s'il y a de la place dans la colonne
def checkPlace(table, x):
	for i in range(7):
		if table[i][x-1] == ' ':
			return i
	return None 

#Remplie la colonne selon la place disponible
def fillTab(table, x, tag):
	for i in range(7):
		if table[i][x-1] == ' ':
			table[i][x-1] = tag;
			break
	return table

#Vide le tableau
def unFillTab(table, x,i):
	table[i][x-1] = ' '
	return table

#Regarde si 4 pions en colonne sont gagnants
def checkCol(table, ligne, tag):
	for i in range (4):
		if (table[ligne][i] == table[ligne][i + 1] == table[ligne][i + 2] == table[ligne][i + 3]) and (table[ligne][i] == tag):
			return True
	return False

#Regarde si 4 pions en ligne sont gagnants
def checkLig(table, ligne, tag):
	for i in range (4):
		if (table[i][ligne] == table[i + 1][ligne] == table[i + 2][ligne] == table[i + 3][ligne]) and (table[i][ligne] == tag):
			return 1
	return 0

#Regarde si une diagonale est gagnante
def checkDiag(table, tag):
	for i in range(4):
		for j in range(4):
			if ((table[i][6-j] == table[i + 1][5 - j] == table[i + 2][4 - j] == table[i + 3][3-j]) and (table[i][6 - j] == tag)) or ((table[i][j] == table[i + 1][1 + j] == table[i + 2][2 + j] == table[i + 3][3 + j]) and (table[i][j] == tag)):
				return True
	return False

#Regarde si le jeu est fini
def gameOver(table, tag):
	for j in range(7):
		if checkCol(table, j, tag) or checkLig(table, j, tag):
			return True
	return checkDiag(table, tag)
	
#Regarde si la table est pleine
def gameDraw(table):
	for i in range(7):
		for j in range(7):
			if table[i][j] ==' ': return False
	return True

#Renvoie le joueur adverse
def getOpponent(player):
	return p2 if player == p1 else p1

#Cherche les coups possibles
def movesAvailable(table):
	moves = []
	for i in range(1,8):
		if checkPlace(table, i) != None:
			moves.append(i)
	return moves

#Algorithme minimax
def minimax(table, player, depth = 0):
	bestMove = None
	best = 10 if getOpponent(player) == p2 else -10

	if gameOver(table, p1.tag): 
		return best + depth, None
	elif gameDraw(table):
		return 0, None
	elif gameOver(table, p2.tag):  
		return best - depth, None

	for move in movesAvailable(table):
		table = fillTab(table, move, player.tag)
		result, _ = minimax(table, getOpponent(player), depth + 1)

		if checkPlace(table, move) == None:
			table = unFillTab(table, move, 6)
		else:
			table = unFillTab(table, move, checkPlace(table, move)-1)
		
		if player == p2:
			if result > best:
				best, bestMove = result, move
		else:
			if result < best:
				best, bestMove = result, move

	return best, bestMove

if __name__ == '__main__':
	
	p1 = Player('Victor', 'x')
	p2 = Player('Joseph4', 'o')

	turn = 0
	table = initTable()
	display(table)


	while True:

		if gameOver(table, p1.tag):
			print(p1.name,'a gagné')
			break
		elif gameOver(table, p2.tag):
			print(p2.name,'a gagné')
			break
		elif gameDraw(table):
			print("Partie nulle")
			break


		if turn: 
			place = takePlace(table)
		else:
			print('Moulinage...')
			_ , place = minimax(table, p2)
			   

		table = fillTab(table, place, p1.tag if turn else p2.tag)
		display(table)
		turn = not(turn)

		
	