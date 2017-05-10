import sys
import ply.yacc
import lex
from lex import tokens

"""
    Grammar definition
"""

def p_program_program_subprogram(p) :
  '''program : program subprogram'''
  p[0] = p[1] + p[2]

def p_program_subprogram(p) :
  '''program : subprogram'''
  p[0] = p[1]


def p_subprogram_text(p) :
  '''subprogram : TEXT'''
  p[0] = [('print', infos(p), p[1])]

def p_subprogram_codeblock(p) :
  '''subprogram : CODESTART codeblock CODEEND'''
  p[0] = p[2]

def p_subprogram_empty(p) :
  '''subprogram : CODESTART CODEEND'''
  p[0] = []


def p_codeblock_codeblock_codeline(p) :
  '''codeblock : codeblock codeline'''
  p[0] = p[1] + [p[2]]

def p_codeblock_codeline(p) :
  '''codeblock : codeline'''
  p[0] = [p[1]]

def p_codeline_instruction(p) :
  '''codeline : instruction SEMICOLON'''
  p[0] = p[1]


def p_instruction_print(p) :
  '''instruction : PRINT value'''
  p[0] = ('print', infos(p), p[2])

def p_instruction_assign(p) :
  '''instruction : VARIABLE ASSIGNATION value'''
  p[0] = ('assign', infos(p), p[1], p[3])

def p_instruction_for(p) :
  '''instruction : FOR VARIABLE IN variable DO codeblock ENDFOR
                 | FOR VARIABLE IN stringlist DO codeblock ENDFOR'''
  p[0] = ('for', infos(p), p[2], p[4], p[6])

def p_instruction_if(p) :
  '''instruction : IF boolop DO codeblock ENDIF'''
  p[0] = ('if', infos(p), p[2], p[4])


def p_value(p) :
  '''value : variable
           | boolop
           | intop
           | stringop
           | stringlist'''
  # value -> variable is already included in boolop, intop and stringop
  # but this is a shortcut that makes things clear
  p[0] = p[1]

def p_variable(p) :
  '''variable : VARIABLE'''
  p[0] = ('variable', infos(p), p[1])


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

def p_bool_variable(p) :
  '''bool : variable'''
  p[0] = p[1]

def p_bool_comparison(p) :
  '''bool : intop COMPARATOR intop'''
  p[0] = (p[2], infos(p), p[1], p[3])


def p_stringop_string_stringop(p) :
  '''stringop : string CONCATENATION stringop'''
  p[0] = (p[2], infos(p), p[1], p[3])

def p_stringop_string(p) :
  '''stringop : string'''
  p[0] = p[1]

def p_string_string(p) :
  '''string : STRING'''
  p[0] = p[1]

def p_string_variable(p) :
  '''string : variable'''
  p[0] = p[1]


def p_stringlist_stringseq(p) :
  '''stringlist : LEFT_PARENTHESE stringseq RIGHT_PARENTHESE'''
  p[0] = p[2]

def p_stringlist_empty(p) :
  '''stringlist : LEFT_PARENTHESE RIGHT_PARENTHESE'''
  p[0] = []

def p_stringseq_string_stringseq(p) :
  '''stringseq : string COMA stringseq'''
  p[0] = [p[1]] + p[3]

def p_stringseq_string(p) :
  '''stringseq : string'''
  p[0] = [p[1]]


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

def p_factor_integer(p):
  '''factor : INTEGER'''
  p[0] = p[1]

def p_factor_variable(p):
  '''factor : variable'''
  p[0] = p[1]


def p_error(p) :
  print('ERROR syntax', infos(p))

def infos(p) :
  return lex.token_info(p.lexer)


def parse_file(file_name) :
  lexer = lex.parse_file(file_name)
  if lexer == None : return
  return parser.parse(lexer=lexer)

def init() :
  'init parser with defined grammar in this file'
  global parser
  parser = ply.yacc.yacc(debug=lex.debug)

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
