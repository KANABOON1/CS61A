def group_by(s,fn):
    group={}
    for element in s:
        key=fn(element)
        if key in group:  # 字典中已有键值对
            group[key].append(element)
        else:             # 字典中没有键值对
            group[key]=[element]
    return group

def add_this_many(x,el,s):
    count=0
    for e in s:
        if e==x:
            count+=1
    for i in range(count):
        s.append(el)

def filter(iterable,fn):
    for e in iterable:
        if fn(e):
            yield e

def merge(a,b):
    next_a = next(a)
    next_b = next(b)
    while True:
        if next_a==next_b:
            yield next_a
            next_a=next(a)
            next_b=next(b)
        elif next_a<next_b:
            yield next_a
            next_a=next(a)
        else:
            yield next_b
            next_b=next(b)
def sequence(start,step):
    while True:
        yield start
        start+=step
a=sequence(2,3)
b=sequence(3,2)
result=merge(a,b)
print([next(result) for _ in range(10)])