
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
