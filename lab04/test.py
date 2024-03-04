def get_length(n):
    if n // 10 == 0:
        return 1
    else:
        return 1 + get_length(n // 10)
def get_max2(n, width):
    """找到n的从1号位开始的至length的最大数"""
    max, length,counter = n // (10**(get_length(n)-1)), get_length(n),0
    while n//10:
        counter+=1
        if counter > width:
            break
        if n // (10 ** (length - counter)) > max:
            max = n // (10 ** (length - counter))
        n%=10 ** (length - counter)
    return max
#print(get_max2(12345,4))
def add_chars(w1, w2):
    def check(a1,l2):
        if a1==l2[0]:
            return 0
        else:
            return 1+check(a1,l2[1:])
    if w1=='':
        return w2
    else:
        return w2[:check(w1[0],w2)]+add_chars(w1[1:],w2[check(w1[0],w2)+1:])

def max_subseq(n, t):
    if t == 0: # base case 1
        return 0
    elif n < 10:# base case 2
        return n
    else:#在a(n-1)返回正确的情况下仅有两种情况:1.max_subseq(n//10,t-1)*10+n%10;2.max_subseq(n//10,t)
        return max(max_subseq(n // 10, t - 1) * 10 + n % 10, max_subseq(n // 10, t))
