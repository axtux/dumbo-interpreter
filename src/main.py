import sys

from yacc import parser
from dumbo import dumbo_exec
from files import *

def main() :
  argc = len(sys.argv)
  if argc < 4 :
    print('Usage: {} data template output')
    return
  
  data = file_get_contents(sys.argv[1])
  if data == None :
    print('data file {} not readable'.format(sys.argv[1]))
    return
  
  template = file_get_contents(sys.argv[2])
  if template == None :
    print('template file {} not readable'.format(sys.argv[2]))
    return
  
  output_name = sys.argv[3]
  if file_get_contents(output_name) != None :
    print('output file {} already exists')
    return
  
  data_code = parser.parse(data)
  template_code = parser.parse(template)
  
  # only save variables from data, not output
  result = dumbo_exec(data_code)
  result = dumbo_exec(template_code)
  
  if file_put_contents(output_name, result) :
    print('Result saved successfully into {}'.format(output_name))
  else :
    print('output file {} not writable'.format(output_name))

if __name__ == "__main__" :
  main()
