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
	import time
	import pygame
	import numpy as np
	import queue
	import threading
	import os

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
		
		rank_l = [
			"7",
			"8",
			"9",
			"10",
			"V",
			"D",
			"R",
			"A",
		]
	
		def __init__(self, suit, rank):
		
			if suit not in self.suit_d.keys():
				return Exception("Invalid suit {}".format(suit))

			if rank not in self.rank_l:
				return Exception("Invalid rank {}".format(rank))

			self.suit = suit
			self.rank = rank
			
		def __repr__(self):
		
			return "{__class__.__name__}(suit={suit!r}, rank={rank!r})".format(
				__class__ = self.__class__,
				**self.__dict__,
			)
			
		def __str__(self):
			
			return "{:>2}".format(self.rank)+self.suit_d[self.suit]
			
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
				}[self.rank]
				
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
				}[self.rank]			

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
				}[self.rank]
				
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
				}[self.rank]					

	class Deck(list):
		
		def __new__(cls, data = None):
			obj = super(Deck, cls).__new__(cls, data)
			obj.b_dix_de_der = False
			return obj

		def get_points(self, atout):
		
			dix_de_der = 0
			if self.b_dix_de_der:
				dix_de_der = 10
			
			return sum([c.get_points(atout) for c in self]) + dix_de_der
	
		def __str__(self):
		
			return " ".join([str(carte) for carte in self])
	
	class Joueur(object):
	
		def __init__(self, name):
		
			self.name = name
			self.hand_l = Deck([])
			self.b_human = False
			self.b_thinking = False
			self.human_choice = None
			
		def __repr__(self):
			
			return "{__class__.__name__}(name={name!r})".format(
				__class__ = self.__class__,
				**self.__dict__,
			)
			
		def __str__(self):
			
			return self.name
	
		def play_a_card(self, table_l, atout, regles, b_play_thread_abort_queue):
			
			# determine what cards can be played (according to the rules)
			allowed_card_index_l = []
			for c_index, c in enumerate(self.hand_l):
				rest_of_hand = copy.copy(self.hand_l)
				rest_of_hand.pop(c_index)
				b_card_playable, card_playable_explanation = regles.b_is_card_playable(c, rest_of_hand, table_l, atout)
				LOG.debug("{} {} {}".format(c, b_card_playable, "({})".format(card_playable_explanation)))
				if b_card_playable:
					allowed_card_index_l.append(c_index)
			
			# loop to filter out wrong clicks on GUI
			while True:
			
				if not self.b_human:
					# current strategy: random
					card_choice = random.choice(allowed_card_index_l)
				else:
					self.b_thinking = True
					LOG.debug("Waiting for human player {}".format(self.name))
					while True:

						try:
							b_play_thread_abort = b_play_thread_abort_queue.get(block = False)
							if b_play_thread_abort:
								raise Exception("Aborted while choosing a card")
						except queue.Empty:
							pass
					
						if self.human_choice is not None:
							break
							
						time.sleep(1/20)
						
					card_choice = self.human_choice
					self.human_choice = None				
					self.b_thinking = False
				
				try:
					played_card = self.hand_l.pop(card_choice)
				except IndexError:
					LOG.debug("IndexError while popping card from player hand. Likely problem with card clicked.")
					continue
				
				break
			
			LOG.debug("{:<5}: {}".format(str(self), played_card))
			
			return played_card

	class Regles(object):
	
		def get_couleur_demandee(self, table_l):
		
			return table_l[0].suit
	
		def b_coupe(self, table_l, atout):
		
			b_coupe = False
			for c in table_l[1:]:
				if c.suit == atout:
					b_coupe = True
					break
			return b_coupe
		
		def get_highest_atout_rank(self, table_l, atout):
			
			highest_atout_rank = 0
			for c in table_l:
				if (c.suit == atout) and (c.get_rank(atout) >= highest_atout_rank):
					highest_atout_rank = c.get_rank(atout)
					break
			else:
				highest_atout_rank = None
			return highest_atout_rank
		
		def b_is_card_playable(self, player_card, rest_of_hand, table_l, atout):

			# is the table not empty?
			if table_l != []:
				
				# la couleur demandée
				couleur_demandee = self.get_couleur_demandee(table_l)
				
				# atout demandé ? . TODO create dedicated function
				b_atout_demande = False
				if couleur_demandee == atout:
					b_atout_demande = True
				
				# coupé?
				b_coupe = self.b_coupe(table_l, atout)
						
				# est-ce que le partenaire du joueur est maître?. TODO create dedicated function
				b_partenaire_maitre = False
				if (
					(len(table_l) == 2) and (self.get_winning_card_from_table(table_l, atout) == 0)
				   or
					(len(table_l) == 3) and (self.get_winning_card_from_table(table_l, atout) == 1)
				):
					b_partenaire_maitre = True

				# atout tombé le plus fort ?
				highest_atout_rank = self.get_highest_atout_rank(table_l, atout)

				# carte du joueur est de la couleur demandée 
				if player_card.suit == couleur_demandee:
					
					if b_atout_demande:
					
						# carte plus haute que l'atout tombé le plus fort
						if player_card.get_rank(atout) > highest_atout_rank:
							return (True, "Atout demandé, peut jouer plus haut avec cet atout")
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
								return (False, "Atout demandé, peut monter avec un autre atout")
							# s'il ne peut pas monter alors il peut pisser avec cette carte
							else:
								return (True, "Atout demandé, peut pisser avec cet atout")
								
					# on peut toujours jouer la couleur demandée si ce n'est pas l'atout qui est demandé
					else:
						return (True, "Peut jouer la couleur demandée")
				# carte du joueur n'est pas de la couleur demandée 	
				else:
					# s'il a la couleur demandée en main, il ne peut pas jouer d'une autre couleur
					if self.b_can_play_suit(rest_of_hand, couleur_demandee):
						return (False, "Peut jouer la couleur demandée, donc pas cette carte")
					else:
						# si le partenaire du joueur est maître, il peut soit se défausser, soit jouer de l'atout
						if b_partenaire_maitre:
							return (True, "Peut pas jouer la couleur demandée, partenaire est maitre")
						else:
							# s'il n'a pas la couleur demandée et que son partenaire n'est pas maître, il doit jouer atout
							if player_card.suit == atout:
								
								if b_coupe:

									# carte plus haute que l'atout tombé le plus fort
									if player_card.get_rank(atout) > highest_atout_rank:
										return (True, "Peut pas jouer la couleur demandée, jeu est coupé, peut jouer plus haut avec cet atout")
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
											return (False, "Peut pas jouer la couleur demandée, peut monter avec un autre atout")
										# s'il ne peut pas monter alors il peut pisser avec cette carte
										else:
											return (True, "Peut pas jouer la couleur demandée, peut pisser avec cet atout")
								
								else:
									return (True, "Peut pas jouer la couleur demandée, peut couper avec cet atout")
									
							else:		
								# s'il a de l'atout, il ne peut pas jouer d'une autre couleur
								if self.b_can_play_suit(rest_of_hand, atout):
									return (False, "Peut pas jouer la couleur demandée, peut jouer un atout")
								# s'il n'a pas la couleur demandée en main ni d'atout alors il peut se defausser de n'importe quelle carte
								else:
									return (True, "Peut pas jouer la couleur demandée, pas d'atout")

			# empty table => any card is good
			else:
				return (True, "Table is empty")
		
		def get_winning_card_from_table(self, table_l, atout):
		
			"""
			TODO determine the winning card on the table 
			"""
	
			couleur_demandee = self.get_couleur_demandee(table_l)
			b_coupe = self.b_coupe(table_l, atout)
	
			if b_coupe or (couleur_demandee == atout):
				winning_suit = atout
			else:
				winning_suit = couleur_demandee
	
			winning_c_index = 0
			for c_index, c in enumerate(table_l):
				if (c.suit == winning_suit) and (c.get_points(atout) >= table_l[winning_c_index].get_points(atout)):
					winning_c_index = c_index
			
			return winning_c_index

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
		
			self.deck_l	   = None
			self.joueurs_l = None
			self.table_l   = None
			self.winning_player = None
			
			self.play_thread = None
			self.b_play_thread_abort_queue = queue.Queue()
			
			self.t = 0
		
		def initialise(self):
			
			self.deck_l	   = Deck(CsvObjectGenerator(Carte).generate_from_csv(csv_path = r'C:\Users\rex87\belote2\belote\cartes.csv' ))
			self.joueurs_l = CsvObjectGenerator(Joueur).generate_from_csv(csv_path = r'C:\Users\rex87\belote2\belote\joueurs.csv')
			
			# self.test_thread = threading.Thread(target = self.run_test_thread)		
			self.play_thread = threading.Thread(name = "play_thread", target = self.run_play_thread)		
		
		def run_play_thread(self):
			
			# shuffle the deck
			random.shuffle(self.deck_l)
			
			# quick distribution of cards
			for i in range(8):
				for j in self.joueurs_l:
					j.hand_l.append(self.deck_l.pop())
			
			atout = "Coeur"

			# game
			self.table_l = Deck([])
			team1_l   = Deck([])
			team2_l   = Deck([])
			points_sum = 0
			self.winning_player = 0
			for round_i in range(8):

				for j in self.joueurs_l:
					LOG.debug("{:<5}: {}".format(str(j), j.hand_l))
				
				# table_l is indexed with table_i
				for table_i in range(4):
					
					j_index = (table_i+self.winning_player)%4
					j = self.joueurs_l[j_index]
					
					# player plays a card
					played_card = j.play_a_card(self.table_l, atout, Regles(), self.b_play_thread_abort_queue)
					self.table_l.append(played_card)
					
					time.sleep(0.5)
				
				winning_c_index = Regles().get_winning_card_from_table(self.table_l, atout)
				next_winning_player = (self.winning_player+winning_c_index)%4
				
				LOG.debug(
					"Fin du tour: {}| Valeur de la main: {}| Joueur qui prend la main: {} ({})".format(
						self.table_l,
						self.table_l.get_points(atout),
						str(self.joueurs_l[next_winning_player]),
						next_winning_player,
					)
				)
				input("PAUSE")
				
				self.winning_player = next_winning_player
				
				# end of round: empty table and in winning team's pile
				if self.winning_player%2 == 0:
					winning_team_l = team1_l
				else:
					winning_team_l = team2_l
				
				for table_i in range(4):
					winning_team_l.append(self.table_l.pop())
					
				if round_i == 7:
					winning_team_l.b_dix_de_der = True
					
				LOG.debug("")
			
			assert((team1_l.get_points(atout) + team2_l.get_points(atout)) == 162)
			
			team1_points = team1_l.get_points(atout)
			team2_points = team2_l.get_points(atout)
			
			LOG.debug("Equipe 0-2: {}".format(team1_points))
			LOG.debug("Equipe 1-3: {}".format(team2_points))
			
			return (team1_points, team2_points)
	
		def run_test_thread(self):
			
			ClockFrequency = 60
			TimeElapsed = 0
			startTime = 0
			while True:
				
				try:
					b_test_thread_abort = self.b_test_thread_abort_queue.get(block = False)
					if b_test_thread_abort:
						break
				except queue.Empty:
					pass		 
				
				TimeElapsed = time.perf_counter() - startTime
				if TimeElapsed > ( 1/ClockFrequency ):
					startTime = time.perf_counter()
					self.t += 1
					self.x1 = (1/2)*(np.sin(self.t/ClockFrequency) + 1)
					self.x2 = (1/2)*(np.cos(0.7*self.t/ClockFrequency) + 1)
				else:
					time.sleep(1/ClockFrequency - TimeElapsed) 		
	
		def start_all_threads(self):
			# self.test_thread.start()
			self.play_thread.start()
			return
		
		def abortAllThreads(self):
			# self.b_test_thread_abort_queue.put(True)
			self.b_play_thread_abort_queue.put(True)
			return
		
		def joinAllThreads(self):
			# self.test_thread.join()
			self.play_thread.join()
			return
		
		def stopAllThreads(self):
			self.abortAllThreads()
			self.joinAllThreads()
	
	def get_hand_x(i):
		return int(i*(screen_width-168)/7)
	
	this_folder = os.path.dirname(os.path.realpath(__file__))
	
	screen_width = 800
	screen_height = 600

	BLACK_COLOUR = (0, 0, 0)
	GREEN_COLOUR = (0, 127, 0)
	WHITE_COLOUR = (255, 255, 255)

	pygame.init()
	pygame.font.init()
	
	myfont = pygame.font.SysFont('Consolas', 30)
	
	screen = pygame.display.set_mode((screen_width, screen_height))

	background = pygame.Surface(screen.get_size())
	background = background.convert()

	FPS = 30

	hj = 2 # human joueur id
	b_obj = Belote()
	b_obj.initialise()
	b_obj.start_all_threads()
	b_obj.joueurs_l[hj].b_human = True

	# table cards coordinates
	tx = 320
	ty = 120
	to1, to2 = 70, 25
	table_coord_l = [
		(tx - to2, ty + to1), # human player
		(tx - to1, ty - to2),
		(tx + to2, ty - to1),
		(tx + to1, ty + to2),
	]

	# load card images
	card_images_d = {}
	name_map = {
		'pique'   : 'Pique',
		'coeur'   : 'Coeur',
		'carreau' : 'Carreau',
		'trefle'  : 'Trefle',
		'7'       : '7',
		'8'       : '8',
		'9'       : '9',
		'10'      : '10',
		'valet'   : 'V',
		'dame'    : 'D',
		'roi'     : 'R',
		'as'      : 'A',
	}
	for suit in ['pique', 'coeur', 'carreau', 'trefle']:
		card_images_d[name_map[suit]] = {}
		for rank in ['7', '8', '9', '10', 'valet', 'dame', 'roi', 'as']:
			card_images_d[name_map[suit]][name_map[rank]] = pygame.image.load(os.path.join(this_folder, r'..\images\cards\{}_{}.png'.format(suit, rank)))

	b_playing = True
	last_time = 0
	hand_y_idle = screen_height - 120
	hand_y_sel_offset = -50
	while b_playing:
	
		# pygame events
		b_left_click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				b_playing = False # pygame window closed by user
				b_obj.stopAllThreads()
			elif event.type == pygame.MOUSEMOTION:
				mouse_pos = pygame.mouse.get_pos()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				b_left_click = True
				# LOG.info(mouse_pos)
		
		# the nice green background
		background.fill(GREEN_COLOUR)
		
		# update card selection
		b_hand_card_selected_l = [False]*8
		if mouse_pos[1] > hand_y_idle + hand_y_sel_offset: 
			
			for hand_i in range(8):
				
				if mouse_pos[0] >= get_hand_x(7+1):
					b_hand_card_selected_l[7] = True
					
				if mouse_pos[0] < get_hand_x(hand_i+1):
					b_hand_card_selected_l[hand_i] = True
					break
			
			if b_left_click:
				b_obj.joueurs_l[hj].human_choice = hand_i
		
		# update table
		for table_i, table_card in enumerate(b_obj.table_l):
			
			table_coord_i = (table_i - hj + b_obj.winning_player)%4
			
			table_x = table_coord_l[table_coord_i][0]
			table_y = table_coord_l[table_coord_i][1]
			background.blit(card_images_d[table_card.suit][table_card.rank], (table_x, table_y))
			
		# update card sprites
		for hand_i, hand_card in enumerate(b_obj.joueurs_l[hj].hand_l):
			
			hand_x = get_hand_x(hand_i)
			hand_y = hand_y_idle + hand_y_sel_offset*b_hand_card_selected_l[hand_i]
			
			background.blit(card_images_d[hand_card.suit][hand_card.rank], (hand_x, hand_y))
		
		# display players' names
		joueur_name  = myfont.render(b_obj.joueurs_l[(hj+0)%4].name, True, (0, 0, 0))
		joueur_left  = myfont.render(b_obj.joueurs_l[(hj+1)%4].name, True, (0, 0, 0))
		joueur_front = myfont.render(b_obj.joueurs_l[(hj+2)%4].name, True, (0, 0, 0))
		joueur_right = myfont.render(b_obj.joueurs_l[(hj+3)%4].name, True, (0, 0, 0))
		background.blit(joueur_name , (int(screen_width/2), screen_height-50      ))
		background.blit(joueur_left , (0                  , int(4*screen_height/9)))
		background.blit(joueur_front, (int(screen_width/2), 0                     ))
		background.blit(joueur_right, (screen_width - 100 , int(5*screen_height/9)))
		
		# refresh rate
		now = time.time()
		if (now - last_time) > (1/FPS):
			screen.blit(background, (0, 0))
			pygame.display.flip()
			last_time = time.time()
		else:
			milliseconds_left = int(1000*((1/FPS) - (now - last_time)))
			pygame.time.wait(milliseconds_left)
	 
## -------- SOMETHING WENT WRONG -----------------------------	
except:

	import traceback
	LOG.error("Something went wrong! Exception details:\n{}".format(traceback.format_exc()))

## -------- GIVE THE USER A CHANCE TO READ MESSAGES-----------
finally:
	
	pygame.quit()
	# input("Press any key to exit ...")
