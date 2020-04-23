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

	LOG.debug("import pandas ...");    import pandas as pd
	LOG.debug("import random ...");    import random
	LOG.debug("import copy ...");      import copy
	LOG.debug("import time ...");      import time
	LOG.debug("import pygame ...");    import pygame
	LOG.debug("import numpy ...");     import numpy as np
	LOG.debug("import queue ...");     import queue
	LOG.debug("import threading ..."); import threading
	LOG.debug("import os ...");        import os

	class Button():

		def __init__(self, text, x=0, y=0, wid=100, hei=50, command=None):

			self.text = text
			self.command = command
			
			self.image_normal = pygame.Surface((wid, hei))
			self.image_normal.fill(GREEN_COLOUR)

			self.image_hovered = pygame.Surface((wid, hei))
			self.image_hovered.fill(RED_COLOUR)

			self.image = self.image_normal
			self.rect = self.image.get_rect()

			font = pygame.font.Font('freesansbold.ttf', 15)
			
			text_image = font.render(text, True, WHITE_COLOUR)
			text_rect = text_image.get_rect(center = self.rect.center)
			
			self.image_normal.blit(text_image, text_rect)
			self.image_hovered.blit(text_image, text_rect)

			# you can't use it before `blit` 
			self.rect.topleft = (x, y)

			self.hovered = False

		def update(self):

			if self.hovered:
				self.image = self.image_hovered
			else:
				self.image = self.image_normal
			
		def draw(self, surface):

			surface.blit(self.image, self.rect)

		def handle_event(self, event):

			if event.type == pygame.MOUSEMOTION:
				self.hovered = self.rect.collidepoint(event.pos)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if self.hovered:
					LOG.debug('Clicked: {}'.format(self.text))
					return True
					
			return False

	class ImageButton():

		def __init__(self, image_surface, x=0, y=0):
			
			self.image_surface = image_surface
			
			self.rect = image_surface.get_rect()
			
			self.image_normal = pygame.Surface(image_surface.get_size())
			self.image_normal.fill(WHITE_COLOUR)

			self.image_hovered = pygame.Surface(image_surface.get_size())
			self.image_hovered.fill(GREEN_COLOUR)
			
			self.image_normal.blit(image_surface, self.rect)
			self.image_hovered.blit(image_surface, self.rect)
			
			self.image = self.image_normal

			# you can't use it before `blit` 
			self.rect.topleft = (x, y)

			self.hovered = False

		def update(self):

			if self.hovered:
				self.image = self.image_hovered
			else:
				self.image = self.image_normal
			
		def draw(self, surface):

			surface.blit(self.image, self.rect)

		def handle_event(self, event):

			if event.type == pygame.MOUSEMOTION:
				self.hovered = self.rect.collidepoint(event.pos)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if self.hovered:
					LOG.debug('Clicked: {}, ID = {}'.format(self.image_surface, id(self.image_surface)))
					return True
					
			return False

	class YesNoBox():
	
		def __init__(self, question_text, x=0, y=0, wid=100, hei=50, command=None):
			
			self.question_text = question_text
			self.command = command
			
			font = pygame.font.Font('freesansbold.ttf', 20)			

			self.bg = pygame.Surface((wid, hei))
			self.bg_rect = self.bg.get_rect()
			
			qtext_image = font.render(question_text, True, WHITE_COLOUR)
			qtext_rect = qtext_image.get_rect(center = (self.bg_rect.center[0], int(self.bg_rect.center[1]/2)))
			
			self.bg.blit(qtext_image, qtext_rect)

			self.oui_button = Button('OUI', 90 , 40, 100, 50)
			self.non_button = Button('NON', 210, 40, 100, 50)		
			
			self.bg_rect.topleft = (x, y)
			
			self.answer = None
			
		def update(self):
			
			self.oui_button.update()
			self.non_button.update()
			
		def draw(self, surface):
	
			self.oui_button.draw(self.bg)
			self.non_button.draw(self.bg)
	
			surface.blit(self.bg, self.bg_rect)			

		def handle_event(self, event):

			event_ = event		
			if event.type == pygame.MOUSEMOTION:
				event_.pos = (event.pos[0] - self.bg_rect.topleft[0], event.pos[1] - self.bg_rect.topleft[1])
				
			if self.oui_button.handle_event(event_):
				self.answer = True
			if self.non_button.handle_event(event_):
				self.answer = False

	class DeuxBox():
	
		def __init__(self, suit_images_d, x = 0, y = 0, wid = 100, hei = 50):
			
			font = pygame.font.Font('freesansbold.ttf', 20)			

			self.bg = pygame.Surface((wid, hei))
			self.bg_rect = self.bg.get_rect()
			
			qtext_image = font.render("Voulez-vous prendre à deux?", True, WHITE_COLOUR)
			qtext_rect = qtext_image.get_rect(center = (self.bg_rect.center[0], int(self.bg_rect.center[1]/2)))
			
			self.bg.blit(qtext_image, qtext_rect)

			x_offset = 35
			self.pique_button   = ImageButton(suit_images_d['pique']  , x_offset+0  , 45)
			self.coeur_button   = ImageButton(suit_images_d['coeur']  , x_offset+70 , 45)		
			self.carreau_button = ImageButton(suit_images_d['carreau'], x_offset+140, 45)		
			self.trefle_button  = ImageButton(suit_images_d['trefle'] , x_offset+210, 45)		
			self.non_button     = Button('NON'                        , x_offset+280, 45, 42, 42)		
			
			self.bg_rect.topleft = (x, y)
			
			self.answer = None
			
		def update(self):
			
			self.pique_button.update()
			self.coeur_button.update()
			self.carreau_button.update()
			self.trefle_button.update()
			self.non_button.update()
			
		def draw(self, surface):
	
			self.pique_button.draw(self.bg)
			self.coeur_button.draw(self.bg)
			self.carreau_button.draw(self.bg)
			self.trefle_button.draw(self.bg)
			self.non_button.draw(self.bg)
	
			surface.blit(self.bg, self.bg_rect)			

		def handle_event(self, event):

			event_ = event		
			if event.type == pygame.MOUSEMOTION:
				event_.pos = (event.pos[0] - self.bg_rect.topleft[0], event.pos[1] - self.bg_rect.topleft[1])
				
			if self.pique_button.handle_event(event_)  : self.answer = 'Pique'
			if self.coeur_button.handle_event(event_)  : self.answer = 'Coeur' 
			if self.carreau_button.handle_event(event_): self.answer = 'Carreau'
			if self.trefle_button.handle_event(event_) : self.answer = 'Trefle' 
			if self.non_button.handle_event(event_)    : self.answer = False 

	class MessageBox():
	
		def __init__(self, message_text, x=0, y=0, wid=100, hei=50):
			
			self.message_text = message_text
			
			font = pygame.font.Font('freesansbold.ttf', 20)			

			self.bg = pygame.Surface((wid, hei))
			self.bg.fill(WHITE_COLOUR)
			self.bg_rect = self.bg.get_rect()
			
			qtext_image = font.render(message_text, True, BLUE_COLOUR)
			qtext_rect = qtext_image.get_rect(center = self.bg_rect.center)
			qtext_rect[0] = 1
			
			self.bg.blit(qtext_image, qtext_rect)
			self.bg.set_colorkey(WHITE_COLOUR)
			self.bg.convert_alpha()
			
			self.bg_rect.topleft = (x, y)
			
		def update(self):
			
			return
			
		def draw(self, surface):
	
			surface.blit(self.bg, self.bg_rect)			

		def handle_event(self, event):

			return

	def StatusBox(message = ""):
		return MessageBox(message, 0, scr_hei - stabar_hei, 550, stabar_hei)

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
					"V"  : 3,
					"D"  : 4,
					"R"  : 5,
					"10" : 6,
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
					"V"  : 2,
					"D"  : 3,
					"R"  : 4,
					"10" : 10,
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
			
		def b_has_card(self, rank = None, suit = None):
			
			assert((rank is not None) or (suit is not None))
			
			for c in self:
				
				if rank is None:
					card_condition = (c.suit == suit)
				elif suit is None:
					card_condition = (c.rank == rank)
				else:
					card_condition = (c.rank == rank and c.suit == suit)
			
				if card_condition:
					return True, c
			
			return False, None
		
		def __str__(self):
		
			return " ".join([str(carte) for carte in self])
	
	class Joueur(object):
	
		def __init__(self, name, index):
		
			self.name = name
			self.index = int(index)
			self.hand_l = Deck([])
			self.b_human = False
			self.b_thinking = False
			self.human_choice = None
			self.allowed_card_index_l = None
			
		def __repr__(self):
			
			return "{__class__.__name__}(name={name!r})".format(
				__class__ = self.__class__,
				**self.__dict__,
			)
			
		def __str__(self):
			
			return self.name
	
		def play_a_card(self, table_l, atout, regles, b_play_thread_abort_queue):
			
			# determine what cards can be played (according to the rules)
			self.allowed_card_index_l = []
			for c_index, c in enumerate(self.hand_l):
				rest_of_hand = copy.copy(self.hand_l)
				rest_of_hand.pop(c_index)
				b_card_playable, card_playable_explanation = regles.b_is_card_playable(c, rest_of_hand, table_l, atout)
				LOG.debug("{} {} {}".format(c, b_card_playable, "({})".format(card_playable_explanation)))
				if b_card_playable:
					self.allowed_card_index_l.append(c_index)
			
			# loop to filter out wrong clicks on GUI
			while True:
			
				if not self.b_human:
					# current strategy: random
					card_choice = random.choice(self.allowed_card_index_l)
				else:
					self.b_thinking = True
					self.human_choice = None
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
				
				# if it excepts here, continue until selection is valid
				try:
					played_card = self.hand_l.pop(card_choice)
				except IndexError:
					LOG.debug("IndexError while popping card from player hand. Likely problem with card clicked.")
					continue
				
				self.allowed_card_index_l = []
				
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
				win_c_i = self.get_winning_card_from_table(table_l, atout)
				if (
					( (len(table_l) == 2) and (win_c_i == 0) and (table_l[win_c_i].suit != atout) )
				   or
					( (len(table_l) == 3) and (win_c_i == 1) and (table_l[win_c_i].suit != atout) )
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
	
			winning_c_index = None
			for c_index, c in enumerate(table_l):
				
				if (c.suit == winning_suit) and winning_c_index is None:
					winning_c_index = c_index
					continue
				
				if (c.suit == winning_suit) and (c.get_rank(atout) >= table_l[winning_c_index].get_rank(atout)):
					winning_c_index = c_index
			
			# ensure winning card has the winning suit
			assert(table_l[winning_c_index].suit == winning_suit)
			
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
				
		def __init__(self, hj_i = None):
		
			self.deck_l	   = None
			self.joueurs_l = None
			self.table_l   = None
			self.winning_player = None
			self.b_left_click = False
			self.atout = None
			self.hj_i = hj_i
			self.preneur = None
			self.dealer = random.randint(0, 3)
			
			# dialog boxes
			self.yesno_box = None
			self.message_box = None
			self.deux_box = None
			
			self.play_thread = None
			self.b_play_thread_abort_queue = queue.Queue()
			
			self.t = 0
		
		def my_time_sleep(self, duration):
			
			if duration <= 0.05:
				time.sleep(0.05)
			else:
				start_time = time.time()
				while True:
					try:
						b_play_thread_abort = self.b_play_thread_abort_queue.get(block = False)
						if b_play_thread_abort:
							raise Exception("Aborted while choosing a card")
					except queue.Empty:
						pass
					
					if time.time() - start_time > duration:
						break
					else:
						time.sleep(0.05)
		
		def run_play_thread(self):

			# initialise deck and joueurs
			self.deck_l	   = Deck(CsvObjectGenerator(Carte).generate_from_csv(csv_path = r'C:\Users\rex87\belote2\belote\cartes.csv' ))
			self.joueurs_l = CsvObjectGenerator(Joueur).generate_from_csv(csv_path = r'C:\Users\rex87\belote2\belote\joueurs.csv')
			
			if self.hj_i is not None:
				self.joueurs_l[self.hj_i].b_human = True

			self.atout = None
			self.table_l = Deck([])
			team1_l   = Deck([])
			team2_l   = Deck([])

			# shuffle the deck
			LOG.debug("Shuffle the deck ...")
			random.shuffle(self.deck_l)
			
			# distribution of cards
			# for i in range(8):
				# for j in self.joueurs_l:
					# j.hand_l.append(self.deck_l.pop())
			
			self.winning_player = self.dealer # only there to define a slot on the table

			LOG.debug("Première distribution...")
			
			self.message_box = StatusBox("{} distribue les cartes ...".format(self.joueurs_l[self.dealer].name))
			
			for j_index_, j_ in enumerate(self.joueurs_l):
				j_index = (j_index_ + self.dealer + 1)%4
				j = self.joueurs_l[j_index]
				for i in range(3):
					j.hand_l.append(self.deck_l.pop())
				self.my_time_sleep(1)
			for j_index_, j_ in enumerate(self.joueurs_l):
				j_index = (j_index_ + self.dealer + 1)%4
				j = self.joueurs_l[j_index]
				for i in range(2):
					j.hand_l.append(self.deck_l.pop())
				self.my_time_sleep(1)
			self.table_l.append(self.deck_l.pop())
			
			for j_index, j in enumerate(self.joueurs_l):
				LOG.debug("{}: {}".format(j.name, j.hand_l))
			
			LOG.debug("Tour de une...")
			for j_index_, j_ in enumerate(self.joueurs_l):
				j_index = (j_index_ + self.dealer + 1)%4
				j = self.joueurs_l[j_index]
				self.message_box = StatusBox("{} réfléchit ...".format(j.name))
				if self.b_decide_de_prendre_a_une(j, self.table_l):
					j.hand_l.append(self.table_l.pop())
					break
			
			if self.atout is not None:
				pass
			else:
				LOG.debug("Tour de deux...")
				for j_index_, j_ in enumerate(self.joueurs_l):
					j_index = (j_index_ + self.dealer + 1)%4
					j = self.joueurs_l[j_index]
					self.message_box = StatusBox("{} réfléchit ...".format(j.name))				
					b_j_answer, atout = self.b_decide_de_prendre_a_deux(j, self.table_l)
					if b_j_answer:
						j.hand_l.append(self.table_l.pop())
						break
					
			for j_key in ['human', 'top', 'left', 'right']:
				j_loc_d[j_key]['speech_text'] = None
				
			assert (self.atout is not None)
			
			self.message_box = StatusBox("{} finit de distribuer ...".format(self.joueurs_l[self.dealer].name))
			for j_index_, j_ in enumerate(self.joueurs_l):
				j_index = (j_index_ + self.dealer + 1)%4
				j = self.joueurs_l[j_index]
				if j_index == self.preneur:
					for i in range(2):
						j.hand_l.append(self.deck_l.pop())				
				else:				
					for i in range(3):
						j.hand_l.append(self.deck_l.pop())
				self.my_time_sleep(1)

			self.message_box = None
			
			# game
			points_sum = 0
			self.winning_player = (self.dealer + 1)%4
			for round_i in range(8):

				for j in self.joueurs_l:
					LOG.debug("{:<5}: {}".format(str(j), j.hand_l))
				
				# table_l is indexed with table_i
				for table_i in range(4):
					
					try:
						b_play_thread_abort = self.b_play_thread_abort_queue.get(block = False)
						if b_play_thread_abort:
							raise Exception("Aborted before joueur played a card")
					except queue.Empty:
						pass
					
					j_index = (table_i+self.winning_player)%4
					j = self.joueurs_l[j_index]
					
					# player plays a card
					self.message_box = StatusBox("À {} de jouer.".format(j.name))
					played_card = j.play_a_card(self.table_l, self.atout, Regles(), self.b_play_thread_abort_queue)
					self.table_l.append(played_card)
						
					self.my_time_sleep(0.5)
				
				winning_c_index = Regles().get_winning_card_from_table(self.table_l, self.atout)
				next_winning_player = (self.winning_player+winning_c_index)%4
				
				LOG.debug(
					"Fin du tour: {}| Valeur de la main: {}| Joueur qui prend la main: {} ({})".format(
						self.table_l,
						self.table_l.get_points(self.atout),
						str(self.joueurs_l[next_winning_player]),
						next_winning_player,
					)
				)
				
				self.wait_for_user_click(message = "{} gagne ce tour.".format(self.joueurs_l[next_winning_player]))
				
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
			
			assert((team1_l.get_points(self.atout) + team2_l.get_points(self.atout)) == 162)
			
			team1_points = team1_l.get_points(self.atout)
			team2_points = team2_l.get_points(self.atout)
			
			LOG.debug("Equipe 0-2: {}".format(team1_points))
			LOG.debug("Equipe 1-3: {}".format(team2_points))
			
			self.dealer = (self.dealer + 1)%4
			
			# this thread is going to end. Schedule a delayed start for the next one
			self.play_thread_count += 1
			self.play_thread = threading.Timer(.01, self.run_play_thread)
			self.play_thread.name = "play_thread_{}".format(self.play_thread_count)
			self.play_thread.daemon = True
			self.play_thread.start()
			# return (team1_points, team2_points)
			return

		def b_decide_de_prendre_a_une(self, joueur, table_l):
		
			c = table_l[0]
			
			if not joueur.b_human:
			
				self.my_time_sleep(0.5) # pour le fun			
				
				b_answer = None
				
				if c.rank == 'V':
					b_answer = True
				else:
					b_has_atout_v, atout_v_c = joueur.hand_l.b_has_card(rank = 'V', suit = c.suit)
					if b_has_atout_v:
						b_answer = True
					else:
						b_answer = False
					
			else:
				
				b_answer = self.wait_for_user_answer(message = "Voulez-vous prendre à une?")
			
			if b_answer:
				message_text = "{} prend à {}!".format(joueur.name, c.suit)
				LOG.debug(message_text)
				self.winning_player = joueur.index # only there to define a slot on the table
				self.atout = c.suit
				self.preneur = joueur.index
				j_loc_d[j_loc_d[joueur.index]]['speech_text'] = "JE PRENDS!"
				self.wait_for_user_click(message = message_text)
			else:
				msg = '{} dit "UNE!"'.format(joueur.name)
				LOG.debug(msg)
				self.message_box = StatusBox(msg)
				j_loc_d[j_loc_d[joueur.index]]['speech_text'] = "UNE!"	
					
			return b_answer 			

		def b_decide_de_prendre_a_deux(self, joueur, table_l):
		
			c = table_l[0]
			
			b_answer = None
			atout = None
			if not joueur.b_human:
			
				self.my_time_sleep(0.5) # pour le fun	
			
				b_has_v, v_c = joueur.hand_l.b_has_card(rank = 'V')
				if b_has_v:
					b_answer = True
					atout = v_c.suit
				else:
					b_answer = False
					
			else:
				
				answer_a_deux = self.wait_for_user_answer_a_deux()
				if answer_a_deux == False:
					b_answer = False
				else:
					b_answer = True
					atout = answer_a_deux
			
			if b_answer:
				message_text = "{} prend à {}!".format(joueur.name, atout)
				self.winning_player = joueur.index # only there to define a slot on the table
				self.atout = atout
				self.preneur = joueur.index
				LOG.debug(message_text)
				j_loc_d[j_loc_d[joueur.index]]['speech_text'] = "JE PRENDS!"
				self.wait_for_user_click(message = message_text)
			else:
				msg = '{} dit "DEUX!"'.format(joueur.name)
				LOG.debug(msg)
				self.message_box = StatusBox(msg)
				j_loc_d[j_loc_d[joueur.index]]['speech_text'] = "DEUX!"			
			
			return b_answer, atout

		def wait_for_user_click(self, message = None):
			LOG.debug("Waiting for user to click anywhere")
			self.message_box = StatusBox(message)
			self.b_left_click = False
			while True:
				
				try:
					b_play_thread_abort = self.b_play_thread_abort_queue.get(block = False)
					if b_play_thread_abort:
						raise Exception("Aborted while waiting for user to click anywhere")
				except queue.Empty:
					pass
					
				if self.b_left_click:
					break
					
				time.sleep(0.02)
				
			self.message_box = None
			
		def wait_for_user_answer(self, message = None):
			LOG.debug("Waiting for user to answer question")
			human_answer = None
			self.yesno_box = YesNoBox(message, 200, 350, 400, 100)
			while True:

				try:
					b_play_thread_abort = self.b_play_thread_abort_queue.get(block = False)
					if b_play_thread_abort:
						raise Exception("Aborted while waiting for user to click anywhere")
				except queue.Empty:
					pass

				if self.yesno_box.answer is not None:
					answer = self.yesno_box.answer
					self.yesno_box = None
					return answer
				
				time.sleep(0.02)

		def wait_for_user_answer_a_deux(self):
			LOG.debug("Waiting for user to answer question à deux")
			human_answer = None
			self.deux_box = DeuxBox(suit_images_d, 200, 350, 400, 100)
			while True:

				try:
					b_play_thread_abort = self.b_play_thread_abort_queue.get(block = False)
					if b_play_thread_abort:
						raise Exception("Aborted while waiting for user to click anywhere")
				except queue.Empty:
					pass

				if self.deux_box.answer is not None:
					answer = self.deux_box.answer
					self.deux_box = None
					return answer
				
				time.sleep(0.02)

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
			
			# self.test_thread = threading.Thread(target = self.run_test_thread, daemon = True)			
			# self.test_thread.start()
			
			self.play_thread = threading.Thread(name = "play_thread_1", target = self.run_play_thread, daemon = True)
			self.play_thread.start()
			self.play_thread_count = 1
			
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
		return int(i*(scr_wid-168)/7)
	
	this_folder = os.path.dirname(os.path.realpath(__file__))
	
	scr_wid = 800
	scr_hei = 600

	BLACK_COLOUR = (0, 0, 0)
	WHITE_COLOUR = (255, 255, 255)
	GREEN_COLOUR = (0, 128, 0)
	GREY_COLOUR = (64, 64, 64)
	RED_COLOUR = (255, 0, 0)
	BLUE_COLOUR = (0, 0, 255)
	YELLOW_COLOUR = (255, 255, 0)
	LIGHT_BLUE_COLOUR = (255, 120, 110)
	
	class MouseButtons:
		LEFT = 1
		MIDDLE = 2
		RIGHT = 3
		WHEEL_UP = 4
		WHEEL_DOWN = 5

	LOG.debug("Create GUI window ...")
	pygame.init()
	pygame.font.init()
	
	myfont = pygame.font.Font('freesansbold.ttf', 30)
	
	scr = pygame.display.set_mode((scr_wid, scr_hei))

	background = pygame.Surface(scr.get_size())
	background = background.convert()
	
	stabar_hei = 30
	stabar = pygame.Surface((scr_wid, stabar_hei))
	stabar = stabar.convert()
	stabar.set_alpha(220)

	FPS = 30

	# table cards coordinates
	tx = 320
	ty = 120
	to1, to2 = 70, 10
	table_coord_l = [
		(tx - to2, ty + to1), # human player
		(tx - to1, ty - to2),
		(tx + to2, ty - to1),
		(tx + to1, ty + to2),
	]

	# hand coordinates
	hand_y_idle = scr_hei - 120
	hand_y_sel_offset = -50

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
	suit_images_d = {}
	for fname in ['pique', 'coeur', 'carreau', 'trefle']:
		suit_images_d[fname] = pygame.image.load(os.path.join(this_folder, r'..\images\cards\{}.png'.format(fname)))
		suit_images_d[fname].convert_alpha()
		# suit_images_d[fname] = pygame.transform.smoothscale(suit_images_d[fname], (stabar_hei, stabar_hei))
	suit_images_small_d = {}
	for fname in ['pique', 'coeur', 'carreau', 'trefle']:
		suit_images_small_d[fname] = pygame.image.load(os.path.join(this_folder, r'..\images\cards\{}.png'.format(fname)))
		suit_images_small_d[fname].convert_alpha()
		suit_images_small_d[fname] = pygame.transform.smoothscale(suit_images_d[fname], (stabar_hei, stabar_hei))
	small_deck_image = pygame.image.load(os.path.join(this_folder, r'..\images\cards\small_deck.png'))
	dos_image = pygame.image.load(os.path.join(this_folder, r'..\images\cards\dos.png'))
	
	disabled_card_surface = pygame.Surface(card_images_d['Pique']['7'].get_size())
	disabled_card_surface.fill(GREY_COLOUR)
	disabled_card_surface.set_alpha(128)
	disabled_card_surface.convert_alpha()
	
	atout_bg = pygame.Surface(suit_images_small_d[fname].get_size())
	atout_bg.fill(YELLOW_COLOUR)
	
	hj_i = 0 # human joueur id
	b_obj = Belote(hj_i)
	LOG.debug("Start belote thread ...")
	b_obj.start_all_threads()
	time.sleep(0.1)

	# surfaces for names of the joueurs
	j_loc_d = {"human":{},"left":{},"top":{},"right":{},}
	
	j_loc_d['human']['j_index'] = (hj_i+0)%4
	j_loc_d['left' ]['j_index'] = (hj_i+1)%4
	j_loc_d['top'  ]['j_index'] = (hj_i+2)%4
	j_loc_d['right']['j_index'] = (hj_i+3)%4
	
	j_loc_d[(hj_i+0)%4] = 'human'
	j_loc_d[(hj_i+1)%4] = 'left'
	j_loc_d[(hj_i+2)%4] = 'top'
	j_loc_d[(hj_i+3)%4] = 'right'

	j_loc_d['human']['name_surface'] = myfont.render(b_obj.joueurs_l[(hj_i+0)%4].name, True, (0, 0, 0))
	j_loc_d['left' ]['name_surface'] = myfont.render(b_obj.joueurs_l[(hj_i+1)%4].name, True, (0, 0, 0))
	j_loc_d['top'  ]['name_surface'] = myfont.render(b_obj.joueurs_l[(hj_i+2)%4].name, True, (0, 0, 0))
	j_loc_d['right']['name_surface'] = myfont.render(b_obj.joueurs_l[(hj_i+3)%4].name, True, (0, 0, 0))
	
	j_loc_d['human']['name_coord'] = (int(3*scr_wid/4), scr_hei-stabar_hei )
	j_loc_d['left' ]['name_coord'] = (0               , int(1*scr_hei/9)   )
	j_loc_d['top'  ]['name_coord'] = (int(scr_wid/2)  , 0                  )
	j_loc_d['right']['name_coord'] = (scr_wid - 100   , int(5*scr_hei/9)   )
	
	j_loc_d['human']['atout_coord'] = (j_loc_d['human']['name_coord'][0] - stabar_hei , j_loc_d['human']['name_coord'][1]              )
	j_loc_d['left' ]['atout_coord'] = (j_loc_d['left' ]['name_coord'][0]              , j_loc_d['left' ]['name_coord'][1] + stabar_hei )
	j_loc_d['top'  ]['atout_coord'] = (j_loc_d['top'  ]['name_coord'][0] - stabar_hei , j_loc_d['top'  ]['name_coord'][1]              )
	j_loc_d['right']['atout_coord'] = (j_loc_d['right']['name_coord'][0]              , j_loc_d['right']['name_coord'][1] + stabar_hei )

	j_loc_d['human']['speech_text'] = None
	j_loc_d['left' ]['speech_text'] = None
	j_loc_d['top'  ]['speech_text'] = None
	j_loc_d['right']['speech_text'] = None

	j_loc_d['human']['speech_coord'] = (j_loc_d['right']['name_coord'][0]                , j_loc_d['human']['name_coord'][1]              )
	j_loc_d['left' ]['speech_coord'] = (j_loc_d['left' ]['name_coord'][0]                , j_loc_d['left' ]['name_coord'][1] - stabar_hei )
	j_loc_d['top'  ]['speech_coord'] = (j_loc_d['top'  ]['name_coord'][0] + 4*stabar_hei , j_loc_d['top'  ]['name_coord'][1]              )
	j_loc_d['right']['speech_coord'] = (j_loc_d['right']['name_coord'][0]                , j_loc_d['right']['name_coord'][1] - stabar_hei )
	
	font_18 = pygame.font.Font('freesansbold.ttf', 16)
	
	LOG.debug("Start GUI main thread ...")
	b_playing = True
	last_refreshed_time = 0
	while b_playing:
	
		human_j = b_obj.joueurs_l[hj_i]
	
		# pygame events
		b_left_click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				b_playing = False # pygame window closed by user
				b_obj.stopAllThreads()
			elif event.type == pygame.MOUSEMOTION:
				mouse_pos = pygame.mouse.get_pos()
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == MouseButtons.LEFT:
				b_obj.b_left_click = True
				b_left_click = True
				# LOG.info(mouse_pos)
			
			if b_obj.yesno_box is not None: 			
				b_obj.yesno_box.handle_event(event)
			
			if b_obj.deux_box is not None: 			
				b_obj.deux_box.handle_event(event)
		
		# update card selection
		b_hand_card_selected_l = [False]*8
		if human_j.allowed_card_index_l is not None:
			if mouse_pos[1] > hand_y_idle + hand_y_sel_offset: 
				
				for hand_i in range(8):
							
					if hand_i in human_j.allowed_card_index_l:
					
						# if mouse_pos[0] >= get_hand_x(7+1):
							# b_hand_card_selected_l[7] = True
							
						if mouse_pos[0] >= get_hand_x(hand_i) and mouse_pos[0] < get_hand_x(hand_i+1):
							b_hand_card_selected_l[hand_i] = True
							break
				
				if b_left_click:
					human_j.human_choice = hand_i
		
		# update question box if necessary
		if b_obj.yesno_box is not None: 
			b_obj.yesno_box.update()
		if b_obj.deux_box is not None:		
			b_obj.deux_box.update()
		
		# the nice green background
		background.fill(GREEN_COLOUR)		
		
		# other players' hands
		for c_i, c in enumerate(b_obj.joueurs_l[(hj_i+1)%4].hand_l):
			background.blit(dos_image, (-140+16*c_i, 150+6*c_i))
		for c_i, c in enumerate(b_obj.joueurs_l[(hj_i+2)%4].hand_l):
			background.blit(dos_image, (60+16*c_i, -230+6*c_i))
		for c_i, c in enumerate(b_obj.joueurs_l[(hj_i+3)%4].hand_l):
			background.blit(dos_image, (770-16*c_i, 50-6*c_i))

		# update table
		for table_i, table_card in enumerate(b_obj.table_l):
			
			table_coord_i = (table_i - hj_i + b_obj.winning_player)%4
			
			table_x = table_coord_l[table_coord_i][0]
			table_y = table_coord_l[table_coord_i][1]
			background.blit(card_images_d[table_card.suit][table_card.rank], (table_x, table_y))
			
		# update card sprites
		for hand_i, hand_card in enumerate(human_j.hand_l):
			
			hand_x = get_hand_x(hand_i)
			hand_y = hand_y_idle + hand_y_sel_offset*b_hand_card_selected_l[hand_i]
			
			background.blit(card_images_d[hand_card.suit][hand_card.rank], (hand_x, hand_y))
			if human_j.allowed_card_index_l is not None:
				if hand_i not in human_j.allowed_card_index_l:
					background.blit(disabled_card_surface, (hand_x, hand_y))
		
		# STATUS BAR
		stabar.fill(WHITE_COLOUR)
		background.blit(stabar, (0, scr_hei - stabar_hei))

		# display players' names
		background.blit(j_loc_d['left' ]['name_surface'], j_loc_d['left' ]['name_coord'])
		background.blit(j_loc_d['top'  ]['name_surface'], j_loc_d['top'  ]['name_coord'])
		background.blit(j_loc_d['right']['name_surface'], j_loc_d['right']['name_coord'])
		background.blit(j_loc_d['human']['name_surface'], j_loc_d['human']['name_coord'])	
		
		if b_obj.deck_l != []:		
			# dealer icon
			dealer_str = j_loc_d[b_obj.dealer]
			background.blit(small_deck_image, j_loc_d[dealer_str]['atout_coord'])

		# atout icon
		if (b_obj.atout is not None) and (b_obj.preneur is not None):
			atout_image = suit_images_small_d[b_obj.atout.lower()]
			pr = j_loc_d[b_obj.preneur]
			# background.blit(atout_bg, j_loc_d[pr]['atout_coord'])
			background.blit(atout_image, j_loc_d[pr]['atout_coord'])
		
		# speech
		for j_index in range(4):
			j_key = j_loc_d[j_index]
			if j_loc_d[j_key]['speech_text'] is not None:
				background.blit(font_18.render(j_loc_d[j_key]['speech_text'], True, LIGHT_BLUE_COLOUR), j_loc_d[j_key]['speech_coord'])
			
		# draw question box if necessary
		if b_obj.yesno_box is not None: 
			b_obj.yesno_box.draw(background)
		if b_obj.deux_box is not None:
			b_obj.deux_box.draw(background)
			
		# status message
		if b_obj.message_box is not None:
			b_obj.message_box.draw(background)	
	
		# Screen refresh
		now = time.time()
		if (now - last_refreshed_time) > (1/FPS):
			scr.blit(background, (0, 0))
			pygame.display.flip()
			last_refreshed_time = time.time()
		else:
			milliseconds_left = int(1000*((1/FPS) - (now - last_refreshed_time)))
			pygame.time.wait(milliseconds_left)
			
## -------- SOMETHING WENT WRONG -----------------------------	
except:

	import traceback
	LOG.error("Something went wrong! Exception details:\n{}".format(traceback.format_exc()))

## -------- GIVE THE USER A CHANCE TO READ MESSAGES-----------
finally:
	
	pygame.quit()
	# input("Press any key to exit ...")
