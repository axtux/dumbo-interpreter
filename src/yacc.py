import sys
import ply.yacc
import lex
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
  p[0] = [('print', infos(p), p[1])]

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
  '''instruction : PRINT stringop'''
  p[0] = ('print', infos(p), p[2])

def p_instruction_assign(p) :
  '''instruction : VARIABLE ASSIGNATION boolop
                 | VARIABLE ASSIGNATION intop
                 | VARIABLE ASSIGNATION stringop
                 | VARIABLE ASSIGNATION stringlist'''
  p[0] = ('assign', infos(p), p[1], p[3])

def p_instruction_for(p) :
  '''instruction : FOR VARIABLE IN enumarable DO codeblock ENDFOR'''
  p[0] = ('for', infos(p), p[2], p[4], p[6])

def p_instruction_if(p) :
  '''instruction : IF boolop DO codeblock ENDIF'''
  p[0] = ('if', infos(p), p[2], p[4])


def p_boolop_boolop_bool(p) :
  '''boolop : boolop AND bool
            | boolop OR bool'''
  p[0] = (p[2], infos(p), p[1], p[3])

def p_boolop_bool(p) :
  '''boolop : bool'''
  p[0] = p[1]

def p_bool_boolean(p) :
  '''bool : BOOLEAN'''
  p[0] = p[1]

def p_bool_comparison(p) :
  '''bool : comparison'''
  p[0] = p[1]

def p_comparison(p) :
  '''comparison : intop COMPARATOR intop'''
  p[0] = (p[2], infos(p), p[1], p[3])


def p_stringop_concat(p) :
  '''stringop : string CONCATENATION stringop'''
  p[0] = (p[2], infos(p), p[1], p[3])

def p_stringop_string(p) :
  '''stringop : string'''
  p[0] = p[1]


def p_string_var(p) :
  '''string : variable'''
  p[0] = p[1]

def p_string_string(p) :
  '''string : STRING'''
  p[0] = p[1]

def p_enumarable_stringlist(p) :
  '''enumarable : stringlist'''
  p[0] = p[1]

def p_enumarable_variable(p) :
  '''enumarable : variable'''
  p[0] = p[1]

def p_stringlist(p) :
  '''stringlist : LEFT_PARENTHESE stringnext RIGHT_PARENTHESE'''
  p[0] = p[2]

def p_stringnext_string(p) :
  '''stringnext : string'''
  p[0] = [p[1]]

def p_stringnext_stringnext(p) :
  '''stringnext : string COMA stringnext'''
  p[0] = [p[1]] + p[3]

def p_intop_plus_minus(p):
  '''intop : intop PLUS term
           | intop MINUS term'''
  p[0] = (p[2], infos(p), p[1] , p[3])

def p_intop_term(p):
  '''intop : term'''
  p[0] = p[1]

def p_term_times_divide(p):
  '''term : term TIMES factor
          | term DIVIDE factor'''
  p[0] = (p[2], infos(p), p[1], p[3] )

def p_term_factor(p):
  '''term : factor'''
  p[0] = p[1]

def p_factor_num(p):
  '''factor : INTEGER'''
  p[0] = p[1]

def p_factor_variable(p):
  '''factor : variable'''
  p[0] = p[1]

def p_variable(p) :
  '''variable : VARIABLE'''
  p[0] = ('variable', infos(p), p[1])

def p_error(p) :
  print('ERROR syntax', infos(p))


def parse_file(file_name) :
  lexer = lex.parse_file(file_name)
  return parser.parse(lexer=lexer)

def infos(p) :
  return lex.token_info(p.lexer)

def init() :
  'read command line arguments and init parser'
  debug = 0
  
  for arg in sys.argv :
    if arg == '-d' or arg == '--debug' :
      debug = 1
  
  # init parser with defined grammar in this file
  global parser
  parser = ply.yacc.yacc(debug=debug)

def main() :
  argc = len(sys.argv)
  if argc < 2 :
    exit('Usage: python3 {} file_to_parse'.format(sys.argv[0]))
  
  result = parse_file(sys.argv[1])
  if result != None :
    from pprint import pprint
    print('Output is :\n')
    pprint(result)


init()

if __name__ == "__main__" :
  main()
