## Vocabs for the GRE ##
# purpose: Make it fun and easy to learn them

import random, os, sys, time, threading
import ScrolledText as tkst
from all_vocabs import gre_vocabs
from Tkinter import *

## Global constants ##

heading = "\n\nLET'S PLAY A VOCABULARY GAME!\n-----------------------------"
usage = """\nTIPS: \n----\nType 'def' to get the definition of any vocabulary.\n\
Type 'hint' to get a hint for any vocabulary.\n\
Type 'ex', 'eg' or 'example' to get an example for a vocabulary's use. \n\
Type 'quit' or 'exit' to leave the program at anytime.
Type the definition starting with 'n ' (notice space) to\n     check the number of random vocabularies defined.\n\n"""

num_random = '\n>>> How many random vocabularies do you want to define? '
num_specific = '\n>>> How many vocabularies do you want to look up? '
num_max_voc = '\n    Please enter a number eqaul or smaller than %i.' % (len(gre_vocabs)-1)
gui_title = "AVAILABLE VOCABULARIES"
vocabs_str = ''
example_status = False
guessed_vocabs = []
after_hint = 0
after_example = 0
definition_status = False

## Defined functions ##

def print_header(head, usage):
  print reindent(head, 16)
  print reindent(usage, 8)

# get the number of random vocabularies to generate
def get_num_voc(question):
  num_vocabs = raw_input(question)
  exit_game(num_vocabs)
  verified_input = check_input(num_vocabs)
  
  if str(verified_input) == str(False):
    if question == num_random:
      get_random_vocabs(get_num_voc(num_random))
      get_specific_vocabs(get_num_voc(num_specific))
    if question == num_specific:
      get_specific_vocabs(get_num_voc(num_specific))
    replay()
  else:
    return verified_input

# check if input type is correct
def check_input(num):
  try:
    arg = int(num)
    if arg >= 0:
      if arg <= len(gre_vocabs)-1:
        return arg
      else:
        print num_max_voc
        return False
    else:
      print '\n    Please enter a positive number.'
      return False
    
  except ValueError:
    print '\n    Please enter a number.'
    return False
  
# check if a hint is requested
def is_hint(answer):
  if answer.lower() == 'hint':
    return True

# check if an example is requested
def is_example(answer):
  if answer.lower() in ['ex', 'eg','example']:
    return True
  
# Define again after seeing hint or example
def define_again(word):
  answer = raw_input('\n    %s (%s): ' % (word, gre_vocabs[word.lower()][0]))
  exit_game(answer)
  get_num_done_vocabs(answer)
  if is_hint(answer) == True or is_example(answer) == True:
    print_definition(answer, word)

# check if an e.g. was requested
def set_eg_status(status):
  global example_status
  example_status = status

# update after calling get_hint
def update_hint():
  global after_hint
  after_hint += 1

# upddate after calling get_example
def update_example():
  global after_example
  after_example += 1

# check definitions of words in the 'dictionary'
def vocab_present(vocab):
  try:
    presence = gre_vocabs[vocab.lower()]
  except KeyError:
    print '    "%s" is currently not available\n' % (vocab)
    return False
  return presence[1]

# indent strings
def reindent(string, num_spaces):
  string = string.split('\n')
  string = [(num_spaces * ' ') + line for line in string]
  string = '\n'.join(string)
  return string

# save previous random words
def done_words(word):
  global guessed_vocabs
  
  if len(guessed_vocabs) == len(gre_vocabs)-1:
    print "\n>>> You have seen all vocabularies!!!\n"
    guessed_vocabs = []
    return False  
  if word in guessed_vocabs:
    return True 

  if word not in guessed_vocabs:
    guessed_vocabs.append(word)
    return False

# check a hint
def get_hint(vocab):
  m = 0
  space_1, space_2 = False, False
  definition = vocab_present(vocab.lower())
    
  for n in range(len(definition)):
      
    if definition[n] == ' ':
      m += 1
    if m == 1 and definition[n] == ' ':
      w = n
    if m == 2 and definition[n] == ' ':
      v = n
      space_1 = True
    if m == 3:
      print_hint(n, vocab, definition)
      space_2 = True
      break
    if m == 0 and len(definition) == len(definition[:n+1]):
      print_hint(n, vocab, definition)
      break      
    if len(definition[:n+1])  == len(definition) and space_1 == False:
      print_hint(w, vocab, definition)
      break
      
    if len(definition[:n+1]) == len(definition) and space_2 == False:
      print_hint(v, vocab, definition)
      break
  
# print hint
def print_hint(num, word, definition):
  if definition[num-1] in ['.',';',':','!','?']:
    hint = 'Hint: '+ definition[:num-1] + ' ...'
  else:
    hint = 'Hint: '+ definition[:num+1] + '...'
    
  print reindent(hint, 4)
  define_again(word)
  
# get an example of vocabulary in a sentence
def get_example(word):
  example = gre_vocabs[word.lower()][2]
  print reindent('\n  + Example: ', 0)
  print reindent(example, 4)
  define_again(word)

# check the number of finished vocabularies

def get_num_done_vocabs(answer):
  if answer[:2] == 'n ':
    print "\n    [You have defined %i vocabularies]" % (len(guessed_vocabs))
    
# generate random vocabularies
def get_random_vocabs(number):
  global definition_status
  loop_random = range(number)
  
  for n in loop_random:
    definition_status = False
    rand_number = random.randint(0,len(gre_vocabs)-1)
    rand_vocab = gre_vocabs.keys()[rand_number]

    if rand_vocab == 'am':
      loop_random.append(len(loop_random))
      continue
    
    if done_words(rand_vocab) == True:
      loop_random.append(len(loop_random))
      continue
    
    else:
      word_type = gre_vocabs[rand_vocab.lower()][0]
      def_vocab = vocab_present(rand_vocab)
      answer_vocab = raw_input('\n    %s (%s): ' % (rand_vocab, word_type))
      exit_game(answer_vocab)
      print_definition(answer_vocab, rand_vocab)
      get_num_done_vocabs(answer_vocab)

# make a string of all available vocabs
def get_vocabs_str():
  global vocabs_str
  n_voc, voc_str, len_str = 0, "", 0
  for vocab in sorted(gre_vocabs.keys()):
    n_voc += 1
    
    if vocab == 'am':
      n_voc -= 1
      continue
    if n_voc == len(gre_vocabs)-1:
      voc_str += vocab + '.\n'
    else:
      voc_str += vocab + ', '
      
    if (len(voc_str) - len_str) > 50:
      voc_str += '\n'
      n_cov = 0
      len_str = len(voc_str)
      
  vocabs_str = voc_str
  
# display all vocabs in a GUI
class display_vocabs(threading.Thread):
  
  def __init__(self):
    threading.Thread.__init__(self)
    self.start()
  def callback(self):
    self.root.quit()
  def run(self):
    self.root = Tk()
    self.root.protocol("WM_DELETE_WINDOW", self.callback)
    frame1 = Frame(
            self.root,
            background = '#C0C0C0'
                
    )
    frame1.pack(fill='both', expand='yes')
    editArea = tkst.ScrolledText(
              master = frame1,
              wrap   = WORD,
              width  = 60,
              height = 35,
              bg = '#000000',
              fg = '#FFFFFF',
              font = ("Times New Roman", 11, "bold")
    )
    editArea.pack(padx=10, pady=10, fill= BOTH, expand=True)

    all_content = '\n' + reindent(gui_title, 20) + '\n\n' + reindent(vocabs_str, 10)
    editArea.insert(INSERT, all_content)
    self.root.mainloop()

# define specific vocabularies
def get_specific_vocabs(number):
  global definition_status
  loop_specific = range(number)
  if number == 0:
    print '\n'
    replay()
    
  for n in loop_specific:
    #display_vocabs()
    definition_status = False
    new_vocab = raw_input('\n    Enter a vocabulary: ')
    exit_game(new_vocab)
    def_vocab = vocab_present(new_vocab.lower())
    if str(def_vocab) == str(False):
      loop_specific.append(len(loop_specific))
      continue
    
    else:
      word_type = gre_vocabs[new_vocab.lower()][0]
      answer_vocab = raw_input('\n    %s (%s): ' % (new_vocab, word_type))
      exit_game(answer_vocab)
      print_definition(answer_vocab, new_vocab)
      

# print definitions & examples
def print_definition(answer, word):
  global after_hint
  global after_example
  global example_status
  global definition_status
  definition = gre_vocabs[word.lower()][1]
  example = gre_vocabs[word.lower()][2]

  if is_hint(answer) == True:
    update_hint()
    get_hint(word)
    
  if is_example(answer):
    set_eg_status(True)
    update_example()
    get_example(word)
  
  if (after_hint == 1 and after_example == 0) or (after_hint == 0 \
    and after_example == 1) or (after_hint == 0 and after_example == 0):
    
    if definition_status == False:
      if example_status == True:
        print '\n  - Definition : \n', reindent(definition, 4)
      else:
        print '\n  - Definition : \n', reindent(definition, 4)
        print '\n  + Example : \n', reindent(example, 4)
        
      definition_status = True
      
  if definition_status == True:
    set_eg_status(False)

  after_hint, after_example = 0, 0

# restart the program
def replay():
  question = raw_input('\n    Do you want to play again? (yes/no) ')
  exit_game(question)
  if question.lower() in ['yes','y']:
    main()
  if question.lower() in ['no','n']:
    print reindent('\nThanks for playing!!!\n', 16)
    time.sleep(1.5)
    sys.exit()
  else:
    print reindent('\nProgram is exiting ...\n', 16)
    time.sleep(1.5)
    sys.exit()

# exit the program
def exit_game(user_input):
  if user_input in ['quit', 'exit']:
    print reindent('\nKEEP CALM AND SEE YOU SOON :-) \n', 16)
    time.sleep(1.5)
    sys.exit()

# print welcome message & display vocabs   
print_header(heading, usage)
get_vocabs_str()
vocabs_gui = display_vocabs()

## main function ##

def main():
  get_random_vocabs(get_num_voc(num_random))
  get_specific_vocabs(get_num_voc(num_specific))
  replay()
  
main()
