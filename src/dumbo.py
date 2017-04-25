from yacc import parser

def dumbo_exec(arg) :
  if is_array(arg) :
    for instr in arg :
      dumbo_exec(instr)
    return
  
  l = len(arg)
  if not is_tuple(arg) or l < 1:
    return error('Expecting tuple with minimum size 1, got {}'.format(arg))
  
  c = arg[0]
  if c == 'print' :
    print(str_val(arg[1]))
  elif c == 'assign' :
    set_var(arg[1], arg[2])
  elif c == 'for' :
    varname = arg[1]
    array = arg[2]
    if is_tuple(array) and array[0] == 'variable' :
      array = get_var(array[1])
    code = arg[3]
    
    oldval = get_var(varname)
    for value in array :
      set_var(varname, value)
      dumbo_exec(code)
    set_var(varname, oldval)
  else :
    print('Unknown command {}'.format(c))

def str_val(arg) :
  if arg[0] == 'string' :
    return arg[1]
  elif arg[0] == 'variable' :
    value = get_var(arg[1])
    if not is_string(value) :
      print('Variable {} is not a string'.format(arg[1]))
    return value
  elif arg[0] == 'concat' :
    return str_val(arg[1]) + str_val(arg[2])
  else :
    print('No string value for {}'.format(arg))
  
  

def set_var(name, value) :
  if value == None :
    return
  if is_array(value) :
    variables[name] = value
  else :
    variables[name] = str_val(value)
  #else :
    #print('Error assigning {} to {}'.format(value, name))
  

def get_var(name) :
  if name in variables :
    return variables[name]
  
  print('Error : no variable named {}'.format(name))
  return None

def error(message) :
  print(message)
  return None

def is_array(var) :
  return type([]) == type(var)

def is_tuple(var) :
  return type(()) == type(var)

def is_string(var) :
  return type('') == type(var)

def is_bool(var) :
  return type(True) == type(var)


if __name__ == "__main__" :
  import sys
  
  debug = 0
  for arg in sys.argv :
    if arg == '-d' or arg == '--debug' :
      debug = 1
  
  result = parser.parse(sys.stdin.read())
  
  if debug == 1 :
    from pprint import pprint
    print('Tree is :')
    pprint(result)
  
  
  variables = {}
  dumbo_exec(result)

