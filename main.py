""" Установка в py проекте виртуальной среды .venv/ . Почему это работает только на линуксе епрст емае ааа??!! дурак виндовс
sudo apt-get install python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip freeze > requirements.txt
"""



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
    a = [(1, 2, 3), (4, 5, 6)]
    b = zip(*a)
    print(b) # -> [(1, 4), (2, 5), (3, 6)]
    print(zip(*b)) # -> [(1, 2, 3), (4, 5, 6)]

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
    b = repr(a) # -> "[1, 2, 3, 4, 5]" # b = list.__repr__(a)
    c = eval(b) # -> [1, 2, 3, 4, 5] # c = b.__eval__()
    print(a, type(b), type(c), eval('[[1, 2], 3,"ert"]'))
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
    print(kwargs)
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
# объект класса
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

''' Декоратор для генератора/сопрограммы.
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
    def call(*args, **kwargs):
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
''' Эксперименты с питоном.
class F():
    @classmethod
    def df(cls):
        return 123

def fe(x): return 42
def fe(*args): return type(args)

def s(string:list):
    string += [1]
    print(string)

from collections import namedtuple
def main():
    f = F()
    print( "hello" 'world' )
    print(sum({1:2, 2:3}))
    t = namedtuple('Point', 'x y')
    a = t(1, 2)
    b = t(3, 4)
    # a.x = 0 # error
    print(a.x + b.x)
    g = {1, 7, 9}
    g.update(i for i in range(10))
    print(g)
    print(fe(10))
    string = []
    s(string)
    print(string)
'''
''' Дескрипторы. Самая сложная тема
class TypedProperty(object):
    def __init__(self,name,type,value=None):
        self.name = "_" + name
        self.type = type
        self.value = value if value else type()

    def __get__(self,instance,cls):
        return getattr(instance,self.name,self.value)
    
    def __set__(self,instance,value):
        if not isinstance(value,self.type):
            raise TypeError("“Значение должно быть типа %s”" % self.type)
        setattr(instance,self.name,value)

    def __delete__(self,instance):
        raise AttributeError("“Невозможно удалить атрибут”")
    
class Foo(object):
    name = TypedProperty("name",str)
    num = TypedProperty("num",int,42)
    
    def __init__(self, name, num) -> None:
        self.name = name
        self.num = num

    def __str__(self) -> str:
        return self.name + self.num.__str__()
    


def main():
    f = Foo('alex', 12)
    d = Foo("andrey", 13)
    print(f, d)
    print(f._name, f.name)
'''
''' Минутка полиморфизма. __smth is private attribute.
class A():
    def __init__(self) -> None:
        self.__a = "zxc"
        self.a = "qwe"
    
    def prt(self):
        print(self.a, "BUT", self.__a)

class B(A):

    def __init__(self) -> None:
        A.__init__(self)
        self.a = "asd"   
        self.__a = 'rty'

def main():
    b = B()
    b.prt()
    b.dfg = 90
    print(b.dfg)
'''
''' Правила передачи параметров. Позиционные, / , любая передача, *, передача по ключу
def func(positional_only, /, either, *, keyword_only):
    print('Done with:', positional_only, either, keyword_only)

def main():

    # Not Allowed
    # func(positional_only="Frank", "Bob", keyword_only="Alex")
    # func("Frank", either="Bob", "Alex")
    # func("Frank", keyword_only="Alex", "Bob")

    # Allowed
    func("Frank", "Bob", keyword_only="Alex")
    func("Frank", either="Bob", keyword_only="Alex")
    func("Frank", keyword_only="Alex", either="Bob")
'''
''' Перегрузка операторов.
class Kop(object):
    def __init__(self, num):
        self.num = num

    def __repr__(self): return f"Kop({self.num})"
    
    def __str__(self): return "-> %s <-" % (self.num)

    def __add__(self, val): return Kop(self.num + val)
    # right add => instance after value
    def __radd__(self, val): return self.__add__(val)

    def __sub__(self, val): return Kop(self.num - val)
    # right sub => instance after value
    def __rsub__(self, val): return Kop(val - self.num)

def main():
    k = Kop(10)
    print(k + 11)
    print(11 + k)
    print(k - 11)
    print(11 - k)
'''
''' Абстрактные классы.
from abc import abstractmethod, ABCMeta
class Foo(metaclass=ABCMeta):

    @abstractmethod
    def spam(self, a, b): pass

    @property
    def name(self): pass


class Grep:
    def spam(self, a=1, b=2):
        print("Grep.spam")

Foo.register(Grep)

def main():
    g = Grep()
    g.spam()
    print(isinstance(g, Foo))
'''
''' Оператор **
def calc(a, c, b):
    return a + b*0 + c

def main():
    pars = {"a": 2, "b": 4, "c": 6}
    nums = [2, 6, 4]
    print(calc(*nums))
    print(calc(**pars))
'''
''' logging
import logging

logging.basicConfig(
    filename='logging.log', # файл записи
    filemode='w', # режим записи
    level=logging.INFO, # Уровень важности
    format="%(levelname)-9s %(asctime)-30s LineNum:%(lineno)-7d %(message)s"
)
log = logging.getLogger('main')

class FilterFunc(logging.Filter):
    def __init__(self,name):
        self.funcName = name
    def filter(self, record):
        if self.funcName == record.funcName: return False
        else: return True

log.addFilter(FilterFunc('func')) # Игнорировать все сообщения из функции func()

# Next, the execute code

def func(num:int):
    def call():
        log.error("We have big troubles in call function") # will react, despite it placed in func()
    if num == 10: call()
    else: log.info(f"Don't worry, num equal {num}")


def main():
    func(10)
    func(12)
    log.debug("debug msg")
    log.info("info msg")
    log.warning("warning msg")
    log.error("error msg")
    log.critical("critical msg")
'''

''' Маржа. Присваивание результата переменной и одновременный его возврат.
def main():
    if y:=min([1, 2, 3]) == 1: print(y)
'''

''' Наследование. super. Если super указать 
# только в подклассе(дочернем), то вызовется метод первого родителя, 
# иначе если указать везде, то методы будут вызываться в порядке наследования .mro()
class Person(object):
 
    def __init__(self, name):
        super().__init__(name)
        self.__name = name   # имя человека
 
    @property
    def name(self):
        return self.__name
 
    def display_info(self):
        super().display_info()
        print(f"PName: {self.__name}")
 
class B(object):

    def __init__(self, name):
        self.__name = name

    def display_info(self):
        print(f"BName: {self.__name}")
 
class Employee(Person, B):
 
    def __init__(self, name, company):
        super().__init__(name)
        self.company = company
 
    def display_info(self):
        super().display_info()
        print(f"Company: {self.company}")
 
    def work(self):
        print(f"{self.name} works")

        
def main():
    print(Employee.mro())
    tom = Employee("Tom", "Microsoft")
    tom.display_info()  # Name: Tom
                        # Company: Microsoft
'''

# ''' Регулярные выражения regex. import re
# import re

# def main():
#     """
#         Расшифровка:

#     - `U` - поиск символа U (или любого другого символа, указанного буквально)
#     - `a-z` - любой символ в интервале
#     - `[abc]` - любой из символов a, b или c
#     - `[^abc]` - любой из символов, кроме abc
#     - `.` - любой символ
#     - `\d` - любая цифра (0-9)
#     - `\D` - любой символ, кроме цифры
#     - `\w` - любой символ слова ([a-zA-Z0-9_])
#     - `\s` - любой символ пробела
#     - `{4}` - количество повторений предыдущего токена (4 раза)
#     - `+` - предыдущий токен должен повториться 1 или более раз
#     - `*` - предыдущий токен должен повториться 0 или более раз
#     - `()` - группа захвата

#     См. также: [https://regex101.com/](https://regex101.com/)
#     """
#     log_line = '2023-10-27 10:30:00 - ERROR - User [johndoe] attempted login from IP 192.168.1.100'
#     pattern = r'(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+-\s+(\w+)\s+-\s+User\s+\[(\w+)\]\s+attempted\s+login\s+from\s+IP\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    
#     match = re.search(pattern, log_line) # match - совпадение
#     if match:
#         date, time, level, username, ip = match.groups() # можно разбить по группам захвата (по скобочкам)
#         print(f"Date: {date}, Time: {time}, Level: {level}, Username: {username}, IP: {ip}")

#     email = "test.user+alias@example.com"
#     pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
#     if re.match(pattern, email):
#         print("Valid email address")
#     else:
#         print("Invalid email address")

#     text = "This is a sentence with some phone numbers: 123-456-7890 and (555) 123-4567."
#     pattern = r"\(*(\d{3})\D*(\d{3})\D*(\d{4})"
#     replacement = r"(\1) \2-\3"

#     print(re.sub(pattern, replacement, text)) # Подстановка групп захвата под шаблон

#     text = "I have 10 apples and 20 oranges."
#     pattern = r"\d+(?= apples)"

#     print(re.findall(pattern, text)) # Поиск всех совпадений в тексте
# '''
''' Создание архитектуры базы данных для ЛБ2 3 семестр.
import pandas as pd
import numpy as np
import faker
from russian_names import RussianNames
import random
import datetime as dt

cities = [
    "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань",
    "Нижний Новгород", "Челябинск", "Самара", "Омск", "Ростов-на-Дону",
    "Уфа", "Красноярск", "Воронеж", "Пермь", "Волгоград"
]

fake = faker.Faker()

faculties = {
    "Факультет информационных технологий": [
        "Программная инженерия",
        "Информационные системы",
        "Кибербезопасность"
    ],
    "Факультет экономики и финансов": [
        "Экономика",
        "Бухгалтерский учет",
        "Маркетинг"
    ],
    "Факультет гуманитарных наук": [
        "Психология",
        "Социология",
        "История"
    ],
    "Факультет естественных наук": [
        "Биология",
        "Химия",
        "Физика"
    ],
    "Факультет юриспруденции": [
        "Правоведение",
        "Уголовное право",
        "Гражданское право"
    ],
    "Факультет медицины": [
        "Общая медицина",
        "Стоматология",
        "Фармацевтика"
    ],
    "Факультет архитектуры": [
        "Архитектура",
        "Дизайн интерьеров",
        "Градостроительство"
    ],
    "Факультет искусства": [
        "Изобразительное искусство",
        "Музыка",
        "Театр"
    ],
    "Факультет иностранных языков": [
        "Английский язык",
        "Французский язык",
        "Испанский язык"
    ],
    "Факультет педагогики": [
        "Педагогика",
        "Психология образования",
        "Специальное образование"
    ],
    "Факультет физической культуры": [
        "Спорт",
        "Фитнес",
        "Туризм"
    ],
    "Факультет сельского хозяйства": [
        "Агрономия",
        "Ветеринария",
        "Агроинженерия"
    ],
    "Факультет социальных наук": [
        "Политология",
        "Экономическая социология",
        "Социальная работа"
    ],
    "Факультет авиации и космонавтики": [
        "Авиастроение",
        "Космические технологии",
        "Пилотирование"
    ],
    "Факультет электроники": [
        "Электронные системы",
        "Нанотехнологии",
        "Автоматизация"
    ]
}
fac_names = faculties.keys()
faculties = {''.join([j[0] for j in i.split()]).upper():faculties[i] for i in faculties}
spec_to_fac = {i:f for f in faculties.keys() for i in faculties[f]}


def make_students():
    df = pd.DataFrame()
    df.index.name = 'student_id'
    df['name'] = list(RussianNames(count=1000))

    for i in range(1000):

        df.loc[i, 'birth_date'] = fake.date_of_birth(minimum_age=18, maximum_age=23)
        df.loc[i, 'city'] = cities[random.randint(0, len(cities)-1)]
        df.loc[i, 'admission_year'] = df.loc[i, 'birth_date'].year + 16 + random.randint(1, 2)
    
    df['admission_year'] = df['admission_year'].astype(np.int64)

    # df.to_csv('students.csv')
    return df.copy()


def make_groups():
    df = pd.DataFrame()
    df.index.name = 'group_id'

    df['students_amount'] = [25]*40
    df['exam_date'] = [fake.date_between_dates(dt.date(2024, 5, 10), dt.date(2024, 6, 30)) for _ in range(len(df.students_amount))]

    # df.to_csv('groups.csv')
    return df.copy()


def make_facs():
    df = pd.DataFrame()

    df['faculty_code'] = faculties.keys()
    df['faculty_name'] = fac_names
    df['dekan'] = list(RussianNames(count=len(df.faculty_code)))
    df['place_amount'] = [random.randint(75, 100) for _ in range(len(df.faculty_code))]

    # df.to_csv('faculties.csv', index=False)
    return df.copy()


def make_specs(fac):
    df = pd.DataFrame()
    df.index.name = 'spec_id'

    df['spec_name'] = [j for i in faculties for j in faculties[i]]
    df['faculty_code'] = [spec_to_fac[i] for i in df.spec_name]

    # df.to_csv('specs.csv')
    return df.copy()


def make_edus(fac, spec, student, group):
    df = pd.DataFrame()
    
    df['student_id'] = student.index

    tmp = group['students_amount']
    for i in range(len(df.student_id)):

        id = random.choice(tmp.index)
        df.loc[i, 'group_id'] = id

        tmp.loc[id] -= 1
        if tmp.loc[id] == 0: 
            tmp = tmp.drop(id, axis=0)

    # tmp = spec['faculty_code']
    # tmp = tmp.copy().map(fac.set_index('faculty_code')['place_amount']) # Не пригодилось, но умение важное

    tmp = fac[['faculty_code', 'place_amount']]

    for i in range(len(group.index)):
        id = random.choice(tmp.index)
        sp = random.choice(faculties[tmp['faculty_code'][id]])
        df.loc[df.group_id == i, 'spec_id'] = spec[spec.spec_name == sp].index[0]
        
        tmp.loc[id, 'place_amount'] -= 25
        if tmp.loc[id, 'place_amount'] // 25 == 0:
            tmp = tmp.drop(id, axis=0)

    df = df.astype('int')
            
    grants = [0, 3500, 4500, 5700, 15000]
    df['stipend'] = random.choices(grants, weights=[0.5, 0.2, 0.2, 0.15, 0.05], k=len(df.student_id))

    # df.to_csv('edu.csv', index=False)




def main():
    student = make_students()
    group = make_groups()
    fac = make_facs()
    spec = make_specs(fac=fac)
    make_edus(fac=fac, spec=spec, student=student, group=group)
'''


''' Мусор. ДЗ ЦК
import datetime


def gift_count(budget, month, birthdays):

    s = ''

    for name, dt in list(birthdays.items()):
        if dt.month != month: birthdays.pop(name)
        else: 
            if s != '': s += ', '
            s += f'{name} ({dt.strftime("%d.%m.%Y")})'
    
    if s == '':
        print("В этом месяце нет именинников.")
    else:
        print(f"Именинники в месяце {month}: {s}. При бюджете {budget} они получат по {int(budget/len(birthdays))} рублей.")
    


def main():
    birthdays = {"Иванов Иван Иванович": datetime.date(1989, 5, 1), "Петров Петр Петрович": datetime.date(1998, 5, 6)}

    gift_count(20000, 5, birthdays)

    gift_count(budget=20000, month=5, birthdays=birthdays)
'''

# import re

# def check_string(string) -> bool:
#     phone = re.match(r'^\w+(\.\w+)*@\w{2,}(\.\w{2,})*$', string)
#     mail = re.match(r'^(\+7|8){0,1}\D{0,2}\d{3}\D{0,2}\d{3}\D{0,1}\d{2}\D{0,1}\d{2}$', string)
#     return phone, mail


# ss = '''89160000000
# 8916000000000
# +79160000000
# 9160000000
# 8(916)000-00-00
# +7(916)000-00-00
# (916)000-00-00
# 8 (916) 000-00-00
# +7 (916) 000-00-00
# (916) 000-00-00
# 8(916)0000000
# +7(916)0000000
# (916)0000000
# 8-916-000-00-00
# +7-916-000-00-00
# 916-000-00-00'''.split('\n')

# def main():
    
#     for i in ss:
#         print(check_string(i))
        

'''
import json

def main():
    tmp = json.dumps({"asdf":1,  "qweew": [{"afsg": 22, "234tfds": 33}]})
    tmp = json.loads(tmp)
    print(type(tmp), tmp)
'''
# '''
# import re

# def is_valid_expression(expression):
#     ex = expression
#     if ex.count('(') != ex.count(')'): return False
    
#     rex = re.match(r'^([\/\*\-\+ \(]*\d*[ \/\*\-\+\)]*)*$', ex)
    
#     print(rex)

# def main():
#     is_valid_expression('(8 + (345 + 13) / 9 * 6 - 12)')
# '''
'''
import json

def generate_task_report(filename):
    
    with open(filename, 'r') as f:
        data = json.loads(f.read())
    
    res = {
        'total_tasks': 0,
        'completed_tasks': 0,
        'high_priority_tasks': 0
    }

    for i in data:
        res['total_tasks'] += 1
        res['high_priority_tasks'] += i['priority'] == 'high'
        res['completed_tasks'] += i['status'] == 'completed'

    return json.dumps(res)

def main():
    print(generate_task_report('test.json'))
'''
'''
def count_word_occurrences(filename, word):
    import re
    
    answer = 0
    
    with open(filename, 'r') as f:
        while r := f.readline():
            answer += len(re.findall(rf'\b{word}\b', r.lower()))
    
    return f"Слово '{word}' встречается в файле '{filename}' {answer} раз."

def main():
    print(count_word_occurrences('test.txt', 'tnyn'))
'''
'''
class Calculator(object):
    last = None
    
    def __init__(self):
        self._history = []
        
    def sum(self, a, b):
        c = a + b
        Calculator.last = f'sum({a}, {b}) == {c}'
        self._history.append(Calculator.last)
        return c
        
    def sub(self, a, b):
        c = a - b
        Calculator.last = f'sub({a}, {b}) == {c}'
        self._history.append(Calculator.last)
        return c

    def mul(self, a, b):
        c = a * b
        Calculator.last = f'mul({a}, {b}) == {c}'
        self._history.append(Calculator.last)
        return c
    
    def div(self, a, b, mod=False):
        c = a % b if mod else a / b
        Calculator.last = f'div({a}, {b}) == {c}'
        self._history.append(Calculator.last)
        return c
    
    def history(self, n):
        if n > len(self._history): return 0
        return self._history[-n]
        
    @classmethod
    def clear(cls):
        cls.last = None
        
        
def main():
    c = Calculator()
    c.sum(1, 2)
    print(c.history(1))
    print(c.last)
    print(Calculator.last)
'''
'''
class BaseWallet(object):
    def __init__(self, name, amount):
        self.c_name = 'Base Wallet'
        self.name = name
        self.amount = amount
        self.exchange_rate = 1

    def calc(self, other, l_func):
        if type(self) == type(other):
            return self.__class__(self.name, l_func(self.amount, other.amount))
        elif hasattr(other, 'amount'): 
            tmp = RubleWallet('tmp', l_func(self.to_base(), other.to_base()))
            return self.__class__(self.name, tmp.amount / self.exchange_rate)
        else:
            return self.__class__(self.name, l_func(self.amount, other))

    def __add__(self, other):
        return self.calc(other, lambda x, y: x + y)
    def __radd__(self, other): return self.__add__(other)


    def __sub__(self, other, r_flag=-1):
        return self.calc(other, lambda x, y: -r_flag*(x - y))
    def __rsub__(self, other): return self.__sub__(other, r_flag=1)


    def __truediv__(self, other, r_flag=0):
        return self.calc(other, lambda x, y: (x/y, y/x)[r_flag])
    def __rtruediv__(self, other): return self.__truediv__(other, r_flag=1)


    def __mul__(self, other):
        return self.calc(other, lambda x, y: x * y)
    def __rmul__(self, other): return self.__mul__(other)


    def __eq__(self, other):
        return type(self) == type(other) and self.amount == other.amount


    def spend_all(self):
        self.amount = min(0, self.amount)

    def to_base(self):
        return self.amount * self.exchange_rate
    
    def __str__(self):
        return f"{self.c_name} {self.name} {self.amount}"

    # def __str__(self):
    #     return f"name: {self.name}, amount: {self.amount}, e_rate: {self.exchange_rate}"

class RubleWallet(BaseWallet):
    def __init__(self, name, amount):
        super().__init__(name, amount)
        self.c_name = 'Ruble Wallet'
        self.exchange_rate = 1

class DollarWallet(BaseWallet):
    def __init__(self, name, amount):
        super().__init__(name, amount)
        self.c_name = 'Dollar Wallet'
        self.exchange_rate = 60

class EuroWallet(BaseWallet):
    def __init__(self, name, amount):
        super().__init__(name, amount)
        self.c_name = 'Euro Wallet'
        self.exchange_rate = 70
    

def main():
    r = RubleWallet('x', 1)
    d = DollarWallet('d', 1)
    e = EuroWallet('e', 1)
    
    print(
        10 / r,
        r / 10,
        r == r,
        sep='\n'

    )'''
'''
import datetime
class Meeting(object):

    def __init__(self, name, date, start_time, duration):
        self.name = name
        self.date = date
        self.start_time = start_time
        self.duration = duration
        self._duration = datetime.timedelta(hours=duration//60, minutes=duration%60)
        self.participants = []
    
    @property
    def end_time(self):
        meet_datetime = datetime.datetime.combine(self.date, self.start_time)
        return (meet_datetime + self._duration).time()

    def get_participants(self):
        return self.participants

    def __lt__(self, other):
        return self.start_time < other.start_time and self.date == other.date or self.date < other.date

    # def __str__(self):
    #     return f"{self.date} {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}: {self.name}"
    # def __repr__(self): return self.__str__()

class Employee(object):

    def __init__(self, name):
        self.name = name
        self.schedule = []

    def add_meeting(self, meeting):

        for i in self.schedule:
            if meeting.start_time < i.end_time and meeting.start_time > i.start_time and meeting.date == i.date:
                return False

        meeting.participants.append(self.name)
        self.schedule.append(meeting)
        return True

    def get_schedule(self):
        # return sorted(self.schedule)
        sorted_schedule = sorted(self.schedule)
        return [
            f"{m.date} {m.start_time.strftime('%H:%M')} - {m.end_time.strftime('%H:%M')}: {m.name}"
            for m in sorted_schedule
        ]

def main():
    employee1 = Employee("Борис Петров")
    employee2 = Employee("Иван Иванов")

    # Создаем встречу, указывая название, дату, начало и длительность встречи
    meeting1 = Meeting("Встреча с клиентом", datetime.date(2024, 9, 10), datetime.time(10, 0), 60)
    print(meeting1.name)  # Выведет "Встреча с клиентом"
    print(meeting1.date)  # Выведет datetime.date(2024, 9, 10)
    print(meeting1.start_time)  # Выведет datetime.time(10, 0)
    print(meeting1.duration)  # Выведет 60
    print(meeting1.participants)  # Выведет [] (пустой список, так как пока нет участников)

    # Время окончания встречи рассчитано автоматически на основе start_time и duration
    print(meeting1.end_time)  # Выведет datetime.time(11, 0)

    # Создаем еще одну встречу
    meeting2 = Meeting("Планерка", datetime.date(2024, 9, 11), datetime.time(14, 0), 30)
    meeting3 = Meeting("asdfgh", datetime.date(2024, 9, 11), datetime.time(14, 29), 30)
    #Добавляем встречи в расписания сотрудников
    employee1.add_meeting(meeting1)
    employee2.add_meeting(meeting2)

    print(employee1.get_schedule()) # Выведет ['2024-09-10 10:00 - 11:00: Встреча с клиентом']
    print(employee2.get_schedule()) # Выведет ['2024-09-11 14:00 - 14:30: Планерка']

    # Добавление второй встречи в расписание Бориса
    employee1.add_meeting(meeting2)

    employee1.add_meeting(meeting3)

    print(employee1.get_schedule()) # Выведет ['2024-09-10 10:00 - 11:00: Встреча с клиентом', '2024-09-11 14:00 - 14:30: Планерка']

    print(meeting2.get_participants()) # Выведет ['Иван Иванов', 'Борис Петров']
'''
'''
import re
class Field(object):

    def __init__(self):
        self.table = dict()
    
    @staticmethod
    def reshape(key):

        if not isinstance(key, (tuple, str)):
            raise TypeError
        
        if type(key) == tuple: key = str(key[0]) + str(key[1])
        key = key.lower()

        re_key = re.findall(r'[a-z]{1}\d+|\d+[a-z]{1}', key)

        if len(re_key) != 1 or re_key[0] != key:
            raise ValueError
        
        if key[0].isdigit(): key = key[-1] + key[:-1]
        
        return key

    
    def __getitem__(self, key):
        try:
            return self.table[self.reshape(key)]
        except KeyError: return None
        except ValueError as e: raise e
        except TypeError as e: raise e

    def __setattr__(self, name, value):
        if name[0].isalpha() and name[1].isdigit():
            super().__setattr__(self.reshape(name), value)
            super().__setattr__(self.reshape(name).upper(), value)
            self.table[self.reshape(name)] = value
        else:
            super().__setattr__(name, value)

    def __setitem__(self, key, value):
        self.__setattr__(self.reshape(key), value)

    def __delattr__(self, name):
        if name[0].isalpha() and name[1].isdigit():
            super().__delattr__(name.lower())
            super().__delattr__(name.upper())
            del self.table[self.reshape(name)]
        else:
            super().__delattr__(name)
    
    def __delitem__(self, key):
        self.__delattr__(self.reshape(key))

    def __contains__(self, key):
        return self.reshape(key) in self.table

    def __iter__(self):
        for value in self.table:
            yield self.table[value]


def main():
    f = Field()
    f[12, 's'] = 2
    f.d2d23 = 3
    print(f.table, f.__dict__)'''
    
'''
class Fraction(object):
    def __init__(self, ch:int, zn:int):
        if zn <= 0: raise ValueError("Знаменатель не может быть нулевым или отрицательным")
        
        nod = Fraction.evk(abs(ch), abs(zn))
        self.ch = ch // nod
        self.zn = zn // nod

    @staticmethod
    def evk(f, s):
        while f * s != 0:
            if f >= s: f %= s
            else: s %= f
        return max(f, s)

    def __str__(self):
        return f"{self.ch}/{self.zn}"

    def __add__(self, other):
        return Fraction(self.ch*other.zn + other.ch*self.zn, self.zn * other.zn)

    def __sub__(self, other):
        return Fraction(self.ch*other.zn - other.ch*self.zn, self.zn * other.zn)

    def __mul__(self, other):
        return Fraction(self.ch * other.ch, self.zn * other.zn)
    
    def __truediv__(self, other):
        if other.ch == 0: raise ZeroDivisionError
        return Fraction(self.ch * other.zn, self.zn * other.ch)
    
    def __eq__(self, other):
        return self.__str__() == other.__str__()
    
    def __lt__(self, other):
        return self.ch/self.zn < other.ch/other.zn



def main():
    print(
        Fraction.evk(1, 2),
        Fraction(1, 2) != Fraction(20, 35)

    )'''



if __name__ == "__main__":
    main()
