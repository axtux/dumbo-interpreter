import ply.lex as lex

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
}

tokens = [
  # transitions tokens
  'CODESTART',
  'CODEEND',
  
  # TEXT tokens
  'TEXT',
  
  # CODE tokens
  'ASSIGNATION',
  'CONCATENATION',
  'COMA',
  'SEMICOLON',
  
  'LEFT_PARENTHESE',
  'RIGHT_PARENTHESE',
  
  'VARIABLE',
  'STRING',
] + list(reserved.values())


"""
    TEXT lexemes
"""

def t_TEXT_TEXT(t) :
  r'[a-zA-Z0-9:,;&<>"./\\\n\t _-]+'
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

def t_CODE_VARIABLE(t) :
  r'[a-zA-Z0-9_]+'
  t.type = reserved.get(t.value, 'VARIABLE')
  return t

# TODO manage newline within string
def t_CODE_STRING(t) :
  r'\'[a-zA-Z0-9:,;&<>"./\\\n\t _-]+\''
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



# Build lexer from this file
lexer = lex.lex(debug=1)

# start in TEXT state
lexer.begin('TEXT')

# set lastlinepos to 0
lexer.lastlinepos = 0

# Launch analysis with system input
if __name__ == "__main__" :
  import sys
  
  lexer.input(sys.stdin.read())
  
  for token in lexer :
    print("line %d : %s : '%s'"%(token.lineno, token.type, token.value))
