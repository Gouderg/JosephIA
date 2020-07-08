import os
from math import inf
from player import Player

p1 = Player('You', '\033[31;1mx\033[0m') # turn = 1
p2 = Player('Joseph', '\033[33;1mo\033[0m') #turn = 0

#Créer la table de jeu
def initTable():
	return [[' '] * 3 for i in range(3)]

#Affiche le jeu
def display(table):
	os.system('clear')
	for i in range(3):
		print('\t\t|',table[2 - i][0],'|',table[2 - i][1],'|',table[2 - i][2],'|')
		if i != 2: print('\t\t-------------')

#Vérifie si la colonne est gagnante
def checkCol(table, tag):
	for i in range(3):
		if table[0][i] == table[1][i] == table[2][i] and table[1][i] == tag:
			return True
	return False

#Vérifie si la ligne est gagnante
def checkLig(table, tag):
	for i in range(3):
		if table[i][0] == table[i][1] == table[i][2] and table[i][0] == tag:
			return True
	return False

#Vérifie si la diagonale est gagnante
def checkDiag(table, tag):
	if (table[0][0] == table[1][1] == table[2][2] or table[0][2] == table[1][1] == table[2][0]) and table[1][1] == tag:
		return True
	return False

#Vérifie si la partie est gagné:
def gameOver(table,tag):
	if checkLig(table,tag) or checkCol(table,tag) or checkDiag(table,tag):
		return True
	return False

#Vérifie si la partie est nulle
def gameDraw(table):
	for i in range(3):
		for j in range(3):
			if table[i][j] == ' ':
				return False
	return True

#Demande à l'utilisateur de saisir une valeur
def takePlace(table):
	while True:
		place = input("Saisissez une valeur: ")

		if len(place) == 1 and ord(place) >= 49 and ord(place) <= 57:
			if checkPlace(table, int(place)):
				return int(place)
			print("Place déjà occupée.")
		print("Utilisez le pavé tactile.")

#Renvoie la position X de la place:
def getX(place):
	return (place-1)//3

#Renvoie la position Y de la place:
def getY(place):
	return (place-1)%3
	
#Vérifie si la place est libre
def checkPlace(table, place):
	if table[getX(place)][getY(place)] == ' ':
		return True
	return False

#Remplie le tableau
def putTable(table, place, tag):
	table[getX(place)][getY(place)] = tag
	return table

#Vide le tableau de la valeur
def unPutTable(table, place):
	table[getX(place)][getY(place)] = ' '
	return table
#Renvoie le joueur adverse
def getOpponent(player):
	return p2 if player == p1 else p1

#Cherche les coups possibles
def movesAvailable(table):
	moves = []
	for i in range(1,10):
		if checkPlace(table, i):
			moves.append(i)
	return moves

#Choisi qui commence la partie
def whoStart():
	while True:
		who = input("Qui commence (1: Vous, 0: Joseph): ")
		if len(who) == 1 and ord(who) >= 48 and ord(who) <= 49:
			return int(who)
		print("Mauvaise saisie.")

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
		table = putTable(table, move, player.tag)
		result, _ = minimax(table, getOpponent(player), depth + 1)
		table = unPutTable(table, move)
		if player == p2:
			if result > best:
				best, bestMove = result, move
		else:
			if result < best:
				best, bestMove = result, move
	
	return best, bestMove

#Algorithme alphabeta
def alphabeta(table, player, alpha, beta, depth = 0):
	bestMove = None
	best = 10 if getOpponent(player) == p2 else -10

	if gameOver(table, p1.tag): 
		return best + depth, None
	elif gameDraw(table):  
		return 0, None
	elif gameOver(table, p2.tag):  
		return best - depth, None

	for move in movesAvailable(table):
		table = putTable(table, move, player.tag)
		result, _ = alphabeta(table, getOpponent(player), alpha, beta, depth + 1)
		table = unPutTable(table, move)
	
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

#Fonction principale du jeu
def ticTacToe():
	table = initTable()
	display(table)

	turn = whoStart()
	alpha = - inf
	beta = inf

	while True:
		if gameOver(table, p1.tag):
			print("Vous avez gagné.", end = "\n\n")
			break
		elif gameOver(table, p2.tag):
			print(p2.name,"a gagné.", end = "\n\n")
			break
		elif gameDraw(table):
			print("Partie Nulle.", end = "\n\n")
			break

		if turn:
			place = takePlace(table)
			table = putTable(table, place, p1.tag)
		else:
			#_ , place = minimax(table, p2)
			_ , place = alphabeta(table, p2, alpha, beta)
			table = putTable(table, int(place), p2.tag)

		display(table)
		turn = not(turn)

	