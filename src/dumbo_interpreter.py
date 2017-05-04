import sys

from yacc import parser
from execute import execute
from files import *

def main() :
  argc = len(sys.argv)
  if argc < 4 :
    return print('Usage: python3 {} data template output'.format(sys.argv[0]))
  
  data = file_get_contents(sys.argv[1])
  if data == None :
    return print('data file "{}" not readable'.format(sys.argv[1]))
  
  template = file_get_contents(sys.argv[2])
  if template == None :
    return print('template file "{}" not readable'.format(sys.argv[2]))
  
  output_name = sys.argv[3]
  if file_get_contents(output_name) != None :
    return print('output file "{}" already exists'.format(output_name))
  
  data_code = parser.parse(data)
  template_code = parser.parse(template)
  
  # only save variables from data, not output
  result = execute(data_code)
  result = execute(template_code)
  
  if file_put_contents(output_name, result) :
    print('Result saved successfully into {}'.format(output_name))
  else :
    print('output file {} not writable'.format(output_name))

if __name__ == "__main__" :
  main()
