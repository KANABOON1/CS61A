HW_SOURCE_FILE=__file__
def num_eights(x):
    if x//10==0:#base case:作为最简单的case.
        if x == 8:
            return 1
        else:
            return 0
    else:
        if x % 10 == 8:
            return 1 + num_eights(x // 10)
        else:
            return num_eights(x // 10)
def pingpong(n):
    """定义了辅助函数helper()的递归:在递归中记录变量的值"""
    def up(index,sum,adder):
        """
        从第一项开始逐步逼近第n位的算法.
        从第一项开始有利于记住adder,增加程序的效率.
        若要在递归时追踪不止一项的值,则递归helper
        """
        if index==n: #base case: 作为出口.
            return sum
        elif num_eights(index)>0 or index%8==0:
            return up(index+1,sum+adder*(-1),adder*(-1))
        else:
            return up(index + 1, sum + adder, adder)
    return up(1,1,1)

def next_largest_coin(coin):
    if coin == 1:
        return 5
    elif coin == 5:
        return 10
    elif coin == 10:
        return 25

def count_coins(total):
    def helper(change, coin):
        if change==total and coin==None:
            return 1
        elif change>total or coin==None:
            return 0
        else:
            return helper(change,next_largest_coin(coin))+helper(change+coin,coin)
    return helper(0,1)

print(count_coins(20))