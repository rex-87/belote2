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
        
            return self.rank+self.suit_d[self.suit]
    
    class Joueur(object):
    
        def __init__(self, name):
        
            self.name = name
            self.hand = []
            
        def __repr__(self):
            
            return self.name
    
    class Belote(object):
    
        def __init__(self):
        
            self.deck_l    = CsvObjectGenerator(Carte ).generate_from_csv(csv_path = r'C:\Users\rex87\belote\belote\cartes.csv' )
            self.joueurs_l = CsvObjectGenerator(Joueur).generate_from_csv(csv_path = r'C:\Users\rex87\belote\belote\joueurs.csv')
            
        def play(self):
            
            random.shuffle(self.deck_l)
            print(self.deck_l)
            print(self.joueurs_l)
    
    Belote().play()

## -------- SOMETHING WENT WRONG -----------------------------    
except:

    import traceback
    LOG.error("Something went wrong! Exception details:\n{}".format(traceback.format_exc()))

## -------- GIVE THE USER A CHANCE TO READ MESSAGES-----------
finally:
    
    input("Press any key to exit ...")
