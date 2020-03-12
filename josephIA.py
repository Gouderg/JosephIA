import sys
sys.path.append('./game')
from tictactoe import ticTacToe

if __name__ == '__main__':
	print("\t Bienvenue dans l'antre de Joseph, à quoi voulez-vous jouer?: ")
	print("1- Tictactoe")
	print("2- Connect 4")

	while True:
		choix = input('Votre choix: ')

		if len(choix) == 1 and ord(choix) >= 49 and ord(choix) <= 50:
			if int(choix) == 1: 
				ticTacToe()
				break
			elif int(choix) == 2: 
				print('Work in Progress')
				break
		print("Mauvaise Saisie")

	print('\t Joseph a hâte de vous revoir.')