variables = {}

def dumbo_exec(arg) :
  if is_array(arg) :
    r = ''
    for instr in arg :
      r += dumbo_exec(instr)
    return r
  
  l = len(arg)
  if not is_tuple(arg) or l < 1:
    error('Expecting tuple with minimum size 1, got {}'.format(arg))
    return ''
  
  # dumbo command
  c = arg[0]
  
  if c == 'print' :
    if not arg_check(c, l-1, 1) :
      return ''
    
    return dumbo_print(arg[1])
  
  
  if c == 'assign' :
    if not arg_check(c, l-1, 2) :
      return ''
    
    return dumbo_assign(arg[1], arg[2])
  
  
  if c == 'for' :
    if not arg_check(c, l-1, 3) :
      return ''
    
    return dumbo_for(arg[1], arg[2], arg[3])
  
  
  print('Unknown command {}'.format(c))
  return ''


def dumbo_print(var) :
  return str_val(var)

def dumbo_assign(name, value) :
  if is_var(name) :
    warning('reassigning already assigned variable {}'.format(name))
  
  set_var(name, value)
  return ''

def dumbo_for(varname, array, code) :
  if is_tuple(array) and array[0] == 'variable' :
    array = get_var(array[1])
    if array == None :
      error('undefined variable {}'.format(array[1]))
      return ''
    if not is_array(array) :
      error('for expecting argument 2 to be array, got {}'.format(array))
      return ''
  
  oldval = get_var(varname)
  r = ''
  
  for value in array :
    set_var(varname, value)
    r += dumbo_exec(code)
  
  set_var(varname, oldval)
  return r


def str_val(arg) :
  if arg[0] == 'string' :
    return arg[1]
  elif arg[0] == 'variable' :
    value = get_var(arg[1])
    if not is_string(value) :
      print('Variable {} is not a string'.format(arg[1]))
      return ''
    return value
  elif arg[0] == 'concat' :
    return str_val(arg[1]) + str_val(arg[2])
  else :
    print('No string value for {}'.format(arg))
    return ''

def set_var(name, value) :
  if value == None :
    return
  
  if is_array(value) :
    variables[name] = value
  else :
    variables[name] = str_val(value)
  #else :
    #print('Error assigning {} to {}'.format(value, name))


def is_var(name) :
  return name in variables

def get_var(name) :
  if is_var(name) :
    return variables[name]
  
  return None


def arg_check(command, arg_len, expected_len) :
  if arg_len == expected_len :
    return True
  
  error('Expecting {} arguments for command "{}", {} given'.format(l))
  return False

def warning(message) :
  print('WARNING:', message)

def error(message) :
  print('ERROR:', message)

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
  
  from yacc import parser
  code = parser.parse(sys.stdin.read())
  
  if debug == 1 :
    from pprint import pprint
    print('Code is :')
    pprint(code)
  
  result = dumbo_exec(code)
  print(result)

