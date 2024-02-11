# Калькулятор

# График
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

from tkinter import*

# Функция выбора типа калькулятора
def calcChoice():
    if var.get() == 2:
        frSimpleCalc.grid(row = 1, column = 0,
        columnspan = 4)
        frEquatCalc.grid_remove()
        plt.close()
    else:
        frEquatCalc.grid(row = 1, column = 0,
        columnspan = 4, sticky = 'w')
        frSimpleCalc.grid_remove()

###################################
# Логика простого калькулятора
# Математическое выражение,
# идентичное выведенному на экране
#####################################
expression = ""

# Логика кнопки '<<'
def backSp():
    global expression
    expression = expression[0:-1]
    entSimple['state'] = "normal"
    entSimple.delete(len(entSimple.get())-1)
    entSimple['state'] = "readonly"

# Логика кнопки 'C'
def bt_clear():
    global expression
    expression = ""
    entSimple['state'] = "normal"
    entSimple.delete(0, END)
    entSimple['state'] = "readonly"
    
# Логика основных кнопок ввода
def btn_click(item):
    global expression
    
    try:
        expression += item
        entSimple['state'] = "normal"
        entSimple.insert(END, item)

        if item == '=':
            result = str(eval(expression[:-1]))
            entSimple.insert(END, result)
            expression = ""

        entSimple['state'] = "readonly"
    except ZeroDivisionError:
        entSimple.delete(0, END)
        entSimple.insert(
            0, 'Ошибка (деление на 0)')
    except SyntaxError:
        entSimple.delete(0, END)
        entSimple.insert(0, 'Ошибка')

# Общая рамка калькулятора
root = Tk()
root.title('Калькулятор')
root.resizable(0, 0)

# Рамка выбора калькулятора
frRb = Frame(root, relief = 'raised',
    borderwidth = 8).grid(
    row = 0, column = 0, columnspan = 4)

var = IntVar()
var.set(value = 1)

rb1 = Radiobutton(frRb, text = 'Уравнение.',
    font = 'Arial 15', variable = var,
    value = 1, command = calcChoice, fg = 'red'
    ).grid(row = 0, column = 0,
    columnspan = 2)
rb2 = Radiobutton(frRb, text = 'Калькулятор.',
    font = 'Arial 15', variable = var,
    value = 2, command = calcChoice, fg = 'red'
    ).grid(row = 0, column = 2,
    columnspan = 2)

#####################
# Рамка простого калькулятора
frSimpleCalc = Frame(root, relief = 'raised',
    borderwidth = 8, bg = '#696969')

# Экран простого калькулятора
entSimple = Entry(frSimpleCalc,
    font = 'Arial 30 bold',
    width = 20, relief = 'sunken',
    borderwidth = 8, state="readonly")
entSimple.grid(
    row = 1, column = 0, columnspan = 4)

# Кнопка '<<'
btnBackspace = Button(frSimpleCalc,
    text = '<<',
    font='Arial 15 bold', width = 6,
    bg = '#B8B8B8', relief = 'raised',
    borderwidth = 8,
    command = lambda: backSp())
btnBackspace.grid(row = 2, column = 2,
    sticky = 'nsew')

# Кнопка 'C'
btnC = Button(frSimpleCalc, text='C',
    font='Arial 15 bold', width = 6,
    bg = '#B8B8B8', relief = 'raised',
    borderwidth = 8,
    command=lambda: bt_clear())
btnC.grid(row=2, column=3, sticky="nsew")

# Основные кнопки
btns = (('7', '8', '9', '/', '4'),
        ('4', '5', '6', '*', '4'),
        ('1', '2', '3', '-', '4'),
        ('0', '.', '=', '+', '4'))

for row in range(4):
    for col in range(4):
        Button(frSimpleCalc, width=6,
            text=btns[row][col],
            font='Arial 15 bold',
            relief = 'raised',
            borderwidth = 8,
            command = lambda row = row,
            col = col: btn_click(
            btns[row][col]
            )).grid(row=row + 3, column=col,
            sticky="nsew", padx=1, pady=1)


########################
# Математика уравнений #
########################
# Выражение уравнения (не на экране)
expressionX = ''

# Уравнения для вывода на График
plotEquat = ''

# Перехваты ошибок
def checkEquat(expressionX):    
    # Перехват пустого нажатия кнопки "Решение",    
    try:
        checkEquat2(expressionX)
    except (IndexError, SyntaxError):
        txtSolutionX.grid_remove()
        plt.close()
        expressionX == ''
        txtErrorX.grid(
        row = 7, column = 0,
        columnspan = 4, sticky = 'w')
        txtErrorX.insert(1.0,
        'Нажмите клавишу "С".\nВведите уравнение!\n')

def checkEquat2(expressionX):                
    # Несколько знаков '='
    if expressionX.count('=') > 1:
        txtSolutionX.grid_remove()
        plt.close()
        txtErrorX.grid(
        row = 7, column = 0,
        columnspan = 4, sticky = 'w')
        txtErrorX.insert(1.0,
        'Правильно введите уравнение!\n')
        txtErrorX.insert(2.0,
        'Оно не может содержать несколько знаков "=".\n')
    
    # Перехват ошибок ввода, напр-р: 6x+7 без "="
    else:
        try:
            checkEquat3(expressionX)
        except (IndexError, SyntaxError):
            txtSolutionX.grid_remove()
            plt.close()
            txtErrorX.grid(
                row = 7, column = 0,
                columnspan = 4, sticky = 'w')
            txtErrorX.insert(1.0,
                'Ошибка ввода уравнения!\nНажмите клавишу "С"')
    
# Перехват ошибок ввода типа: 2х3
def checkEquat3(expressionX):
    # Список ошибочных подстрок
    er = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6',
        'x7', 'x8', 'x9', 'x0', '+-', '-+' ,
        'x²1', 'x²2', 'x²3', 'x²4', 'x²5',
        'x²6', 'x²7', 'x²8', 'x²9', 'x²0',
        'xx','x²x', 'xx²', 'x²x²', '*+', '*-',
        '-*', '+*', '+=', '-=']
    for i in er:
        if i in expressionX:
            txtSolutionX.grid_remove()
            plt.close()
            txtErrorX.grid(
                row = 7, column = 0,
                columnspan = 4, sticky = 'w')
            txtErrorX.insert(1.0,
                'Неправильно введено уравнение: ' + i + ' !\n')
            txtErrorX.insert(2.0,
                'Нажмите клавишу "С"\n')
            break
        # Выражение заканчивается на знак "="
        elif [-1] == '=':
            txtSolutionX.grid_remove()
            try:
                checkEquat4(expressionX)
            except Exception:
                plt.close()
                txtErrorX.grid(
                    row = 7, column = 0,
                    columnspan = 4, sticky = 'w')
                txtErrorX.insert(1.0,
                    'Уравнение введено неполностью: ' + txtSolutionX + ' !\n')
                txtErrorX.insert(2.0,
                    'Нажмите клавишу "С"\n')            
        else:
            checkEquat4(expressionX)

def checkEquat4(expressionX):
    try:
        equat(expressionX)
    except (IndexError, SyntaxError):
        txtSolutionX.grid_remove()
        plt.close()
        
# F превращает строку уравнения в вид
# Чл1 + Чл2 + ... Члn = 0
def equat(expressionX):
    # Делим уравнение на две части по знаку "="
    y = expressionX.split('=')
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
    y0 = y + '=0\n'
    equatDisplay(expressionX, y0)
    choiceEquat(y)
    return y

# Вывод на консоль выражения y(без =0)
def outConsole():
    pass
    #print(equat(expressionX))

# Вывод на текстовое поле первых трёх строк
def equatDisplay(expressionX, y0):
    txtSolutionX.grid(row = 7, column = 0,
        columnspan = 4, sticky = 'w')
    txtSolutionX.insert(1.0,
        'Вы ввели: ' + expressionX + '\n') # 1
    txtSolutionX.insert(2.0, 'Решение: \n') #2
    txtSolutionX.insert(3.0, y0) #3

##########################
# Добавляем График ф-ции #
##########################
def plotShow():
    # Создание символьной переменной
    x = sp.symbols('x')

    # Определение функции с использованием SymPy
    y_expr = equat(expressionX)
    
    # Эта переменная пойдет на метку графика
    y_expY = 'y=' + y_expr
    
    # Адаптируем формулу под Sympy
    y_expr = y_expr.replace('x', '*x')
    y_expr = y_expr.replace('²', '**2')
    y_expr = y_expr.replace('+*', '+')
    y_expr = y_expr.replace('-*', '-')
    if y_expr[0] == '*':
        y_expr = y_expr[1:]

    # Преобразование в функцию, пригодную для использования с библиотекой Matplotlib
    y_func = sp.lambdify(x, y_expr, 'numpy')

    # Генерация значений x от -10 до 10
    x_values = np.linspace(-10, 10, 100)
    
    # Вычисление соответствующих значений y
    y_values = y_func(x_values)

    # Построение графика с использованием Matplotlib
    plt.plot(x_values, y_values, label=y_expY)
    plt.xlabel('Ось x')
    plt.ylabel('Ось y')
    plt.title('График функции.')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.show()
    


# Определяем тип уравнения:
# линейное оно или квадратное
def choiceEquat(y):
    if '²' in y:
        y = termEquat(y)
        square(y)
    else:
        y = termEquat(y)
        linear(y)

# Ф-ция разбивает строку на список [членов]
def termEquat(y):
    y = y.replace('+', ',+')
    y = y.replace('-', ',-')
    listy = y.split(',')
    return listy
    
### Функция решения линейного уравнения
def linear(y):
    # y - это список [членов уравнения]
    # Сортируем члены на те,
    # которые содержат "х" и не содержат
    yesx = []
    nox = []

    for i in y:
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
    aa = 'a = ' + str(a) + '\n'

    # Находим коэффициент "b"
    nox = ''.join(nox)
    b = eval(nox)
    bb = 'b = ' + str(b) + '\n'

    # Приводим уравнение к виду 'ax+b=0'
    yy = str(a) + 'x+' + str(b) + '=0\n'
    yy = yy.replace('+-', '-')
    txtSolutionX.insert(4.0, yy)  #4    ax+b=0
    txtSolutionX.insert(5.0, aa)  #5    a
    txtSolutionX.insert(6.0, bb)  #6    b
    txtSolutionX.insert(7.0,
        'Уравнение решается по формуле: x=-b/a, т.е.\n')  #7

    # Находим "х"
    xx = 'x = -' + str(b) + ' / ' + str(a)
    xx = xx.replace('--', '+')
    txtSolutionX.insert(8.0, xx + ' или \n')  #8

    # Перехват деления на ноль
    if a == 0:
        txtSolutionX.insert(9.0,
            'Уравнение не имеет решения, т.к. a = 0.\n')  #9
        txtSolutionX.insert(10.0,
            'На ноль делить нельзя!') #10
    else:
        x = -b/a
        x = round(x, 3)
        xx = 'x = ' + str(x) + '\n'
        txtSolutionX.insert(9.0, xx + '\n')  #9
        txtSolutionX.insert(10.0, '\n')
        txtSolutionX.insert(11.0, '\n')
        txtSolutionX.insert(12.0, '\n')
        txtSolutionX.insert(13.0, '\n')

########################################
# Функция решения квдратного уравнения
def square(y):
    # y - это список [членов уравнения]
    # Находим коэффициенты: 'а', 'b', 'c'
    a = []
    b = []
    c = []
    for i in y:
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
    yy = str(a) + 'x²+' + str(b) + 'x+' + str(c) + '=0\n'
    yy = yy.replace('+-', '-')
    #yy = yy.replace('0x²', '')
    yy = yy.replace('+-', '-')
    yy = yy.replace('-=', '=')
    yy = yy.replace('+=', '=')
    yy = yy.replace('++', '+')

    ### Неожиданный переход на линейное уравнение
    ### Когда в ходе решения стало 0x²

    if '²' not in yy:
        if 'x' not in yy:
            txtSolutionX.grid_remove()
            txtErrorX.grid(
                row = 7, column = 0,
                columnspan = 4, sticky = 'w')
            txtErrorX.insert(1.0, 'Выражение ' + str(y) + 'это не уравнение.')
        else:
            y0 = yy[:-3]
            choiceEquat(y0)
    else:
        # Решаем текущее кв_ уравнение
        txtSolutionX.insert(4.0, yy)  #4

        # Ищем дескриминант
        txtSolutionX.insert(5.0,
            'Ищем дискраминант: \n')  #5

        txtSolutionX.insert(6.0,
            'D = b² - 4ac, т.е.\n')
        
        yy = 'D=' + str(b) + '²' + '- 4 * ' + str(a) + '*' + str(c) + '\n'

        txtSolutionX.insert(7.0, yy)

        d=(b**2-4*a*c)
        d = round(d, 3)

        dd = 'D=' + str(d) + '\n'
        txtSolutionX.insert(8.0, dd)  #8

        # Ищем корни уравнения
        if d < 0:
            txtSolutionX.insert(9.0,
                'Дискриминант отрицателен.\n')
            txtSolutionX.insert(10.0,
                'Уравнение не имеет действительных решений.\n')
            txtSolutionX.insert(11.0, '\n')
            txtSolutionX.insert(12.0, '\n')
            txtSolutionX.insert(13.0, '\n')
            txtSolutionX.insert(14.0, '\n')


        elif d == 0:
            txtSolutionX.insert(9.0,   # 9, 10
                'Дискраминант равен нулю.\nУравнение имеет один корень.\n')
            x=-b/(2*a)
            txtSolutionX.insert(11.0, 'x = -b/(2a)\n')
            xx = 'x=' + str(-b) + '/(2*' + str(a) + ')\n'
            txtSolutionX.insert(12.0, xx)
            xxx = 'x=' + str(x) + '\n'
            txtSolutionX.insert(13.0, xxx + '\n')
        else:
            txtSolutionX.insert(9.0,  # 9, 10, 11
                'Дискриминант больше нуля.\nУравнение имеет два корня.\nx = (-b +- √D) / 2a, т.е.\n')
            xx1 = 'x1 =(' + str(-b) + '+√' + str(d) + ')/(2*' + str(a) + ')' # Выражение x1
            x1 = (-b+d**(0.5))/(2*a)
            x1 = round(x1, 3) # Result x1
            
            xx2 = 'x2 =(' + str(-b) + '-√' + str(d) + ')/(2*' + str(a) + ')' # Выражение x2
            x2 = (-b-d**(0.5))/(2*a)
            x2 = round(x2, 3) # Result x2

            txtSolutionX.insert(12.0, xx1 + ' = ' + str(x1) + '\n')
            txtSolutionX.insert(13.0, xx2 + ' = ' + str(x2) + '\n')
            txtSolutionX.insert(14.0, '=====================================\n')

####################################
# Логика калькулятора уравнения
# Логика кнопки '<<'
def backSpaceX():
    global expressionX
    expressionX = expressionX[0:-1]
    entX['state'] = "normal"
    entX.delete(len(entX.get())-1)
    entX['state'] = "readonly"

# Логика кнопки 'C'
def btClearX():
    global expressionX
    expressionX = ""
    entX['state'] = "normal"
    entX.delete(0, END)
    entX['state'] = "readonly"
    txtSolutionX.delete(0.0, END)
    txtSolutionX.grid_remove()
    txtErrorX.delete(0.0, END)
    txtErrorX.grid_remove()
    plotEquat = ""
    plt.close()

# Логика основных кнопок
def btn_clickX(itemX):
    global expressionX
    entX['state'] = "normal"
    expressionX += itemX
    entX.insert(END, itemX)
    entX['state'] = "readonly"

# Рамка калькулятора уравнения
frEquatCalc = Frame(root, relief = 'raised',
    borderwidth = 8, bg = '#696969')

# Экран калькулятора уравнений
entX = Entry(frEquatCalc,
    font = 'Arial 30 bold',
    width = 20, relief = 'sunken',
    borderwidth = 8)
entX.grid(
    row = 1, column = 0, columnspan = 4)

# Окно решения уравнения
txtSolutionX = Text(frEquatCalc, width = 41,
    height = 14, font = 'Arial 15')

# Окно информации об ошибках
txtErrorX = Text(frEquatCalc, width = 41,
    height = 2, font = 'Arial 15', fg = 'red')

# Кнопка 'Решение: '
btnSolutionX = Button(frEquatCalc,
    text='Решение: ',font='Arial 15 bold',
    width = 17, bg = '#FFD700',
    relief = 'raised', borderwidth = 8,
    command = lambda: [checkEquat(expressionX),
    plotShow()]).grid(
    row=2, column=0, columnspan=2)

# Кнопка '<< X'
btnBackspaceX = Button(frEquatCalc, text = '<<',
    font='Arial 15 bold', width = 6,
    bg = '#B8B8B8', relief = 'raised',
    borderwidth = 8,
    command = lambda: backSpaceX())
btnBackspaceX.grid(row = 2, column = 2,
    sticky = 'nsew')

# Кнопка 'C X'
btnCx = Button(frEquatCalc, text='C',
    font='Arial 15 bold', width = 6,
    bg = '#B8B8B8', relief = 'raised',
    borderwidth = 8,
    command = lambda: btClearX())
btnCx.grid(row=2, column=3, sticky="nsew")

# Основные кнопки X
btnsX = (('7', '8', '9', 'x'),
        ('4', '5', '6', 'x²'),
        ('1', '2', '3', '-'),
        ('0', '.', '=', '+'))

for row in range(4):
    for col in range(4):
        Button(frEquatCalc, width=6,
            text=btnsX[row][col],
            font='Arial 15 bold',
            relief = 'raised',
            borderwidth = 8,
            command = lambda
            row=row, col=col:
            btn_clickX(btnsX[row][col]
            )).grid(
            row=row + 3, column=col,
            sticky="nsew", padx=1, pady=1)

# Вызов функции выбора калькулятора,
# чтобы появилась рамка калькулятора
calcChoice()

root.mainloop()

