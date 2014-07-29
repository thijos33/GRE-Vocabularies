## Vocabs for the GRE ##
# purpose: Make it fun and easy to learn them

import random, os, sys
from all_vocabs import gre_vocabs

heading = "Let's play a vocabulary game!\n-----------------------------"

def print_header(message):
  print reindent(message, 16)

# get the number of random vocabularies to generate
def get_input_random():
  surprise_vocabs = raw_input('\n>>> How many random vocabularies do you want to define? ')
  exit_game(surprise_vocabs)
  verified_input = check_input(surprise_vocabs)
  
  if str(verified_input) == str(False):
    get_input_random()
    get_input_specific()
    sys.exit()
  else:
    get_random_vocabs(verified_input)

# get the number of specified vocabularies to look up
def get_input_specific():
  desired_vocabs = raw_input('\n>>> How many vocabularies do you want to look up? ')
  exit_game(desired_vocabs)
  verified_input = check_input(desired_vocabs)
  if str(verified_input) == str(False):
    get_input_specific()
    sys.exit()
  else:
    get_specific_vocabs(verified_input)

# check if input type is correct
def check_input(word):
  try:
    arg = int(word)
    if arg >= 0:
      if arg <= len(gre_vocabs):
        return arg
      else:
        print '    Please enter a number smaller than %i.' % (len(gre_vocabs))
        return False
    else:
      print '    Please enter a positive number.'
      return False
    
  except ValueError:
    print '    Please enter a number.'
    return False

# generate random vocabularies
def get_random_vocabs(number):
  guessed_vocabs = []
  for n in range(number):
    rand_vocab = random.choice(gre_vocabs.keys())
    
    if rand_vocab in guessed_vocabs:
        continue
    def_vocab = vocab_present(rand_vocab)
    if str(def_vocab) == str(False):
      continue
    else:
      answer_vocab = raw_input('\n    Define %s: ' % (rand_vocab))
      exit_game(answer_vocab)
      print '\n    Definition: \n', reindent(def_vocab, 4)
    guessed_vocabs.append(rand_vocab)

# define specific vocabularies
def get_specific_vocabs(number):

  if number == 0:
    print '\n'
    replay()
  print '\n    Specific vocabularies. Choose from :\n'
  n_voc, voc_str = 0, "    "
  for vocab in gre_vocabs:
    n_voc += 1
    
    if n_voc == len(gre_vocabs):
      voc_str += vocab + '.'
    else:
      voc_str += vocab + ','
      
    if n_voc % 5 == 0:
      print voc_str
      voc_str = '    '
  print voc_str
  print '\n'
  
  for n in range(number):
    new_vocab = raw_input('\n    Enter a vocabulary: ')
    exit_game(new_vocab)
    def_vocab = vocab_present(new_vocab.lower())
    if str(def_vocab) == str(False):
      continue
    else:
      answer_vocab = raw_input('\n    Define %s: ' % (new_vocab))
      exit_game(answer_vocab)
      print '\n    Definition : \n', reindent(def_vocab, 4)

  print '\n'

def reindent(string, num_spaces):
  string = string.split('\n')
  string = [(num_spaces * ' ') + line for line in string]
  string = '\n'.join(string)
  return string

def vocab_present(vocab):
  try:
    presence = gre_vocabs[vocab]
  except KeyError:
    print '    %s is currently not available\n' % (vocab)
    return False
  return presence

def replay():
  question = raw_input('    Do you want to play again? (yes/no) ')
  if question in ['yes','Y','YES','Yes','y']:
    main()
  if question in ['no','N','NO','No', 'n']:
    print reindent('\nThanks for playing!!!\n', 16)
    sys.exit()
  else:
    sys.exit()

def exit_game(user_input):
  if user_input in ['quit', 'exit']:
    sys.exit()
    
print_header(heading)

def main():
  get_input_random()
  get_input_specific()
  replay()
main()
 
