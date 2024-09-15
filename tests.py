import unittest
from io import StringIO
from unittest.mock import patch

from Interpreter import *


class TestBefungeInterpreter(unittest.TestCase):
    @patch('sys.stdin', new_callable=lambda: StringIO('@\nQ'))
    def setUp(self, mock_stdin):
        self.inter = Interpreter('mycode')

    @patch('sys.stdin', create=True)
    def test_write_input(self, mock_stdin):
        first_code = ['>987v>.v\n', 'v456<  :\n',
                      '2v   ,&<\n', '1>:&:v\n',
                      ' ^   _@ \n', 'Q\n']

        mock_stdin.readline.side_effect = first_code
        self.inter_input = Interpreter('mycode')
        for line in first_code[:-1]:
            self.assertIn(line, self.inter_input.code)

    def test_write_file(self):
        self.inter_file = Interpreter('./exmpls/hw2.bf')
        result = ['>25*"!dlrow ,olleH":v\n',
                  '                 v:,_@\n',
                  '                 >  ^']

        self.assertEqual(self.inter_file.code, result)

    def test_step(self):
        self.assertEqual(self.inter.x, 0)
        self.assertEqual(self.inter.y, 0)

        self.inter.code = [[1, 2], [1, 2]]
        self.inter.step()
        self.assertEqual(self.inter.x, 1)
        self.assertEqual(self.inter.y, 0)

        self.inter.vector = 3
        self.inter.step()
        self.assertEqual(self.inter.x, 1)
        self.assertEqual(self.inter.y, 1)

        self.inter.vector = 4
        self.inter.step()
        self.assertEqual(self.inter.x, 0)
        self.assertEqual(self.inter.y, 1)

        self.inter.vector = 1
        self.inter.step()
        self.assertEqual(self.inter.x, 0)
        self.assertEqual(self.inter.y, 0)

    def test_op_value(self):
        self.inter.stack = [1, 2]
        self.inter.op_value('+')
        self.assertEqual(self.inter.pop(), 3)

        self.inter.stack = [1, 2]
        self.inter.op_value('-')
        self.assertEqual(self.inter.pop(), 1)

        self.inter.stack = [1, 2]
        self.inter.op_value('*')
        self.assertEqual(self.inter.pop(), 2)

        self.inter.stack = [1, 2]
        self.inter.op_value('/')
        self.assertEqual(self.inter.pop(), 2)

        self.inter.stack = [0, 2]
        self.inter.op_value('/')
        self.assertEqual(self.inter.pop(), 0)

        self.inter.stack = [2, 0]
        self.inter.op_value('/')
        self.assertEqual(self.inter.pop(), 0)

        self.inter.stack = [1, 2]
        self.inter.op_value('%')
        self.assertEqual(self.inter.pop(), 0)

    def test_sf(self):
        self.inter.x = 0
        self.inter.y = 0
        self.inter.stack = []
        self.inter.code = ['"hj" @']
        self.inter.execute()
        self.assertEqual(self.inter.stack_sf, 0)

        self.inter.x = 0
        self.inter.y = 0
        self.inter.code = ['"@']
        self.inter.execute()
        self.assertEqual(self.inter.stack_sf, 1)

    def test_pop(self):
        self.assertEqual(self.inter.pop(), 0)
        self.inter.stack.append(4)
        self.inter.stack.append(3)
        self.inter.stack.append(2)
        self.inter.stack.append(1)
        self.inter.stack.append(0)

        self.assertEqual(self.inter.pop(), 0)
        self.assertEqual(self.inter.pop(), 1)
        self.assertEqual(self.inter.pop(), 2)
        self.assertEqual(self.inter.pop(), 3)
        self.assertEqual(self.inter.pop(), 4)
        self.assertEqual(self.inter.pop(), 0)

    def test_change_vector(self):
        self.inter.ar_value('^')
        self.assertEqual(self.inter.vector, 1)
        self.inter.ar_value('>')
        self.assertEqual(self.inter.vector, 2)
        self.inter.ar_value('v')
        self.assertEqual(self.inter.vector, 3)
        self.inter.ar_value('<')
        self.assertEqual(self.inter.vector, 4)

    def test_execl(self):
        self.inter.stack = [1]

        self.inter.excl()
        self.assertEqual(self.inter.stack[0], 0)

        self.inter.excl()
        self.assertEqual(self.inter.stack[0], 1)

    def test_apostr(self):
        self.inter.stack = [1, 2]
        self.inter.apostr()
        self.assertEqual(self.inter.pop(), 0)

        self.inter.stack = [2, 1]
        self.inter.apostr()
        self.assertEqual(self.inter.pop(), 1)

    def test_colon(self):
        self.inter.stack = [1]
        self.inter.colon()
        self.assertEqual(self.inter.pop(), 1)
        self.assertEqual(self.inter.pop(), 1)

    def test_slash(self):
        self.inter.stack = [1, 2]
        self.inter.slash()
        self.assertEqual(self.inter.pop(), 1)
        self.assertEqual(self.inter.pop(), 2)

    def test_underline(self):
        self.inter.stack = []
        self.inter.underline()
        self.assertEqual(self.inter.vector, 2)

        self.inter.stack = [2]
        self.inter.underline()
        self.assertEqual(self.inter.vector, 4)

    def test_forward(self):
        self.inter.stack = []
        self.inter.forward()
        self.assertEqual(self.inter.vector, 3)

        self.inter.stack = [2]
        self.inter.forward()
        self.assertEqual(self.inter.vector, 1)

    @patch('builtins.input', side_effect=['a'])
    def test_squiggle(self, mock_input):
        self.inter.stack = []
        self.inter.squiggle()
        self.assertEqual(self.inter.pop(), ord('a'))

    @patch('builtins.input', side_effect=[4])
    def test_ampersand(self, mock_input):
        self.inter.stack = []
        self.inter.ampersand()
        self.assertEqual(self.inter.pop(), 4)

    def test_hex(self):
        self.inter.stack = []
        self.inter.hex('a')
        self.assertEqual(self.inter.pop(), 10)
        self.inter.hex('b')
        self.assertEqual(self.inter.pop(), 11)
        self.inter.hex('c')
        self.assertEqual(self.inter.pop(), 12)
        self.inter.hex('d')
        self.assertEqual(self.inter.pop(), 13)
        self.inter.hex('e')
        self.assertEqual(self.inter.pop(), 14)
        self.inter.hex('f')
        self.assertEqual(self.inter.pop(), 15)
