import sys
sys.path.append('./game')
from tictactoe import ticTacToe
from connect4 import connect4
from sudoku import sudoku

if __name__ == '__main__':
	print("\t Bienvenue dans l'antre de Joseph, à quoi voulez-vous jouer?: ")
	print("1- Tictactoe")
	print("2- Connect 4")
	print("3- Sudoku")

	while True:
		choix = input('Votre choix: ')

		if len(choix) == 1 and ord(choix) >= 49 and ord(choix) <= 51:
			if int(choix) == 1: 
				ticTacToe()
				break
			elif int(choix) == 2: 
				connect4()
				break
			elif int(choix) == 3: 
				sudoku()
				break
		print("Mauvaise Saisie")

	print('\t Joseph a hâte de vous revoir.', end = "\n\n\n")