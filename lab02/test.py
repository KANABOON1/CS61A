def func(n,cond):
    """建立累加的通用模板"""
    i,sum=0,0
    while i<n:
        sum,i=sum+cond(i+1),i+1
    return sum

def sum_square(n):
    """通过sum_square可仅传一个参数"""
    return func(n,condition)

condition=lambda x:x*x*x
print(sum_square(3))