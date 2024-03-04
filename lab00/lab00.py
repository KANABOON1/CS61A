
def prime_factors(n):
    """求N的最小因数prime"""
    while n>1:
        k=first_prime(n)
        n//=k
        print(k)
def first_prime(n):
    i=2
    while n%i!=0:
        i+=1
    return i

prime_factors(12)       

