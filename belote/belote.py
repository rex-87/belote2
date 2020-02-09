# -*- coding: utf-8 -*-
"""
	belote
	
	This project is an example of a Python project generated from cookiecutter-python.
"""

## -------- COMMAND LINE ARGUMENTS ---------------------------
## https://docs.python.org/3.7/howto/argparse.html
import argparse
CmdLineArgParser = argparse.ArgumentParser()
CmdLineArgParser.add_argument(
	"-v",
	"--verbose",
	help = "display debug messages in console",
	action = "store_true",
)
CmdLineArgs = CmdLineArgParser.parse_args()

## -------- LOGGING INITIALISATION ---------------------------
import misc
misc.MyLoggersObj.SetConsoleVerbosity(ConsoleVerbosity = {True : "DEBUG", False : "INFO"}[CmdLineArgs.verbose])
LOG, handle_retval_and_log = misc.CreateLogger(__name__)

try:
	
	## -------------------------------------------------------
	## THE MAIN PROGRAM STARTS HERE
	## -------------------------------------------------------	

	import pandas as pd
	import random
	import copy

	class CsvObjectGenerator(object):
		
		def __init__(self, object_class):
		
			self.object_class = object_class
				
		def generate_from_csv(self, csv_path):
			
			csv_df = pd.read_csv(csv_path, dtype = str)
			
			return [self.object_class(**csv_df.loc[i].to_dict()) for i in range(len(csv_df.index))]
  
	class Carte(object):
	
		suit_d = {
			"Pique"  : "♠",
			"Coeur"  : "♥",
			"Carreau": "♦",
			"Trefle" : "♣",
		}
		
		value_l = [
			"7",
			"8",
			"9",
			"10",
			"V",
			"D",
			"R",
			"A",
		]
	
		def __init__(self, suit, value):
		
			if suit not in self.suit_d.keys():
				return Exception("Invalid suit {}".format(suit))

			if value not in self.value_l:
				return Exception("Invalid value {}".format(value))

			self.suit = suit
			self.value = value
			
		def __repr__(self):
		
			return "{__class__.__name__}(suit={suit!r}, value={value!r})".format(
				__class__ = self.__class__,
				**self.__dict__,
			)
			
		def __str__(self):
			
			return "{:>2}".format(self.value)+self.suit_d[self.suit]
			
		def get_rank(self, atout):
		
			if self.suit == atout:
				
				return {
					"7"  : 0,
					"8"  : 1,
					"D"  : 2,
					"R"  : 3,
					"10" : 4,
					"A"  : 5,
					"9"  : 6,
					"V"  : 7,
				}[self.value]
				
			else:

				return {
					"7"  : 0,
					"8"  : 1,
					"9"  : 2,
					"10" : 3,
					"V"  : 4,
					"D"  : 5,
					"R"  : 6,
					"A"  : 7,
				}[self.value]			

		def get_points(self, atout):
		
			if self.suit == atout:
				
				return {
					"7"  : 0,
					"8"  : 0,
					"D"  : 3,
					"R"  : 4,
					"10" : 10,
					"A"  : 11,
					"9"  : 14,
					"V"  : 20,
				}[self.value]
				
			else:

				return {
					"7"  : 0,
					"8"  : 0,
					"9"  : 0,
					"10" : 10,
					"V"  : 2,
					"D"  : 3,
					"R"  : 4,
					"A"  : 11,
				}[self.value]					

	class Deck(list):
	
		def __new__(cls, data = None):
			obj = super(Deck, cls).__new__(cls, data)
			return obj	
	
		def __str__(self):
		
			return " ".join([str(carte) for carte in self])
	
	class Joueur(object):
	
		def __init__(self, name):
		
			self.name = name
			self.hand_l = Deck([])
			
		def __repr__(self):
			
			return "{__class__.__name__}(name={name!r})".format(
				__class__ = self.__class__,
				**self.__dict__,
			)
			
		def __str__(self):
			
			return self.name
	
		def play_a_card(self, table_l, atout, regles):
			
			# determine what cards can be played (according to the rules)
			card_index_l = []
			for c_index, c in enumerate(self.hand_l):
				rest_of_hand = copy.copy(self.hand_l)
				rest_of_hand.pop(c_index)
				b_card_playable = regles.b_is_card_playable(c, rest_of_hand, table_l, atout)
				print(c, b_card_playable)
				if b_card_playable:
					card_index_l.append(c_index)
			
			# current strategy: random
			return self.hand_l.pop(random.choice(card_index_l))

	class Regles(object):
	
		def b_is_card_playable(self, player_card, rest_of_hand, table_l, atout):

			# is the table not empty?
			if table_l != []:
				
				# la couleur demandée. TODO create dedicated function
				couleur_demandee = table_l[0].suit
				
				# atout demandé ? . TODO create dedicated function
				b_atout_demande = False
				if couleur_demandee == atout:
					b_atout_demande = True
				
				# coupé?. TODO create dedicated function
				b_coupe = False
				for c in table_l[1:]:
					if c.suit == atout:
						b_coupe = True
						break
						
				# est-ce que le partenaire du joueur est maître?. TODO create dedicated function
				b_partenaire_maitre = False
				import IPython;IPython.embed(colors='Neutral')
				if (
					(len(table_l) == 2) and (self.get_winning_card_from_table(table_l, atout) == 0)
				   or
					(len(table_l) == 3) and (self.get_winning_card_from_table(table_l, atout) == 1)
				):
					b_partenaire_maitre = True

				# atout tombé le plus fort ?. TODO create dedicated function
				highest_atout_rank = 0
				for c in table_l:
					if (c.suit == atout) and (c.get_rank(atout) >= highest_atout_rank):
						highest_atout_rank = c.get_rank(atout)
						break
				else:
					highest_atout_rank = None

				# carte du joueur est de la couleur demandée 
				if player_card.suit == couleur_demandee:
					
					if b_atout_demande:
					
						# carte plus haute que l'atout tombé le plus fort
						if player_card.get_rank(atout) > highest_atout_rank:
							return True
						# carte moins haute que l'atout tombé le plus fort
						else:
							# peut il monter à l'atout?
							b_peut_monter = False
							for c in rest_of_hand:
								if (c.suit == atout) and (c.get_rank(atout) > highest_atout_rank):
									b_peut_monter = True
									break
							# s'il peut monter alors il ne peut pas jouer un atout moins fort
							if b_peut_monter:
								return False
							# s'il ne peut pas monter alors il peut pisser avec cette carte
							else:
								return True
								
					# on peut toujours jouer la couleur demandée si ce n'est pas l'atout qui est demandé
					else:
						return True
				# carte du joueur n'est pas de la couleur demandée 	
				else:
					# s'il a la couleur demandée en main, il ne peut pas jouer d'une autre couleur
					if self.b_can_play_suit(rest_of_hand, couleur_demandee):
						return False
					else:
						# si le partenaire du joueur est maître, il peut soit se défausser, soit jouer de l'atout
						if b_partenaire_maitre:
							return True
						else:
							# s'il n'a pas la couleur demandée et que son partenaire n'est pas maître, il doit jouer atout
							if player_card.suit == atout:
								
								if b_coupe:

									# carte plus haute que l'atout tombé le plus fort
									if player_card.get_rank(atout) > highest_atout_rank:
										return True
									# carte moins haute que l'atout tombé le plus fort
									else:
										# peut il monter à l'atout?
										b_peut_monter = False
										for c in rest_of_hand:
											if (c.suit == atout) and (c.get_rank(atout) > highest_atout_rank):
												b_peut_monter = True
												break
										# s'il peut monter alors il ne peut pas jouer un atout moins fort
										if b_peut_monter:
											return False
										# s'il ne peut pas monter alors il peut pisser avec cette carte
										else:
											return True
								
								else:
									return True
									
							else:		
								# s'il a de l'atout, il ne peut pas jouer d'une autre couleur
								if self.b_can_play_suit(rest_of_hand, atout):
									return False
								# s'il n'a pas la couleur demandée en main ni d'atout alors il peut se defausser de n'importe quelle carte
								else:
									return True

			# empty table => any card is good
			else:
				return True	
		
		def get_winning_card_from_table(self, table_l, atout):
		
			"""
			TODO determine the winning card properly 
			"""
	
			winning_c_index = 0
			for c_index, c in enumerate(table_l):
				if c.get_points(atout) > table_l[winning_c_index].get_points(atout):
					winning_c_index = c_index
					
			return c_index

		def b_can_play_suit(self, rest_of_hand, suit):
			""" le joueur a-t-il de la couleur suit en main? """
			b_can_play_suit = False
			for c in rest_of_hand:
				if c.suit == suit:
					b_can_play_suit = True
					break
			return b_can_play_suit
		
		
	class Belote(object):
		
				
		def __init__(self):
		
			self.deck_l	   = Deck(CsvObjectGenerator(Carte ).generate_from_csv(csv_path = r'C:\Users\rex87\belote\belote\cartes.csv' ))
			self.joueurs_l = CsvObjectGenerator(Joueur).generate_from_csv(csv_path = r'C:\Users\rex87\belote\belote\joueurs.csv')
			
		def play(self):
			
			# shuffle the deck
			random.shuffle(self.deck_l)
			
			# quick distribution of cards
			for i in range(8):
				for j in self.joueurs_l:
					j.hand_l.append(self.deck_l.pop())
			
			atout = "Coeur"

			# game
			table_l   = Deck([])
			team1_l   = Deck([])
			team2_l   = Deck([])
			for i in range(8):

				for j in self.joueurs_l:
					print("{:<5}: {}".format(str(j), j.hand_l))
				
				for j in self.joueurs_l:
				
					# player plays a card
					played_card = j.play_a_card(table_l, atout, Regles())
					print("{:<5}: {}".format(str(j), played_card))
					table_l.append(played_card)
					
				# end of round: empty table and in winning team's pile
				for i in range(4):
					team1_l.append(table_l.pop())
					
				print()
			
			print(self.deck_l)
			print([j.hand_l for j in self.joueurs_l])
			print(table_l)
			print(team1_l)
			print(team2_l)
	
	Belote().play()
	
	# while True:
		# Belote().play()

## -------- SOMETHING WENT WRONG -----------------------------	
except:

	import traceback
	LOG.error("Something went wrong! Exception details:\n{}".format(traceback.format_exc()))

## -------- GIVE THE USER A CHANCE TO READ MESSAGES-----------
finally:
	
	input("Press any key to exit ...")
