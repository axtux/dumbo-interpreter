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
  t.value = t.value[1:-1]
  update_line_info(t)
  return t

t_CODE_ignore = ' |\t'


"""
    Universal lexemes
"""

def t_NEWLINE(t) :
  r'\n+'
  update_line_info(t)

def update_line_info(t) :
  t.lexer.lineno += t.value.count('\n')
  lastlineindex = t.value.rfind('\n')
  if lastlineindex != -1 :
    t.lexer.lastlinepos = t.lexpos + lastlineindex+1

# special token containing ignored characters (not regex)
t_ignore = ''

def t_error(t) :
  print("Skipping illegal character %s on line %s, column %s"%(t.value[0], t.lineno, t.lexpos-t.lexer.lastlinepos))
  t.lexer.skip(1)


def reset() :
  # start in TEXT state
  lexer.begin('TEXT')
  
  # reset line references
  lexer.lineno = 1
  lexer.lexpos = 0
  lexer.lastlinepos = 0

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

init()

if __name__ == "__main__" :
  'analyze standard input'
  lexer.input(sys.stdin.read())
  
  for token in lexer :
    print('line {} : {} : {!r} '.format(token.lineno, token.type, token.value))
