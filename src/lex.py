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
t_CODE_DIVIDE = r'/+'

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
  r'\'.*?\''
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

"""
    read arguments from command line
"""

debug = 0

import sys

for arg in sys.argv :
  if arg == '-d' or arg == '--debug' :
    debug = 1


"""
    Init lexer
"""

# Build lexer from this file
lexer = lex.lex(debug=debug)

# start in TEXT state
lexer.begin('TEXT')

# set lineno to 0
lexer.lineno = 1

# set lastlinepos to 0
lexer.lastlinepos = 0


"""
    Launch analysis with system input if main script
"""

if __name__ == "__main__" :
  lexer.input(sys.stdin.read())
  
  for token in lexer :
    print('line {} : {} : {!r} '.format(token.lineno, token.type, token.value))
