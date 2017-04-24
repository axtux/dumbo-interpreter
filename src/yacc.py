from ply import yacc
# import lex.py lexemes
from lex import tokens

variables = {}

"""
    Grammar definition
"""

def p_program_textcode_program(p) :
  '''program : TEXT program
             | code program'''
  p[0] = p[1] + p[2]
  
def p_program_textcode(p) :
  '''program : TEXT
             | code'''
  p[0] = p[1]


def p_code_codeblock(p) :
  '''code : CODESTART codeblock CODEEND'''
  p[0] = p[2]

def p_codeblock_codeblock_codeline(p) :
  '''codeblock : codeblock codeline'''
  p[0] = p[1] + p[2]

def p_codeblock_codeline(p) :
  '''codeblock : codeline'''
  p[0] = p[1]

def p_codeline_instruction(p) :
  '''codeline : instruction SEMICOLON'''
  p[0] = p[1]


def p_instruction_print(p) :
  '''instruction : PRINT longstring'''
  p[0] = p[2]

def p_instruction_assign_string(p) :
  '''instruction : VARIABLE ASSIGNATION longstring
                 | VARIABLE ASSIGNATION stringlist'''
  assign(p.lineno(1), p[1], p[3])
  p[0] = ''

def p_instruction_for(p) :
  '''instruction : FOR VARIABLE IN enumarable DO codeblock ENDFOR'''
  name = p[2]
  p[0] = ''
  for value in p[4] :
    variables[name] = value
    p[0] += p[6]


def p_longstring_concat(p) :
  '''longstring : longstring CONCATENATION string'''
  p[0] = p[1] + p[3]

def p_printable_string(p) :
  '''longstring : string'''
  p[0] = p[1]

def p_string_var(p) :
  '''string : VARIABLE'''
  name = p[1]
  if name in variables :
    val = variables[name]
    if type(val) == type('') :
      p[0] = val
    else :
      yacc_error(p.lineno(1), 'variable {} is not string as expected'.format(name))
      p[0] = ''
  else :
    yacc_error(p.lineno(1), 'variable {} undefined'.format(name))
    p[0] = ''

def p_string_string(p) :
  '''string : STRING'''
  p[0] = p[1]

def p_enumarable_stringlist(p) :
  '''enumarable : stringlist'''
  p[0] = p[1]

def p_stringlist(p) :
  '''stringlist : LEFT_PARENTHESE stringnext RIGHT_PARENTHESE'''
  p[0] = p[2]

def p_stringnext_string(p) :
  '''stringnext : string'''
  p[0] = [p[1]]

def p_stringnext_stringnext(p) :
  '''stringnext : string COMA stringnext'''
  p[0] = [p[1]]
  p[0] = p[0] + p[3]

def p_error(p) :
  yacc_error(p.lineno, 'Syntax error')


"""
    Custom functions
"""
def yacc_warning(lineno, message) :
  print('WARNING', 'on line', lineno, ':', message)

def yacc_error(lineno, message) :
  print('ERROR:', 'on line', lineno, ':', message)

def assign(lineno, name, value) :
  if name in variables :
    yacc_warning(lineno, 'redefinition of variable {}'.format(name))
  variables[name] = value

"""
    Init parser
"""
parser = yacc.yacc(debug=1)

"""
    Launch parsing with system input if main script
"""

if __name__ == "__main__" :
  import sys
  
  result = parser.parse(sys.stdin.read())
  
  print('Output is {!r}'.format(result))
