
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
