# This code uses the "PyDictionary" library by Pradipta Bora, licensed under the MIT License.

from PyDictionary import PyDictionary

import os
import time

#                      DATA STRUCTURE                      #
# <word> <stage> <last_review_time> 

stages = {'0':0, '1':1, '2':3, '3':7, '4':14, '5':30, '6':60, '7':90, '8':120, '9':360, '10':900}
dict = PyDictionary()

class Word():
    # clss of each word stored in database
    def __init__(self, word, stage = 0, last_review_time = time.time()) -> None:
        # initialization
        self.word = word
        self.stage = int(stage)
        self.last_rv = float(last_review_time)
    
    def will_review(self): 
        # returns true if time for review has come
        if (time.time() - self.last_rv)/86400 > float(stages[str(self.stage)]):
            return True
        elif self.last_rv == 0:
            return True
        else:
            return False 
        
    def print_meaning(self):
        # prints the definition(s) in a structured form
        definitions = dict.meaning(self.word) 
        # definitions is a dict with keys such as 'Noun' and values that are lists
        for type in definitions:
            print(f"{type}:")
            for definition in definitions[type]:
                print(f"--> {definition}") 

def get_words(filename):
    # this function returns all words in filename as a list
    words_list = []
    with open(filename, 'r+') as file:
        data = file.readlines() # data is a list of every line as a string
        for line in data:
            word_data = line.split() # word_data is a list of all items in a line
            word = Word(word_data[0], word_data[1], word_data[2])
            words_list.append(word)
    return words_list

def review(words_list):
    # review words and renew their stages
    if len(words_list) == 0:
        print("No words in the database!")
        return None
    for word in words_list:
        if word.will_review():
            word.last_rv = time.time()
            knowledge = input(f"\n{word.word}: yes or no?")
            if knowledge == 'y':
                word.stage += 1
            else:
                if word.stage != 0:
                    word.stage -= 1
                word.print_meaning()
    return None
       
def insert(words_list, *args):
    # insert a series of new words and return new list
    for word in args:
        new_word = Word(word, 1, time.time()) 
        words_list.append(new_word)
    return words_list

def overwrite(filename, words_list):
    # updates the databse with renewed words
    with open(filename, 'w') as file:
        for word in words_list:
            file.write(f'{word.word} {word.stage} {word.last_rv}' + '\n')
    return None

def main(database):
    # main game logic
    words_list = get_words(database)
    while True:
        mode = input("Select mode review (r), insert (i) or (q) to quit: ")
        if mode.lower() == 'i':
            new_words_string = input("Enter new words seperated by a space: ")
            new_words_list = new_words_string.split(" ")
            for word in new_words_list:
                words_list.append(Word(word, 0, time.time()))
            overwrite(database,words_list)         
        elif mode.lower() == 'r':
            review(words_list)
            overwrite(database,words_list)         
        elif mode.lower() == "q":
            exit()
        else:
            print("Invalid mode!\n")