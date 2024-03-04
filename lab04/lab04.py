LAB_SOURCE_FILE = __file__



this_file = __file__

def skip_add(n):
    """ Takes a number n and returns n + n-2 + n-4 + n-6 + ... + 0.

    >>> skip_add(5)  # 5 + 3 + 1 + 0
    9
    >>> skip_add(10) # 10 + 8 + 6 + 4 + 2 + 0
    30
    >>> # Do not use while/for loops!
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(this_file, 'skip_add',
    ...       ['While', 'For'])
    True
    """
    if n==1: # base case : 设置奇数时的出口
        return 1
    elif n==0:# base case : 设置偶数时的出口
        return 0
    else:
        return n+skip_add(n-2)

def summation(n, term):

    """Return the sum of the first n terms in the sequence defined by term.
    Implement using recursion!

    >>> summation(5, lambda x: x * x * x) # 1^3 + 2^3 + 3^3 + 4^3 + 5^3
    225
    >>> summation(9, lambda x: x + 1) # 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10
    54
    >>> summation(5, lambda x: 2**x) # 2^1 + 2^2 + 2^3 + 2^4 + 2^5
    62
    >>> # Do not use while/for loops!
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(this_file, 'summation',
    ...       ['While', 'For'])
    True
    """
    assert n >= 1
    def helper(index):
        """尾递归:向上的递归:计算从index至n的term(index)之和."""
        if index==n:
            return term(n)
        else:
            return term(index)+helper(index+1)
    return helper(1)


def paths(m, n):
    """Tree recursion:Return the number of paths from one corner of an
    M by N grid to the opposite corner.

    >>> paths(2, 2)
    2
    >>> paths(5, 7)
    210
    >>> paths(117, 1)
    1
    >>> paths(1, 157)
    1
    """
    if n==1 or m==1:
        return 1
    else: #将问题向下分解为paths(m-1,n) and paths(m,n-1),只要实现了向下/向上拆分问题,并且设置了相应的出口,即可确保递归的返回值.
        return paths(m-1,n)+paths(m,n-1)

def max_subseq(n, t):
    """
    Return the maximum subsequence of length at most t that can be found in the given number n.
    For example, for n = 20125 and t = 3, we have that the subsequences are
        2
        0
        1
        2
        5
        20
        21
        22
        25
        01
        02
        05
        12
        15
        25
        201
        202
        205
        212
        215
        225
        012
        015
        025
        125
    and of these, the maxumum number is 225, so our answer is 225.

    >>> max_subseq(20125, 3)
    225
    >>> max_subseq(20125, 5)
    20125
    >>> max_subseq(20125, 6) # note that 20125 == 020125
    20125
    >>> max_subseq(12345, 3)
    345
    >>> max_subseq(12345, 0) # 0 is of length 0
    0
    >>> max_subseq(12345, 1)
    5
    """
    """def get_length(n):
        if n // 10 == 0:
            return 1
        else:
            return 1 + get_length(n // 10)
    def get_max2(n, width):
        max, length, counter, index = n // (10 ** (get_length(n) - 1)), get_length(n), 0, 1
        while n // 10:
            counter += 1
            if counter > width:
                break
            if n // (10 ** (length - counter)) > max:
                max, index = n // (10 ** (length - counter)), counter
            n %= 10 ** (length - counter)
        return max, index
    if t == 0:
        return 0
    elif t == 1:
        return get_max2(n,get_length(n))[0]
    elif n // 10 ** (t - 1) == 0:
        return n
    else:
        max, index = get_max2(n, get_length(n) + 1 - t)
        return max * 10 ** (t - 1) + max_subseq(n % 10 ** (get_length(n) - index), t - 1)"""
    if t == 0:
        return 0
    elif n // 10 ** t == 0:
        return n
    else:
        return max(max_subseq(n // 10, t - 1) * 10 + n % 10, max_subseq(n // 10, t))
def add_chars(w1, w2):
    """
    note:本题思路:找到第一个字母后,将删去了第一个字母的w1和w2的一部分向下传递,实现递归
    >>> add_chars("owl", "howl")
    'h'
    >>> add_chars("want", "wanton")
    'on'
    >>> add_chars("rat", "radiate")
    'diae'
    >>> add_chars("a", "prepare")
    'prepre'
    >>> add_chars("resin", "recursion")
    'curo'
    >>> add_chars("fin", "effusion")
    'efuso'
    >>> add_chars("coy", "cacophony")
    'acphon'
    >>> from construct_check import check
    >>> # ban iteration and sets
    >>> check(LAB_SOURCE_FILE, 'add_chars',
    ...       ['For', 'While', 'Set', 'SetComp']) # Must use recursion
    True
    """
    """def check(a1, l2):
        if a1 == l2[0]:
            return 0
        else:
            return 1 + check(a1, l2[1:])
    if w1 == '':
        return w2
    else:
        return w2[:check(w1[0], w2)] + add_chars(w1[1:], w2[check(w1[0], w2) + 1:])"""
    if w1=='':
        return w2
    #两种情况:第一位是否相等
    elif w1[0]!=w2[0]:
        return w2[0]+add_chars(w1,w2[1:])
    else:
        return add_chars(w1[1:],w2[1:])



