from ply import yacc
# import lex.py lexemes
from lex import tokens

"""
    Grammar definition
"""

def p_program_subprogram_program(p) :
  '''program : subprogram program'''
  p[0] = p[1] + p[2]

def p_program_subprogram(p) :
  '''program : subprogram'''
  p[0] = p[1]

def p_subprogram_text(p) :
  '''subprogram : TEXT'''
  p[0] = [('print', p[1])]

def p_subprogram_code(p) :
  '''subprogram : code'''
  p[0] = p[1]


def p_code_codeblock(p) :
  '''code : CODESTART codeblock CODEEND'''
  p[0] = p[2]

def p_codeblock_codeblock_codeline(p) :
  '''codeblock : codeline codeblock'''
  p[0] = [p[1]] + p[2]

def p_codeblock_codeline(p) :
  '''codeblock : codeline'''
  p[0] = [p[1]]

def p_codeline_instruction(p) :
  '''codeline : instruction SEMICOLON'''
  p[0] = p[1]


def p_instruction_print(p) :
  '''instruction : PRINT longstring'''
  p[0] = ('print', p[2])

def p_instruction_assign_string(p) :
  '''instruction : VARIABLE ASSIGNATION longstring
                 | VARIABLE ASSIGNATION stringlist'''
  p[0] = ('assign', p[1], p[3])

def p_instruction_for(p) :
  '''instruction : FOR VARIABLE IN enumarable DO codeblock ENDFOR'''
  p[0] = ('for', p[2], p[4], p[6])


def p_longstring_concat(p) :
  '''longstring : longstring CONCATENATION string'''
  p[0] = ('concat', p[1], p[3])

def p_printable_string(p) :
  '''longstring : string'''
  p[0] = p[1]

def p_string_var(p) :
  '''string : VARIABLE'''
  p[0] = ('variable', p[1])

def p_string_string(p) :
  '''string : STRING'''
  p[0] = p[1]

def p_enumarable_stringlist(p) :
  '''enumarable : stringlist'''
  p[0] = p[1]

def p_enumarable_variable(p) :
  '''enumarable : VARIABLE'''
  p[0] = ('variable', p[1])

def p_stringlist(p) :
  '''stringlist : LEFT_PARENTHESE stringnext RIGHT_PARENTHESE'''
  p[0] = p[2]

def p_stringnext_string(p) :
  '''stringnext : string'''
  p[0] = [p[1]]

def p_stringnext_stringnext(p) :
  '''stringnext : string COMA stringnext'''
  p[0] = [p[1]] + p[3]

def p_expression_plus_minus(p):
  '''expression : expression PLUS term
                | expression MINUS term'''
  p[0] = (p[2], p[1] , p[3])

def p_expression_term(p):
  '''expression : term'''
  p[0] = p[1]

def p_term_times_divide(p):
  '''term : term TIMES factor
          | term DIVIDE factor'''
  p[0] = (p[2], p[1], p[3] )

def p_term_factor(p):
  '''term : factor'''
  p[0] = p[1]

def p_factor_num(p):
  '''factor : INTEGER'''
  p[0] = p[1]

def p_error(p) :
  yacc_error(p.lineno, 'Syntax error')


"""
    Custom functions
"""
def yacc_warning(lineno, message) :
  print('WARNING', 'on line', lineno, ':', message)

def yacc_error(lineno, message) :
  print('ERROR:', 'on line', lineno, ':', message)

"""
    read arguments from command line
"""

debug = 0

import sys

for arg in sys.argv :
  if arg == '-d' or arg == '--debug' :
    debug = 1

"""
    Init parser
"""
parser = yacc.yacc(debug=debug)

"""
    Launch parsing with system input if main script
"""

if __name__ == "__main__" :
  result = parser.parse(sys.stdin.read())
  
  #print('Output is {!r}'.format(result))
  print('Output is :\n')
  
  from pprint import pprint
  pprint(result)
