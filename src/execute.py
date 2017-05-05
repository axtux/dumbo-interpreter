import inspect

from _is_ import *

variables = {}

# TODO init functions not to call globals, callable and args_len on each function

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
  """
  get the number of arguments possible for function fct
  """
  return len(inspect.signature(fct).parameters)


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


"""
start dumbo functions
"""
def dumbo_print(var) :
  val = get_value(var)
  return str(val)

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
    error('if argument 1 must be boolean, got {}'.format(condition))
    return ''
  
  if condition :
    return execute(code)
  
  return ''
"""
end dumbo functions
"""

def get_value(args) :
  """
  get value from value function if args is a tuple else return args
  """
  if is_tuple(args) and len(args) > 0 :
    return call_function('value_'+args[0], args[1:])
  
  return args

"""
start value functions
"""
def value_variable(name) :
  if not is_var(name) :
    return error('undefined variable {}'.format(name))
  return get_var(name)

def value_concat(var1, var2) :
  var1 = get_value(var1)
  var2 = get_value(var2)
  
  if not is_string(var1) or not is_string(var2) :
    return error('concat arguments must be string, got {} and {}'.format(var1, var2))
  
  return var1 + var2

def value_arithmetic(op, var1, var2) :
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

def value_boolean(op, var1, var2) :
    var1 = get_value(var1)
    var2 = get_value(var2)
    
    if not is_bool(var1) or not is_bool(var2) :
      return error('boolean {} arguments must be booleans, got {} and {}'.format(op, var1, var2))
    
    if op == 'and' :
      return var1 and var2
    if op == 'or' :
      return var1 or var2
    return error('unknown boolean operation {}'.format(op))

def value_comparison(op, var1, var2) :
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
"""
and value functions
"""

def set_var(name, value) :
  variables[name] = value

def is_var(name) :
  return name in variables

def get_var(name) :
  if is_var(name) :
    return variables[name]
  return None

def warning(message) :
  print('WARNING:', message)

def error(message) :
  print('ERROR:', message)


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

