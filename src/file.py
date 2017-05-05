"""Easy interface to manage text files."""

def get_contents(filename) :
  """Read whole file into a string.
  
  Parameters
  ----------
  filename : string
    String filename absolute or relative to current working directory.
  
  Returns
  -------
  string
    file contents on success
  None
    None if file is not readable
  """
  try :
    f = open(filename, 'r')
  except OSError :
    return None
  contents = f.read()
  f.close()
  return contents

def put_contents(filename, contents) :
  """
  write contents string into file
  return True on success, False on error
  """
  try :
    f = open(filename, 'w')
  except OSError :
    return False
  f.write(contents)
  f.close()
  return True
