import types
def remainders_generator(m):

    def help_generator(i): # i表示余数
        num=1
        while True:
            if num%m==i:
                yield num

    for i in range(m):
        yield help_generator(i)

remainders_four = remainders_generator(4)
for i in range(4):
    print("First 3 natural numbers with remainder {0} when divided by 4:".format(i))
    gen = next(remainders_four)
    for _ in range(3):
        print(next(gen))

