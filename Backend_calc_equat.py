# Backend калькулятора уравнения
# Выражение уравнения (не на экране)
import sys

expressionX = '3x²-2+5=x+3x²'
#expressionX = input('Введите уравнение: ')
print(expressionX)

# Класс проверяет уравнение на правильность
class CheckEquat:
    def __init__(self, eq):
        self.eq = eq

    def sysExit(self):
        print('Нажмите клавишу "С".')
        print('Введите заново уравнение.')
        expressionX = ''
        sys.exit()
        
    # Прoверка знака "=" в выражении
    def equall(self):
        global expressionX
        
        # Наличие более одного знака "="
        if self.eq.count('=') > 1:
            print('Уравнение не может содержать несколько знаков "=".')
            self.sysExit()

        # Выражение без знака "="
        elif '=' not in self.eq:
            print('Выражение не содержит знак "=".')
            self.sysExit()

        # Выражение без "х"
        elif 'x' not in self.eq:
            print('Выражение ' + self.eq + ' не является уравнением.')
            self.sysExit()
            
        else:
            self.endEqual()

    # Выражение заканчивается на знак "="                
    def endEqual(self):
        if self.eq[-1] == '=':
            global expressionX
            print('Уравнение введено неполностью.')
            self.sysExit()
        else:
            self.expError()

    # Проверка на наличие
    # недопустимого сочетания символов    

    def expError(self):
        # Список недопустимых подстрок
        er = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6',
             'x7', 'x8', 'x9', 'x0', '+-', '-+' ,
             'x²1', 'x²2', 'x²3', 'x²4', 'x²5',
             'x²6', 'x²7', 'x²8', 'x²9', 'x²0',
             'xx','x²x', 'xx²', 'x²x²', '*+', '*-',
             '-*', '+*', '+=', '-=']
    
        for i in er:
            if i in self.eq:
                global expressionX
                print('Ошибка ввода: ' + i)
                self.sysExit()

# Класс превращает строку уравнения в вид
# Чл1 + Чл2 + ... Члn = 0
class TermEquat:
    def __init__(self, term):
        self.term = term

    def termEquat(self):
        # Делим уравнение на две части по знаку "="
        y = self.term.split('=')
        yl = y[0]
        yr = y[1]
        
        # В правой части меняем знаки членов
        #на противоположные
        new = ''
        for i in yr:
            if i == '+':
                i = '-'
                new += i
            elif i == '-':
                i = '+'
                new += i
            else:
                i = i
                new += i
        yr = '-' + new
        yr = yr.replace('-+', '+')

        # Переносим правую часть влево
        # Приводим уравнение к виду:
        # Чл1 + Чл2 +...+Члn = 0

        # Выражение без '=0'
        y = yl + yr

        # Выражение c '=0'
        y0 = y + '=0'

        # Выражение без '=0'
        print(y0)
        return y

# Класс разбивает строку на список [членов]
class Terms:
    def __init__(self, listTerms):
        self.listTerms = listTerms

    def subDivisionTerms(self):
        self.listTerms = self.listTerms.replace('+', ',+')
        self.listTerms = self.listTerms.replace('-', ',-')
        self.listTerms = self.listTerms.split(',')
        return self.listTerms

# Класс определяет тип уравнения:
# линейное оно или квадратное

class ChoiceEquat:
    def __init__(self, equat):
        self.equat = equat

    def choiceEquat(self):
        # Переменная содержащая х²
        square = ''
        for i in self.equat:
            if '²' in i:
                square += i
        #print(square)
        if square == '':
            # Вызываем м-д объекта класса Linear()
            objLinear = LinearEquat(terms)
            objLinear.solveLinear()
        else:
            # Вызываем м-д объекта класса Square()
            objSquare = SquareEquat(terms)
            objSquare.solveSquare()
            
# Класс решения линейного уравнения
class LinearEquat:
    def __init__(self, linear):
        self.linear = linear
        
    def solveLinear(self):
        # self.linear - это список [членов уравнения]
        # Сортируем члены на те,
        # которые содержат "х" и не содержат
        yesx = []
        nox = []

        for i in self.linear:
            if 'x' in i:
                yesx += i
            else:
                nox += i
        #print(yesx)
        # Выводим строку коэффициента "а" на eval()
        yesx = ''.join(yesx)
        yesx = yesx.replace('x', '*1')
        if yesx[0] == '*':
            yesx = yesx[1:]
        yesx = yesx.replace('-*', '-')
        yesx = yesx.replace('+*', '+')
        
        # Находим коэффициент "а"
        a = eval(yesx) # Проблема
        a = round(a, 3)
        aa = 'a = ' + str(a)
        #print(aa)

        # Находим коэффициент "b"
        nox = ''.join(nox)
        b = eval(nox)
        bb = 'b = ' + str(b)
        #print(bb)

        # Приводим уравнение к виду 'ax+b=0'
        yy = str(a) + 'x+' + str(b) + '=0'
        yy = yy.replace('+-', '-')
        print('Это линейное уравнение.')
        print('Решается по формуле: x = -b/a')
        print(yy)

        # Находим "х"
        xx = 'x = -' + str(b) + ' / ' + str(a)
        xx = xx.replace('--', '+')
        print(xx)

        # Перехват деления на ноль
        if a == 0:
            print('Уравнение не имеет решения, т.к. a = 0.')  #9
            print('На ноль делить нельзя!') #10
        else:
            x = -b/a
            x = round(x, 3)
            xx = 'x = ' + str(x)
            print(xx)                

# Класс решения квдратного уравнения
class SquareEquat:
    def __init__(self, square):
        self.square = square

    def solveSquare(self):
        # square - это список [членов уравнения]
        # Находим коэффициенты: 'а', 'b', 'c'
        a = []
        b = []
        c = []
        for i in self.square:
            if 'x²' in i:
                a += i
            elif 'x' in i and '²' not in i:
                b += i
            else:
                c += i

        a = ''.join(a)
        a = a.replace('x²', '*1')
        a = a.replace('+*', '+')
        a = a.replace('-*', '-')
        if a[0] == '*':
                a = a[1:]
        elif a[0] == '²':
            a = '0' + a
        a = eval(a)
        a = round(a, 3)
       
        b = ''.join(b)
        b = b.replace('x', '*1')
        b = b.replace('+*', '+')
        b = b.replace('-*', '-')

        if b == []:
            b = 0
        elif b != 0:
            if b == '':
                b = '0'
            elif b[0] == '*':
                b = b[1:]

        b = eval(b)
        b = round(b, 3)

        if c == []:
            c = 0
        else:
            c = ''.join(c)
            c = eval(c)
            c = round(c, 3)

        # Приводим уравнение к виду: ax²+bx+c=0
        yy = str(a) + 'x²+' + str(b) + 'x+' + str(c) + '=0'
        yy = yy.replace('+-', '-')
        yy = yy.replace('+-', '-')
        yy = yy.replace('-=', '=')
        yy = yy.replace('+=', '=')
        yy = yy.replace('++', '+')
        print(yy)

        ### Неожиданный переход на линейное уравнение
        ### Когда в ходе решения стало 0x²

        if a == 0:
            yy = yy.replace('0x²', '')
            if 'x' not in yy:
                print('Выражение ' + str(y) + 'это не уравнение.')
            else:
                y0 = yy[:-2]
                listTerms = Terms(y0)
                terms = listTerms.subDivisionTerms()
                objLinear = LinearEquat(terms)
                objLinear.solveLinear()
        else:
            # Решаем текущее кв_ уравнение
            # Ищем дескриминант
            print('Ищем дискраминант: ')  #5
            print('D = b² - 4ac, т.е.')
            
            yy = 'D=' + str(b) + '²' + '-4*' + str(a) + '*' + str(c)

            print(yy)

            d=(b**2-4*a*c)
            d = round(d, 3)

            dd = 'D=' + str(d)
            print(dd)  #8

            # Ищем корни уравнения
            if d < 0:
                print('Дискриминант отрицателен.')
                print('Уравнение не имеет действительных решений.')

            elif d == 0:
                print('Дискраминант равен нулю.')
                print('Уравнение имеет один корень.')
                x=-b/(2*a)
                print('x = -b/(2a)')
                xx = 'x=' + str(-b) + '/(2*' + str(a) + ')'
                print(xx)
                xxx = 'x=' + str(x)
                print(xxx)
            else:
                print('Дискриминант больше нуля.')
                print('Уравнение имеет два корня.')
                print('x = (-b +- √D) / 2a, т.е.')
                xx1 = 'x1 =(' + str(-b) + '+√' + str(d) + ')/(2*' + str(a) + ')' # Выражение x1
                x1 = (-b+d**(0.5))/(2*a)
                x1 = round(x1, 3) # Result x1
                
                xx2 = 'x2 =(' + str(-b) + '-√' + str(d) + ')/(2*' + str(a) + ')' # Выражение x2
                x2 = (-b-d**(0.5))/(2*a)
                x2 = round(x2, 3) # Result x2
                print(xx1 + ' = ' + str(x1))
                print(xx2 + ' = ' + str(x2))
            
###############################################
# Проверкa выражения на правильность
exp = CheckEquat(expressionX)
exp.equall()

# Перевод выражения в вид
# Чл.1 + Чл.2 + ... + Члn = 0
expTerm = TermEquat(expressionX)

# Перехват исключения
try:
    # equation это уравнение без "=0"
    equation = expTerm.termEquat()
except Exception:
    expressionX = ''
    print('Нажмите клавишу "С"')
    print('Введите заново уравнение.')

# Разбиваем строку уравнения на список [членов]
listTerms = Terms(equation)
terms = listTerms.subDivisionTerms()

# Определяем тип уравнения:
# линейное оно или квадратное
# и решаем его
choicedEquat = ChoiceEquat(terms)
choicedEquat.choiceEquat()
