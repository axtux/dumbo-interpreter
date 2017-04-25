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
  
  
  error('unknown command {}'.format(c))
  return ''


def dumbo_print(var) :
  val get_value(var)
  if val == None :
    return ''
  return val

def dumbo_assign(name, value) :
  if is_var(name) :
    warning('reassigning already assigned variable {}'.format(name))
  value = get_value(value)
  if not value == None :
    set_var(name, value)
  return ''

def dumbo_for(varname, array, code) :
  array = get_value(array)
  if not is_array(array) :
    error('for argument 2 must be array, got {}'.format(array))
    return ''
  
  oldval = get_var(varname)
  r = ''
  
  for value in array :
    set_var(varname, value)
    r += dumbo_exec(code)
  
  if oldval != None :
    set_var(varname, oldval)
  return r


def set_var(name, value) :
  variables[name] = value

def is_var(name) :
  return name in variables

def get_var(name) :
  if is_var(name) :
    return variables[name]
  return None

def get_value(var) :
  if is_tuple(var) :
    l = len(var)
    if l == 2 and var[0] == 'variable' :
      if not is_var(var[1]) :
        return error('undefined variable {}'.format(array[1]))
      return get_var(var[1])
    if l == 3 and var[0] == 'concat' :
      p1 = get_value(var[1])
      p2 = get_value(var[2])
      if not is_string(p1) or not is_string(p2) :
        return error('concat arguments must be string, got {} and {}'.format(p1, p2))
      return p1 + p2
    if l == 2 and var[0] == '+' :
      p1 = get_value(var[1])
      p2 = get_value(var[2])
      if not is_int(p1) or not is_int(p2) :
        return error('concat arguments must be string, got {} and {}'.format(p1, p2))
    
    return error('value should not be unidentified tuple {}'.format(var))
  
  # no tuple, return raw value
  return var
    
  

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

def is_int(var) :
  return type(0) == type(var)

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

