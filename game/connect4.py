from player import Player
from math import inf
import os

#Constante
NB_COL = 7
NB_ROW = 6

p1 = Player('You', '\033[31;1mx\033[0m') # turn = 1
p2 = Player('Joseph', '\033[33;1mo\033[0m') #turn = 0

#Initialise la table de jeu
def initTable():
	return [[' '] * NB_COL for i in range(NB_ROW)]

#Affiche le jeu
def display(table):
	os.system('clear')
	for i in range(NB_ROW):
		print("|", end=' ')
		for j in range(NB_COL):
			print(table[NB_ROW-1-i][j], "|", end=' ')
		print(end='\n')
		if i != 5: print('-----------------------------')
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
	for i in range(NB_ROW):
		if table[i][x-1] == ' ':
			return i
	return None 

#Remplie la colonne selon la place disponible
def fillTab(table, x, tag):
	for i in range(NB_ROW):
		if table[i][x-1] == ' ':
			table[i][x-1] = tag;
			break
	return table

#Vide le tableau
def unFillTab(table, x, i):
	table[i][x-1] = ' '
	return table

#Regarde si 4 pions en colonne sont gagnants
def checkLig(table, ligne, tag):
	for i in range(NB_COL-3):
		if (table[ligne][i] == table[ligne][i + 1] == table[ligne][i + 2] == table[ligne][i + 3]) and (table[ligne][i] == tag):
			return True
	return False

#Regarde si 4 pions en ligne sont gagnants
def checkCol(table, ligne, tag):
	for i in range(NB_ROW-3):
		if (table[i][ligne] == table[i + 1][ligne] == table[i + 2][ligne] == table[i + 3][ligne]) and (table[i][ligne] == tag):
			return True
	return False

#Regarde si une diagonale est gagnante
def checkDiag(table, tag):
	for i in range(NB_ROW-3):
		for j in range(NB_COL-3):
			if ((table[i][6-j] == table[i + 1][5 - j] == table[i + 2][4 - j] == table[i + 3][3-j]) and (table[i][6 - j] == tag)) or ((table[i][j] == table[i + 1][1 + j] == table[i + 2][2 + j] == table[i + 3][3 + j]) and (table[i][j] == tag)):
				return True
	return False

#Regarde si le jeu est fini
def gameOver(table, tag):
	for j in range(NB_COL):
		if checkCol(table, j, tag): return True
	for i in range(NB_ROW):
		if checkLig(table, i, tag): return True
	return checkDiag(table, tag)
	
#Regarde si la table est pleine
def gameDraw(table):
	for i in range(NB_ROW-3):
		for j in range(NB_COL):
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

#Permet de savoir qui commence
def whoStart():
	while True:
		who = input("Qui commence (1: Vous, 0: Joseph): ")
		if len(who) == 1 and ord(who) >= 48 and ord(who) <= 49:
			return int(who)
		print("Mauvaise saisie.")

#Retourne une valeur en fonction de l'intéret du coup
def countQuadruplet(quads):
	valeur = 0
	for quad in quads:

		if (p1.tag in quad and p2.tag in quad) or (' ' in quad and p2.tag not in quad and p1.tag not in quad): 
			valeur += 0

		elif (p2.tag in quad and p1.tag not in quad):
			oVal = quad.count(p2.tag) 
			if oVal == 1: valeur += 1
			elif oVal == 2: valeur += 10
			elif oVal == 3: valeur += 1000
			elif oVal == 4: valeur += 100000

		elif (p1.tag in quad and p2.tag not in quad):
			xVal = quad.count(p1.tag)
			if xVal == 1: valeur -= 1
			elif xVal == 2: valeur -= 10
			elif xVal == 3: valeur -= 500

	return valeur

#Evalue la situation autour de lui
def evalCurrentTable(table):
	quad = []
	#Check et stock les quadruplets en colonne
	for ligne in range(NB_COL):
		for i in range(NB_ROW-3):
			col = []
			col.append(table[i][ligne])
			col.append(table[i + 1][ligne])
			col.append(table[i + 2][ligne])
			col.append(table[i + 3][ligne])
			quad.append(col)
	#Check et stock les quadruplets en ligne
	for ligne in range(NB_ROW):
		for i in range(NB_COL-3):
			lig = []
			lig.append(table[ligne][i])
			lig.append(table[ligne][i + 1])
			lig.append(table[ligne][i + 2])
			lig.append(table[ligne][i + 3])
			quad.append(lig)
	#Check et stock les quadruplets en diagonale
	for i in range(NB_ROW-3):
		for j in range(NB_COL-3):
			diag = []
			diag.append(table[i][6 - j])
			diag.append(table[i + 1][5 - j])
			diag.append(table[i + 2][4 - j])
			diag.append(table[i + 3][3 - j])
			quad.append(diag)
			diag = []
			diag.append(table[i][j])
			diag.append(table[i + 1][j + 1])
			diag.append(table[i + 2][j + 2])
			diag.append(table[i + 3][j + 3])
			quad.append(diag)

	return countQuadruplet(quad)
	

#Algorithme AlphaBeta
def alphabeta(table, player, alpha = -inf, beta = inf, depth = 0, depthMax = 6):
	bestMove = None
	best = 100000 if getOpponent(player) == p2 else -100000

	if gameOver(table, p1.tag): 
		return best + depth, None
	elif gameDraw(table):
		return 0, None
	elif gameOver(table, p2.tag):  
		return best - depth, None
	elif depthMax == 0:
		return evalCurrentTable(table), None

	for move in movesAvailable(table):
		table = fillTab(table, move, player.tag)
		result, _ = alphabeta(table, getOpponent(player), alpha, beta, depth + 1, depthMax - 1)

		if checkPlace(table, move) == None:
			table = unFillTab(table, move, NB_COL-2)
		else:
			table = unFillTab(table, move, checkPlace(table, move)-1)
		
		if player == p2:
			if result > best:
				best, bestMove = result, move
			if best >= beta:
				return best, move
			alpha = max(alpha, result)
		else:
			if result < best:
				best, bestMove = result, move
			if best <= alpha:
				return best, move
			beta = min(beta, result)

	return best, bestMove

#Fonction principal
def connect4():
	table = initTable()
	display(table)
	turn = whoStart()

	while True:
		if gameOver(table, p1.tag):
			print('Vous avez gagné')
			break
		elif gameOver(table, p2.tag):
			print(p2.name,'a gagné')
			break
		elif gameDraw(table):
			print("Partie nulle")
			break

		if turn: 
			place = takePlace(table)
			#_, place = alphabeta(table, p1)
		else:
			print('Joseph réfléchi...')
			_, place = alphabeta(table, p2)
			   

		# table = fillTab(table, place, p1.couleur if turn else p2.couleur)
		table = fillTab(table, place, p1.tag if turn else p2.tag)
		display(table)
		turn = not(turn)
