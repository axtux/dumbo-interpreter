import unittest
import sys

sys.path.append('..')
from yacc import parser
from execute import reset, execute

class DumboTests(unittest.TestCase):
  def input_expect(self, input, expected_output):
    code = parser.parse(input)
    reset()
    actual_output = execute(code)
    self.assertEqual(expected_output, actual_output, 'intput : "{}"'.format(input))
  
  """subprogram test"""
  def test_text(self):
    self.input_expect("text_only", "text_only")
  
  def test_text_code(self):
    self.input_expect("t1{{ print 'c1';}}t2{{ print 'c2';}}", "t1c1t2c2")
  
  
  """boolop tests"""
  def test_print_boolop_and(self):
    self.input_expect("{{ print true and true; }}", "true")
    self.input_expect("{{ print false and true; }}", "false")
    self.input_expect("{{ print true and false; }}", "false")
    self.input_expect("{{ print false and false; }}", "false")
  
  def test_print_boolop_or(self):
    self.input_expect("{{ print true or true; }}", "true")
    self.input_expect("{{ print false or true; }}", "true")
    self.input_expect("{{ print true or false; }}", "true")
    self.input_expect("{{ print false or false; }}", "false")
  
  def test_print_boolop_and_or(self):
    self.input_expect("{{ print false and true or true; }}", "true")
    self.input_expect("{{ print true or true and false; }}", "false")
  
  def test_print_comparison_lt(self):
    self.input_expect("{{ print 1 < 2; }}", "true")
    self.input_expect("{{ print 2 < 1; }}", "false")
  
  def test_print_comparison_gt(self):
    self.input_expect("{{ print 1 > 2; }}", "false")
    self.input_expect("{{ print 2 > 1; }}", "true")
  
  def test_print_comparison_eq(self):
    self.input_expect("{{ print 1 = 1; }}", "true")
    self.input_expect("{{ print 1 = 2; }}", "false")
  
  def test_print_comparison_ne(self):
    self.input_expect("{{ print 1 != 1; }}", "false")
    self.input_expect("{{ print 1 != 2; }}", "true")
  
  """stringop tests"""
  def test_print_stringop(self):
    self.input_expect("{{ print 's1'.'s2'; }}", "s1s2")
  
  def test_print_stringop_multi(self):
    self.input_expect("{{ print 's1'.'s2'.'s3'.'s4'; }}", "s1s2s3s4")
  
  
  """intop tests"""
  def test_print_intop_plus(self):
    self.input_expect("{{ print 1+2; }}", "3")
  
  def test_print_intop_minus(self):
    self.input_expect("{{ print 1-2; }}", "-1")
  
  def test_print_intop_times(self):
    self.input_expect("{{ print 2*2; }}", "4")
  
  def test_print_intop_divide(self):
    self.input_expect("{{ print 4/2; }}", "2")
  
  def test_print_intop_divide_floor(self):
    self.input_expect("{{ print 101/100; }}", "1")
    self.input_expect("{{ print 199/100; }}", "1")
  
  def test_print_intop_precedence(self):
    self.input_expect("{{ print 2*3+4*5; }}", "26")
    self.input_expect("{{ print 2+3*4+5; }}", "19")
  
  
  """variable assignation"""
  def test_print_variable_bool(self):
    self.input_expect("{{ var := true; print var; }}", "true")
    self.input_expect("{{ var := false; print var; }}", "false")
  
  def test_print_variable_int(self):
    self.input_expect("{{ var := 1; print var; }}", "1")
    self.input_expect("{{ var := 2+3; print var+4; }}", "9")
  
  def test_print_variable_string(self):
    self.input_expect("{{ var := 's1'; print var; }}", "s1")
    self.input_expect("{{ var := 's1'.'s2'; print var.'s3'; }}", "s1s2s3")
  


if __name__ == '__main__':
  unittest.main()
