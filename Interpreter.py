import random
import sys
from registr import *


class Interpreter:
    """
    Класс Interpreter используется
    для исполнение Befunge файлов

    x -> Номер символа в строке
    y -> Номер строки
    vector -> Направление движения указателя
    stack -> Список, эмулирующий работ стэка Befunge
    code -> Список строк кода на этом языке
    stack_sf -> Флаг, указыващий режим 'запись строки'/'выполнение операторов'
    operators -> Список для оптимизации выброра операторов
    """
    x = 0
    y = 0
    vector = 2
    stack = []
    code = []
    stack_sf = 0
    operators = ['+', '-', '*', '/', '%']
    arrows = ['<', '>', '^', 'v']

    def __init__(self, filename: str):
        """
        Конструктор класса, записывающий
        двумерное поле исполняемое файла
        в виде списка строк

        :param filename: Имя исполняемого файла
        """
        if filename != 'mycode':
            with open(filename, 'r') as f:
                self.code = f.readlines()
        else:
            stop_char = 'Q'
            while True:
                line = sys.stdin.readline()
                if line[0] == stop_char:
                    break
                self.code.append(line)

        self.execute()

    def step(self):
        """
        Функция 'шага':
        Переключает символ в зависимостиэ
        от направление (переменная vector)

        1 - ВВЕРХ
        2 - ВПРАВО
        3 - ВНИЗ
        4 - ВЛЕВО
        """
        if self.vector == 1:
            self.y -= 1
            if self.y < 0:
                self.y = len(self.code) - 1
        elif self.vector == 2:
            self.x += 1
            if self.x >= len(self.code[self.y]):
                self.x = 0
        elif self.vector == 3:
            self.y += 1
            if self.y >= len(self.code):
                self.y = 0
        elif self.vector == 4:
            self.x -= 1
            if self.x < 0:
                self.y = len(self.code[self.y]) - 1

    def execute(self):
        """
        Функция выполняющая
        код Befounge

        ☦️ Дай бог ей здоровья ☦️
        """
        try:
            while True:
                value = self.code[self.y][self.x]
                if value == '@':
                    break
                if value == '"' and self.stack_sf == 0:
                    self.stack_sf = 1
                elif value == '"' and self.stack_sf == 1:
                    self.stack_sf = 0
                elif self.stack_sf == 1:
                    self.stack.append(ord(value))

                elif value.isdigit():
                    self.stack.append(int(value))

                elif value in self.operators:
                    self.op_value(value)

                elif value in self.arrows:
                    self.ar_value(value)

                elif 'a' <= value <= 'f':
                    self.hex(value)
                else:
                    self.choice_mark(value)

                self.step()

        except IndexError as e:
            print(e)
            print('Кончился стек или вышли за поле')
            sys.exit(2)

    def pop(self):
        """
        Получение последнего элемента
        из стека Befunge
        :return: Последний элемент стека
        """
        if len(self.stack):
            return self.stack.pop()
        else:
            return 0

    def op_value(self, value: str):
        """
        Базовые арифметические операции

        :param value: операция
        """
        top = self.pop()
        substrate = self.pop()
        match value:
            case '+':
                res = top + substrate
            case '-':
                res = top - substrate
            case '*':
                res = top * substrate
            case '/':
                if substrate == 0:
                    res = 0
                else:
                    res = top // substrate
            case '%':
                res = top % substrate
        self.stack.append(res)

    def ar_value(self, value: str):
        """
        Изменения направления движения
        указателя, относительно стрелочки

        :param value: стрелочка
        """
        match value:
            case '>':
                self.vector = 2
            case '<':
                self.vector = 4
            case '^':
                self.vector = 1
            case 'v':
                self.vector = 3

    def choice_mark(self, value: str):
        """
        Остальные операции, которые
        поддерживает Befunge-93/98

        :param value: операция
        """
        if value in command_registry:
            command_registry[value](self)

    @registr('!')
    def excl(self):
        """
        Инвертирование верхнего
        значения стека

        """
        top = self.pop()
        if top == 0:
            top = 1
        else:
            top = 0
        self.stack.append(top)

    @registr('`')
    def apostr(self):
        """
        Сравнение по величине
        вершины и подвершины стека

        """
        top = self.pop()
        substrate = self.pop()
        if substrate > top:
            res = 1
        else:
            res = 0
        self.stack.append(res)

    @registr('?')
    def question(self):
        """
        Выбор случайнрого направления
        движения указателя

        """
        top = random.randint(1, 4)
        self.vector = top

    @registr(':')
    def colon(self):
        """
        Клонирование вершины
        стека

        """
        if len(self.stack) > 0:
            last = self.pop()
            self.stack.append(last)
            self.stack.append(last)

    @registr('\\')
    def slash(self):
        """
        Поменять местами
        вершину и подвершину

        """

        top = self.pop()
        substrate = self.pop()
        self.stack.append(top)
        self.stack.append(substrate)

    @registr(',')
    def comma(self):
        """
        Вывести на экран
        вершину стека
        (Из ASCII в символ)

        """
        top = self.pop()
        print(chr(top), end='')

    @registr('.')
    def point(self):
        """
        Вывести на экран
        вершину стека
        (ASCII код)

        """
        top = self.pop()
        print(top, end='')

    @registr('_')
    def underline(self):
        """
        Условие движения
        (полный стек -> налево)
        (пустой стекм -> направо)

        """
        if len(self.stack) == 0:
            self.vector = 2
        else:
            self.pop()
            self.vector = 4

    @registr('|')
    def forward(self):
        """
        То же что и прошлый,
        но вверх и вниз

        """
        if len(self.stack) == 0:
            self.vector = 3
        else:
            self.pop()
            self.vector = 1

    @registr('~')
    def squiggle(self):
        """
        Получение символа

        """
        val = input('Введите символ: ')
        self.stack.append(ord(val[0]))

    @registr('&')
    def ampersand(self):
        """
        Получение числа

        """
        try:
            val = int(input('Введите число: '))
        except ValueError:
            print("Число, а не буквы")
            sys.exit(123)
        self.stack.append(val)

    @registr('p')
    def num_to_code(self):
        """
        Положить в координаты x:y
        символ из ASCII-кода
        :return:
        """
        y = self.pop()
        x = self.pop()
        symcode = self.pop()
        try:
            self.code[y] = (self.code[y][:x] + chr(symcode) +
                            self.code[y][x + 1:])
        except ValueError:
            print("\nТекущий символ не поддерживается")
            sys.exit(1)

    @registr('g')
    def code_to_num(self):
        """
        Положить в координаты x:y
        ASCII-код текущего символа

        """
        y = self.pop()
        x = self.pop()
        vl = self.code[y][x]
        self.stack.append(ord(vl))

    # From BF-98

    def hex(self, value: str):
        """
        Записать в стек 16-ое
        число

        :param value: Буква a-f
        """
        try:
            self.stack.append(int(value, 16))
        except ValueError:
            print('\nДанный символ не может быть представлен в 16-ой системе')

    @registr('q')
    def quit(self):
        """
        Завершить работу программы
        с кодом из вершины стека
        :return:
        """
        code = self.pop()
        sys.exit(code)

    # разбить, поддержка func-98, декортаор-регистрор
