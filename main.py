
''' Генераторы. Пример работы функций-генераторов. Многопоточность.
numbers = list(range(1, 1000))

def ends_with_one():
    global numbers
    for n in numbers:
        if n % 10 == 1: yield n
    print("Числа кончились")

def div_on_seven(nums):
    for n in nums:
        if n % 7 == 0: yield n
    print("Больше никто не делится")

def main():
    box = div_on_seven(ends_with_one())
    while (input() == " "): print(next(box))
'''

''' Сопрограммы. В отличие от генераторов, не возвращают, а принимают значения в (yield)
def counter(num: int=9):
    while True: 
        tmp = (yield)
        if num == tmp % 3: print(tmp)

def main():
    Counter = counter(2)
    Counter.__next__() # !!!Перемещение до первой инструкции yield
    for i in range(100):
        input()
        Counter.send(i)
    Counter.close()
'''
''' Исключения. Функция документирования .__doc__ 
def problem_func(value: int):
    "Это документация к функции. попробуй вызвать problem_func.__doc__"
    print(problem_func.__doc__)
    raise(Exception("We have big problems!"))
def main():
    try:
        problem_func(0)
    except IOError as e:
        print("error:", e)
    except Exception as e:
        print(e)
    finally:
        print(12)

    print(dir(int)) # По приколу вывел все методы класса int
'''
''' Типы/Классы данных.
def main():
    kop = 1 + 10j #Комплексное число
    if type(kop) is complex: print('complexxx')
    if isinstance(kop, complex): print('xomplexx')
    if type(kop) == type([]): print("wow")
    else: print('i forgive u')
'''
''' Глубокое кипорование. deepcopy
from copy import deepcopy
def main():
    a = [1, [2, 3]]
    b = a.copy()
    b[0] = 4
    b[1][0] = 5
    print(a, b) # Заметим, что вложеный список изменен и в а, и в b, несмотря на copy
    b = deepcopy(a) # Глубокое копирование
    b[1][0] = 6
    print(a, b) # А сейчас все гуд
'''
''' Первоклассным объектам (например словарю) можно присваивать функции, модули, методы и исключения
def main():
    items = dict()
    items['function'] = abs
    import math
    items['module'] = math
    nums = [1, 2, 3]
    items['append'] = nums.append

    items['append'](4)
    print(
        nums,
        items['module'].sqrt(16),
        items['function'](-4)
    )
'''
'''
def main():
    "Применение Первоклассных объектов и zip на практике"
    line = "123, 45.0j, abc"
    types = [int, complex, str]
    box = [tp(value) for tp, value in zip(types, line.split(', '))]
    print(box)
'''
''' Методы и их вызов.
class Foo(object):
    def instance_method(self): # self - ссылка на экземляр класса Foo
        pass
    @classmethod
    def class_method(cls): # cls - ссылка на сам класс Foo
        pass
    @staticmethod
    def static_method():
        pass

def main():
    f = Foo()

    f.instance_method() # 1

    meth = f.instance_method # 2
    meth()

    meth = Foo.instance_method # 3
    meth(f)
    # Все три способы работают
'''
''' Запуск строки, как кода. exec. repr and eval.
def main():
    exec('print("Hello World!")')
    a = [1, 2, 3, 4, 5]
    # a = {'a': 1}
    b = repr(a) # -> "[1, 2, 3, 4, 5]"" # b = list.__repr__(a)
    c = eval(b) # -> [1, 2, 3, 4, 5] # c = b.__eval__()
    print(a, b, c, eval('[[1, 2], 3,"ert"]'))
'''

''' Оценка истинности последовательности. all() and any()
def main():
    print(all([1, 'ee', 0])) # -> False
    print(any([1, 'ee', 0])) # -> True
    print(all([10, abs, sum])) # -> True
    print(all([10, abs, None])) # -> False
'''
''' Магия аргументов функций. *args and **params. Удобно совмещать, когда делаешь декоратор под разные функции
def func(n:int=1, *args, **kwargs) -> None:
    print(n)
    print(args)
    print(params)
    print('-'*10)

def main():
    func()
    func(100, [1, 2, 3], 'bomb', {'k': 1}, noname=17)
    func(noname_1 = '123', noname_2 = [2, 3, 4], noname_3='prikol')
'''
''' Декораторы. Два способа связывания
# Будь внимателен, все не так очевидно
# Посмотри на вывод, сначала сработают принты внешнего декоратора!
# потому что связывание функции с декоратором, это то же самое, что
# вызов самого декоратора с передачей в него функции, как в способе 2.
def decor(vfunc):
    def callf(*args, **kwargs):
        print('Execute function', vfunc.__name__)
        return vfunc(*args, **kwargs)
    return callf

    
def external_decor(vfunc):
    print(external_decor.__name__)
    return vfunc
    
@external_decor    
@decor # 1 способ
def func():
    print('func')

def func_1(): # 2 способ
    print('func_1')
func_1 = external_decor(decor(func_1))

def main():
    func()
    print()
    func_1()

# PS: Функция-декоратор, применяемая к классу, всегда должна возвращать 
объект класса
'''
''' Декоратор с аргументами.
def event_handler(mes: str):
    def call(func):
        print(mes)
        def inner_decor(*args):
            print('inner_decor', args)
            func(*args)
        return inner_decor
    return call
# Есть отличие, но тоже работает. Нет обработки аргументов func
# def event_handler(mes: str):
#     def call(func):
#         print(mes, 'decor')
#         return func
#     return call

@event_handler("btn")
def func1(*args):
    print('func11111')

def func2(*args):
    print('func22222')
tmp = event_handler('etc')
func2 = tmp(func2)

def main():
    func1(1, 2, "func1")
    func2(1, 2, "func2")
'''

''' Декоратор для генератора(сопрограммы).
def decor_for_gener(func):
    def call(*args, **kwargs):
        tmp = func(*args, **kwargs)
        next(tmp)
        return tmp
    return call

@decor_for_gener
def gener(mes:str):
    print('Im ready for splitting.', mes)
    result = None
    while True:
        print(result)
        line = (yield result) # Это то же самое, что написать line = (yield); yield result
        result = line.split()

def main():
    runner = gener('message')
    print(runner.send("my big message !"))
    runner.close()
'''
''' Выражение-генератор. Крутость в том, что операция выполняется при вызове __next__() (или исп. for _ in _), а предыдущие вычисления не сохраняются. 
# Это позволяет повысить скорость и не занимать много памяти.
def main():
    a = [1, 2, 3, 4, 5]
    b = (i*2 if (i % 2 == 1) else 0 for i in a) # Выражение-генератор
    c = (j/2 for j in b)
    # while True:
    #     try: 
    #         print(b.__next__())
    #     except:
    #         print('exit')
    #         break
    for bc in c: # только на этом этапе посчитался очередной элемент в b, а затем элемент в c
        print(bc)
    
'''

''' Атрибуты функций. Декоратор функции с комментарием, именем и атрибутами
def wrap(func):
    call(*args, **kwargs)
        return func(*args, **kwargs)
    call.__doc__ = func.__doc__
    call.__name__ = func.__name__
    call.__dict__.update(func.__dict__) # !!!
    return call
    
@wrap
def main():
    """ Comment for main """
    print(main.__dict__, main.__name__, main.__doc__)
main.my_atribute = 5
'''
''' Eval and Exec. eval() для выражений, exec() для кода выполнения
def main():
    globals = { 'x': 7,
                'y': 10,
                'birds': ['Parrot', 'Swallow', 'Albatross']
              }
    locals = { 'x': 5 }
    # Словари, объявленные выше, используются, как глобальное и
    # локальное пространства имен при выполнении следующих инструкций
    a = eval("x + 4 * y", globals, locals)
    print(a)
    exec("for b in birds: print(b)", globals, locals)
'''
''' @classmethod. 
class Times(object):
    factor = 1

    def __init__(self, num:int):
        self.num = num
    
    @classmethod
    def new_obj(cls):
        return cls(cls.factor)

    @classmethod
    def mul(cls, x):
        return cls.factor * x

class TwoTimes(Times):
    factor = 2

def main():
    x = TwoTimes.mul(10) # Вызовет Times.mul(TwoTimes, 10) -> 20
    print(x)

    a = TwoTimes.new_obj()
    print(a.num)

    b = Times.new_obj()
    print(b.num)
'''
''' Свойства, сеттеры, геттеры и делиттеры. @property
class Foo(object):
    def __init__(self, name:str):
        self.__name = name
    
    @property # геттер
    def name(self): return self.__name
    @name.setter # сеттер
    def name(self, new_name:str): self.__name = new_name
    @name.deleter # делиттер
    def name(self): raise(Exception('Impossible to delete attribute.'))

def main():
    f = Foo('Alex')
    print(f.name)
    f.name = 'Alexey'
    print(f.name)
    try: 
        del f.name
    except Exception as e:
        print(e)
    finally:
        print("(END)")
'''        
def main():
    pass

if __name__ == "__main__":
    main()