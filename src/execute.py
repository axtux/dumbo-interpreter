import inspect
import operator

from _is_ import *

def init() :
  """Store functions of this module into functions dictionary to later call functions from name.
  Also store the number of arguments accepted by each function into functions_args dictionary.
  Storing references avoid future lookups for functions and arguments length.
  """
  global variables, functions
  
  # initialize variables dictionary
  variables = {}
  
  # dynamically build functions dictionary storing all functions from this module
  '''
  functions = {
    name : (args_len, fct),
    ...
  }
  '''
  functions = {}
  for name, fct in globals().items() :
    if not callable(fct) :
      continue
    functions[name] = (args_len(fct), fct)
  
  # check operations dictionary for errors
  for name, desc in operations.items() :
    if not is_tuple(desc) :
      print('expected operation description to be a tuple, {} given'.format(desc))
    
    if len(desc) != 3 :
      print('expected 3 arguments per operation description, {} given for {}'.format(len(desc), name))
    
    (args_type, args_l, fct) = desc
    if not is_string(args_type) :
      print('expected args_type to be string, {} given for {}'.format(args_type, name))
    
    if not 'is_'+args_type in functions :
      print('unknown type {} for {}'.format(args_type, name))
    
    if not is_int(args_l) :
      print('expected args_len to be string, {} given for {}'.format(args_l, name))
    
    if args_l < 0 :
      print('expected args_len to be >= 0, {} given for {}'.format(args_l, name))
    
    if not callable(fct) :
      print('expected function to be callable, {} given for {}'.format(fct, name))

def reset() :
  '''
  reset variables for next instructions to be executed in clean environment
  '''
  global variables
  variables = {}

def args_len(fct) :
  """
  get the number of arguments from function signature
  """
  return len(inspect.signature(fct).parameters)


def execute(args) :
  """
  Executes dumbo instruction or instructions array and return output.
  Return None and stop execution if an error occurs. Details will be printed to standard output.
  """
  # execute each instruction in the array
  if is_array(args) :
    r = ''
    for instruction in args :
      re = execute(instruction)
      if re == None :
        return None
      r += re
    return r
  
  if not is_tuple(args) or len(args) < 1 :
    return error('instruction must be tuple with minimum size 1, got {}'.format(args))
  
  # dumbo function
  fct_name = 'dumbo_'+args[0]
  args = args[1:]
  
  if not fct_name in functions :
    return error('function {} is not defined'.format(fct_name))
  
  (args_len, fct) = functions[fct_name]
  if args_len != len(args) :
    return error('expected {} arguments for function {}, got {}'.format(args_len, fct_name, len(args)))
  
  return fct(*args)


"""
start dumbo functions
"""
def dumbo_print(var) :
  val = get_value(var)
  return None if val == None else str(val)

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
    return error('for argument 2 must be array, got {}'.format(array))
  
  oldval = get_var(varname)
  r = ''
  for value in array :
    set_var(varname, value)
    re = execute(code)
    if re == None :
      return None
    r += re
  
  if oldval != None :
    set_var(varname, oldval)
  
  return r

def dumbo_if(condition, code) :
  condition = get_value(condition)
  if not is_bool(condition) :
    return error('if argument 1 must be boolean, got {}'.format(condition))
  
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
  if not is_tuple(args) or len(args) < 1 :
    return args
  
  op = args[0]
  args = args[1:]
  
  if not op in operations :
    return print('unknown operation {}'.format(op))
  
  (args_type, args_len, fct) = operations[op]
  if args_len != len(args) :
    return print('operation {} expected {} arguments, {} given'.format(op, args_len, len(args)))
  
  # recursively get value on operation arguments
  args = tuple(map(get_value, args))
  
  (_, check) = functions['is_'+args_type]
  if not all(map(check, args)) :
    return print('operation {} expected arguments of type {}, got {}'.format(op, args_type, args))
  
  return fct(*args)


"""
start operations
"""
def operation_variable(name) :
  if not is_var(name) :
    return error('undefined variable {}'.format(name))
  return get_var(name)

def operation_division(var1, var2) :
    if var2 == 0 :
      return error('trying to divide {} by 0'.format(var1))
    return operator.floordiv(var1, var2)

# 'op_name' : ('args_type', args_len', function)
operations = {
  'variable' : ('string', 1, operation_variable),
  # string
  '.' : ('string', 2, operator.concat),
  # int
  '+'  : ('int', 2, operator.add),
  '-'  : ('int', 2, operator.sub),
  '*'  : ('int', 2, operator.mul),
  '/'  : ('int', 2, operation_division),
  '<'  : ('int', 2, operator.lt),
  '>'  : ('int', 2, operator.gt),
  '='  : ('int', 2, operator.eq),
  '!=' : ('int', 2, operator.ne),
  # bool
  'and' : ('bool', 2, lambda a, b : a and b),
  'or'  : ('bool', 2, lambda a, b : a or b),
}

"""
end operations
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


def main() :
  import sys
  from yacc import parse_file
  
  argc = len(sys.argv)
  if argc < 2 :
    exit('Usage: python3 {} file_to_parse'.format(sys.argv[0]))
  
  code = parse_file(sys.argv[1])
  if code == None :
    return
  
  r = execute(code)
  if r == None :
    return print('error executing file {}'.format(sys.argv[1]))
  
  print('Execution result :\n{}'.format(r))

"""
Initialize variable and function dictionaries, check operations dictionary
"""
init()

if __name__ == "__main__" :
  main()

