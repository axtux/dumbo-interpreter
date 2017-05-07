import sys
import file

from yacc import parse_file
from execute import execute

def main() :
  argc = len(sys.argv)
  if argc < 4 :
    return print('Usage: python3 {} data template output'.format(sys.argv[0]))
  
  data_name = sys.argv[1]
  template_name = sys.argv[2]
  
  output_name = sys.argv[3]
  if file.get_contents(output_name) != None :
    return print('output file "{}" already exists'.format(output_name))
  
  data_code = parse_file(data_name)
  if data_code == None :
    return
  template_code = parse_file(template_name)
  if template_code == None :
    return
  
  # save variables from data and template, output from template
  result = execute(data_code)
  if result == None :
    return print('execution error into data file "{}"'.format(sys.argv[1]))
  result = execute(template_code)
  if result == None :
    return print('execution error into template file "{}"'.format(sys.argv[2]))
  
  if file.put_contents(output_name, result) :
    print('saved output to file "{}"'.format(output_name))
  else :
    print('output file "{}" not writable'.format(output_name))

if __name__ == "__main__" :
  main()
