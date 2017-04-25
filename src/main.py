import sys

from yacc import parser
from dumbo import dumbo_exec

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
  
  program = data + template
  code = parser.parse(program)
  result = dumbo_exec(code)
  
  if file_put_contents(output_name, result) :
    print('Result saved successfully into {}'.format(output_name))
  else :
    print('output file {} not writable'.format(output_name))


def file_get_contents(filename) :
  try :
    f = open(filename, 'r')
  except OSError :
    return None
  contents = f.read()
  f.close()
  return contents

def file_put_contents(filename, contents) :
  try :
    f = open(filename, 'w')
  except OSError :
    return False
  f.write(contents)
  f.close()
  return True


if __name__ == "__main__" :
  main()
