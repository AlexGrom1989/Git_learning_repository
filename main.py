
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
            
def main():
    pass

if __name__ == "__main__":
    main()