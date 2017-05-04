import inspect

variables = {}

def execute(args) :
  """
  Executes dumbo instruction or serie of instructions and return output.
  """
  # exec each instruction in the array
  if is_array(args) :
    r = ''
    for instruction in args :
      r += execute(instruction)
    return r
  
  if not is_tuple(args) or len(args) < 1 :
    error('Expecting tuple with minimum size 1, got {}'.format(args))
    return ''
  
  # dumbo function
  r = call_function('dumbo_'+args[0], args[1:])
  return '' if r == None else r


def call_function(name, args) :
  """
  call function from function name and arguments tuple
  """
  # get module namespace
  g = globals()
  if not name in g :
    return error('function {} is not defined'.format(name))
  
  fct = g[name]
  if not callable(fct) :
    return error('{} is not a callable'.format(fct))
  
  if args == None :
    args = ()
  
  if not is_tuple(args) :
    return error('args must be a tuple, got {}'.format(args))
  
  if len(args) != args_len(fct) :
    return error('expected {} arguments, got {}'.format(args_len(fct), len(args)))
  
  return fct(*args)

def args_len(fct) :
  return len(inspect.signature(fct).parameters)

def dumbo_print(var) :
  val = get_value(var)
  if is_string(val) or is_bool(val) or is_int(val) :
    return str(val)
  return ''

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
    r += execute(code)
  
  if oldval != None :
    set_var(varname, oldval)
  return r

def dumbo_if(condition, code) :
  condition = get_value(condition)
  if not is_bool(condition) :
    error('is argument 1 must be boolean, got {}'.format(array))
    return ''
  
  if condition :
    return execute(code)
  
  return ''


def set_var(name, value) :
  variables[name] = value

def is_var(name) :
  return name in variables

def get_var(name) :
  if is_var(name) :
    return variables[name]
  return None

def get_value(var) :
  if not is_tuple(var) or len(var) < 1 :
    # no tuple, return raw value
    return var
  
  l = len(var)
  c = var[0]
  
  if c == 'variable' :
    if not arg_check(c, l-1, 1) :
      return None
    if not is_var(var[1]) :
      return error('undefined variable {}'.format(array[1]))
    return get_var(var[1])
  
  if c == 'concat' :
    if not arg_check(c, l-1, 2) :
      return None
    return dumbo_concat(var[1], var[2])
  
  if c == 'arithmetic' :
    if not arg_check(c, l-1, 3) :
      return None
    return dumbo_arithmetic(var[1], var[2], var[3])
  
  if c == 'boolean' :
    if not arg_check(c, l-1, 3) :
      return None
    return dumbo_bool(var[1], var[2], var[3])
  
  if c == 'comparison' :
    if not arg_check(c, l-1, 3) :
      return None
    return dumbo_compare(var[1], var[2], var[3])
  
  return error('value should not be unidentified tuple {}'.format(var))

def dumbo_concat(var1, var2) :
  var1 = get_value(var1)
  var2 = get_value(var2)
  
  if not is_string(var1) or not is_string(var2) :
    return error('concat arguments must be string, got {} and {}'.format(var1, var2))
  
  return var1 + var2

def dumbo_arithmetic(op, var1, var2) :
    var1 = get_value(var1)
    var2 = get_value(var2)
    
    if not is_int(var1) or not is_int(var2) :
      return error('arithmetic {} arguments must be integers, got {} and {}'.format(op, var1, var2))
    
    if op == '+' :
      return var1 + var2
    if op == '-' :
      return var1 - var2
    if op == '*' :
      return int(var1 * var2)
    if op == '/' :
      if var2 == 0 :
        return error('trying to divide {} by 0'.format(var1))
      return int(var1 / var2)
    return error('unknown arithmetic operation {}'.format(op))

def dumbo_bool(op, var1, var2) :
    var1 = get_value(var1)
    var2 = get_value(var2)
    
    if not is_bool(var1) or not is_bool(var2) :
      return error('boolean {} arguments must be booleans, got {} and {}'.format(op, var1, var2))
    
    if op == 'and' :
      return var1 and var2
    if op == 'or' :
      return var1 or var2
    return error('unknown boolean operation {}'.format(op))

def dumbo_compare(op, var1, var2) :
    var1 = get_value(var1)
    var2 = get_value(var2)
    
    if not is_int(var1) or not is_int(var2) :
      return error('compare {} arguments must be integers, got {} and {}'.format(op, var1, var2))
    
    if op == '<' :
      return var1 < var2
    if op == '>' :
      return var1 > var2
    if op == '=' :
      return var1 == var2
    if op == '!=' :
      return var1 != var2
    return error('unknown comparison operation {}'.format(op))


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
  
  result = execute(code)
  print(result)

