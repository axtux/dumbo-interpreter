import sys
from ply import lex

"""
    States
"""

states = (
  ('TEXT', 'inclusive'),
  ('CODE', 'inclusive'),
)

"""
    States transitions
"""

def t_TEXT_CODESTART(t) :
  r'{{'
  t.lexer.begin('CODE')
  return t

def t_CODE_CODEEND(t) :
  r'}}'
  t.lexer.begin('TEXT')
  return t


"""
    Tokens
"""

reserved = {
  'print' : 'PRINT',
  'for'   : 'FOR',
  'in'    : 'IN',
  'do'    : 'DO',
  'endfor': 'ENDFOR',
  'if'    : 'IF',
  'endif' : 'ENDIF',
  'and'   : 'AND',
  'or'    : 'OR',
}

tokens = [
  # transitions tokens
  'CODESTART',
  'CODEEND',
  
  # TEXT tokens
  'TEXT',
  
  # CODE tokens
  'COMA',
  'SEMICOLON',
  
  'LEFT_PARENTHESE',
  'RIGHT_PARENTHESE',
  
  'ASSIGNATION',
  'CONCATENATION',
  'COMPARATOR',
  
  'PLUS',
  'MINUS',
  'TIMES',
  'DIVIDE',

  'VARIABLE',
  'BOOLEAN',
  'INTEGER',
  'STRING',
] + list(reserved.values())


"""
    TEXT lexemes
"""

def t_TEXT_TEXT(t) :
  r'(?:[^{]|{[^{])+'
  #r'[a-zA-Z0-9:,;&<>"./\\\n\t _-]+'
  update_line_info(t)
  return t


"""
    CODE lexemes
"""

t_CODE_ASSIGNATION = r':='
t_CODE_CONCATENATION = r'\.'
t_CODE_COMA = r','
t_CODE_SEMICOLON = r';'

t_CODE_LEFT_PARENTHESE = r'\('
t_CODE_RIGHT_PARENTHESE = r'\)'


t_CODE_PLUS = r'\+'
t_CODE_MINUS = r'-'
t_CODE_TIMES = r'\*'
t_CODE_DIVIDE = r'/'

t_CODE_COMPARATOR = r'<|>|!=|='


def t_CODE_INTEGER(t) :
  r'[0-9]+'
  t.value = int( t.value)
  return t

def t_CODE_BOOLEAN(t) :
  r'true|false'
  t.value = True if t.value == 'true' else False
  return t

def t_CODE_VARIABLE(t) :
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value, 'VARIABLE')
  return t

def t_CODE_STRING(t) :
  r'\'(?:.|\n)*?\''
  # . does not match newline
  #r'\'[a-zA-Z0-9:,;&<>"./\\\n\t =_-]+\''
  update_line_info(t)
  t.value = t.value[1:-1]
  return t

t_CODE_ignore = ' |\t'


"""
    Universal lexemes
"""

def t_NEWLINE(t) :
  r'\n+'
  update_line_info(t)

def update_line_info(t) :
  line_rel_indexes = [i for i in range(len(t.value)) if t.value[i] == '\n']
  # get absolute index of first character of each line
  line_abs_indexes = list(map(lambda x : x+t.lexpos+1, line_rel_indexes))
  
  t.lexer.lineno += len(line_abs_indexes)
  line_indexes.extend(line_abs_indexes)

# special token containing ignored characters (not regex)
t_ignore = ''

def t_error(t) :
  print('Skipping illegal character %s on line %s, char %s'.format(t.value[0], t.lineno, charno(t)))
  t.lexer.skip(1)


def reset() :
  # start in TEXT state
  lexer.begin('TEXT')
  
  # reset line references
  lexer.lineno = 1
  lexer.lexpos = 0
  
  global line_indexes
  line_indexes = [0]

def charno(t) :
  'Return index of token relative to its line, starting at 1'
  for i in line_indexes :
    if i > t.lexpos :
      break
    last = i
  
  return t.lexpos-last+1

def parse_file(filename) :
  import file
  
  data = file.get_contents(filename)
  if data == None :
    return print('file "{}" not readable'.format(filename))
  
  reset()
  lexer.input(data)
  
  return lexer

def init() :
  'read command line arguments and init lexer'
  debug = 0
  
  for arg in sys.argv :
    if arg == '-d' or arg == '--debug' :
      debug = 1
  
  # init lexer with defined tokens in this file
  global lexer
  lexer = lex.lex(debug=debug)
  reset()


def main() :
  argc = len(sys.argv)
  if argc < 2 :
    exit('Usage: python3 {} file_to_parse'.format(sys.argv[0]))
  
  lex = parse_file(sys.argv[1])
  if lex == None :
    return
  
  for token in lex :
    print('line {}, char {} : {} : {!r} '.format(token.lineno, charno(token), token.type, token.value))



init()

if __name__ == "__main__" :
  main()
