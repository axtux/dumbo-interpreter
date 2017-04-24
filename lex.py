import ply.lex as lex

tokens = (
  'TEXT',
  'CODE',
)

states = (
  ('text', 'exclusive'),
)

def t_TEXT_START(t) :
  r'}}'
  t.lexer.begin('text')

# Text mode
t_text_TEXT = r'[a-zA-Z0-9:,;&<>"./\\\n\t _-]+'

def t_text_TEXT_END(t) :
  r'{{'
  t.lexer.begin('INITIAL')

def t_NEWLINE(t) :
  r'\n'
  t.lexer.lineno += 1

# special token containing ignored characters (not regex)
t_ignore = ' |\t'

# special token
def t_error(t) :
  print("Illegal character '%s'"%t.value[0])
  t.lexer.skip(1)


import sys
lexer = lex.lex(debug=1)
# start in text mode
lexer.begin('text')
lexer.input(sys.stdin.read())

for token in lexer :
  print("line %d : %s (%s)"%(token.lineno, token.type, token.value))
