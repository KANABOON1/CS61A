"""Functions that simulate dice rolls.

A dice function takes no arguments and returns a number from 1 to n
(inclusive), where n is the number of sides on the dice.

Types of dice:

 -  Dice can be fair, meaning that they produce each possible outcome with equal
    probability. Examples: four_sided, six_sided

 -  For testing functions that use dice, deterministic test dice always cycle
    through a fixed sequence of values that are passed as arguments to the
    make_test_dice function.
"""

from random import randint

def make_fair_dice(sides):
    """Return a die that returns 1 to SIDES with equal chance."""
    assert type(sides) == int and sides >= 1, 'Illegal value for sides'
    #assert:断言语句:真:继续执行;假:'Illegal value for sides'
    # 确保sides输入的类型:int,值:>=1
    def dice():
        return randint(1,sides)
    return dice

four_sided = make_fair_dice(4)
six_sided = make_fair_dice(6)#掷6面骰子

def make_test_dice(*outcomes):#outcomes实际传入的时候已经变为一个元组,每当调用才能重置
    """Return a die that cycles deterministically through OUTCOMES.
    >>> dice = make_test_dice(1, 2, 3)
    >>> dice()
    1
    >>> dice()
    2
    >>> dice()
    3
    >>> dice()
    1
    >>> dice()
    2

    This function uses Python syntax/techniques not yet covered in this course.
    The best way to understand it is by reading the documentation and examples.
    """
    assert len(outcomes) > 0, 'You must supply outcomes to make_test_dice'
    for o in outcomes:
        assert type(o) == int and o >= 1, 'Outcome is not a positive integer'
    #确保输入的参数数量、类型、大小全部正确
    index = len(outcomes) - 1
    #index为最后一位数的序号
    def dice():
        nonlocal index
        #nonlocal:通过每次修改外部变量index,实现多次调用index的继承!
        index = (index + 1) % len(outcomes)
        return outcomes[index]
    return dice