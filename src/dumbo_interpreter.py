import sys
import file

from yacc import parser
from execute import execute

def main() :
  argc = len(sys.argv)
  if argc < 4 :
    return print('Usage: python3 {} data template output'.format(sys.argv[0]))
  
  data = file.get_contents(sys.argv[1])
  if data == None :
    return print('data file "{}" not readable'.format(sys.argv[1]))
  
  template = file.get_contents(sys.argv[2])
  if template == None :
    return print('template file "{}" not readable'.format(sys.argv[2]))
  
  output_name = sys.argv[3]
  if file.get_contents(output_name) != None :
    return print('output file "{}" already exists'.format(output_name))
  
  data_code = parser.parse(data)
  template_code = parser.parse(template)
  
  # only save variables from data, not output
  result = execute(data_code)
  result = execute(template_code)
  
  if file.put_contents(output_name, result) :
    print('saved output to file "{}"'.format(output_name))
  else :
    print('output file "{}" not writable'.format(output_name))

if __name__ == "__main__" :
  main()
