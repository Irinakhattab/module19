#class Calculator:
#   def multiply(self, x, y):
#       return x * y
#
#  def division(self, x, y):
#       return x / y
#
#  def subtraction(self, x, y):
#      return x - y
#
#   def adding(self, x, y):
#       return x + y

    import pytest  

from calc import Calculator

class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_adding_succes(self):
        assert self.calc.adding(self, 1, 1) == 2

    def test_adding_unsucces(self):
        assert self.calc.adding(self, 1, 1) == 3

    def test_zero_division(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.division(self, 1, 0)

    def teardown(self):
        print('Выполнение метода Teardown')
