import inspect
import operator

from _is_ import *

def init() :
  """Store functions of this module into functions dictionary to later call functions from name.
  Also store the number of arguments accepted by each function into functions_args dictionary.
  Storing references avoid future lookups for functions and arguments length.
  """
  reset()
  
  # dynamically build functions dictionary storing all functions from this module
  '''
  functions = {
    name : (args_len, fct),
    ...
  }
  '''
  global functions
  functions = {}
  for name, fct in globals().items() :
    if not callable(fct) :
      continue
    functions[name] = (args_len(fct), fct)
  
  # check operations dictionary for errors
  for name, desc in operations.items() :
    if not is_tuple(desc) :
      unexpected_exit('operation description to be a tuple', desc, name)
    
    if len(desc) != 4 :
      unexpected_exit('4 arguments per operation description', len(desc), name)
    
    (args_type, args_l, fct, infos) = desc
    if not is_string(args_type) :
      unexpected_exit('args_type to be string', args_type, name)
    
    if not 'is_'+args_type in functions :
      unexpected_exit('args_type to be type from _is_ module', args_type, name)
    
    if not is_int(args_l) :
      unexpected_exit('args_len to be int', args_l, name)
    
    if args_l < 0 :
      unexpected_exit('args_len to be >= 0', args_l, name)
    
    if not callable(fct) :
      unexpected_exit('function to be callable', fct, name)
    
    if not is_bool(infos) :
      unexpected_exit('incl_infos to be boolean', infos, name)

def unexpected_exit(expected, given, name):
  exit('expected {}, {} given for {}'.format(expected, given, name))

def reset() :
  """reset variables for next instructions to be executed in clean environment"""
  global variables
  variables = {}

def args_len(fct) :
  """get the number of arguments from function signature"""
  return len(inspect.signature(fct).parameters)



def execute(args) :
  """
  Executes dumbo instruction or instructions array and return output.
  Return None and stop execution if an error occurs. Details will be printed to standard output.
  
  Supported functions :
    ('print', infos, variable_or_value)
    ('assign', infos, variable_name, variable_value)
    ('for', infos, variable_name_in_instructions, variable_array_or_array, instructions_list)
    ('if', infos, bool_condition_or_comparison, insturctions_list)
    
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
def dumbo_print(infos, var) :
  val = get_value(var)
  if is_bool(val) : return str(val).lower()
  return None if val == None else str(val)

def dumbo_assign(infos, name, value) :
  if is_var(name) :
    warning('{} reassigning already assigned variable {}'.format(infos, name))
  value = get_value(value)
  if not value == None :
    set_var(name, value)
  return ''

def dumbo_for(infos, varname, array, code) :
  array = get_value(array)
  if not is_array(array) :
    return error('{} for argument 2 must be array, got {}'.format(infos, array))
  
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

def dumbo_if(infos, condition, code) :
  condition = get_value(condition)
  if not is_bool(condition) :
    return error('{} if argument 1 must be boolean, got {}'.format(infos, condition))
  
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
  if not is_tuple(args) or len(args) < 2 :
    return args
  
  op = args[0]
  infos = args[1]
  args = args[2:]
  
  if not op in operations :
    return error('{} unknown operation {}'.format(infos, op))
  
  (args_type, args_len, fct, incl_infos) = operations[op]
  if args_len != len(args) :
    return error('{} operation {} expected {} arguments, {} given'.format(infos, op, args_len, len(args)))
  
  # recursively get value on operation arguments
  args = tuple(map(get_value, args))
  
  (_, check) = functions['is_'+args_type]
  if not all(map(check, args)) :
    return error('{} operation {} expected arguments of type {}, got {}'.format(infos, op, args_type, args))
  
  if incl_infos :
    args = (infos,) + args
  
  return fct(*args)


"""
start operations
"""
def operation_variable(infos, name) :
  if not is_var(name) :
    return error('{} undefined variable {}'.format(infos, name))
  return get_var(name)

def operation_division(infos, var1, var2) :
    if var2 == 0 :
      return error('{} division by 0'.format(infos))
    return operator.floordiv(var1, var2)

# 'op_name' : ('args_type', args_len, function, incl_infos)
operations = {
  'variable' : ('string', 1, operation_variable, True),
  # string
  '.' : ('string', 2, operator.concat, False),
  # int
  '+'  : ('int', 2, operator.add, False),
  '-'  : ('int', 2, operator.sub, False),
  '*'  : ('int', 2, operator.mul, False),
  '/'  : ('int', 2, operation_division, True),
  '<'  : ('int', 2, operator.lt, False),
  '>'  : ('int', 2, operator.gt, False),
  '='  : ('int', 2, operator.eq, False),
  '!=' : ('int', 2, operator.ne, False),
  # bool
  'and' : ('bool', 2, lambda a, b : a and b, False),
  'or'  : ('bool', 2, lambda a, b : a or b, False),
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
  import yacc
  
  argc = len(sys.argv)
  if argc < 2 :
    exit('Usage: python3 {} file_to_parse'.format(sys.argv[0]))
  
  code = yacc.parse_file(sys.argv[1])
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

