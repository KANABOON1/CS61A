from math import sqrt
def change_abstraction(change):
    change_abstraction.changed = change

change_abstraction.changed = False
def make_city(name, lat, lon):
    """
    >>> city = make_city('Berkeley', 0, 1)
    >>> get_name(city)
    'Berkeley'
    >>> get_lat(city)
    0
    >>> get_lon(city)
    1
    """
    if change_abstraction.changed:
        return {"name" : name, "lat" : lat, "lon" : lon}
    else:
        return [name, lat, lon]

def get_name(city):
    """
    >>> city = make_city('Berkeley', 0, 1)
    >>> get_name(city)
    'Berkeley'
    """
    if change_abstraction.changed:
        return city["name"]
    else:
        return city[0]

def get_lat(city):
    """
    >>> city = make_city('Berkeley', 0, 1)
    >>> get_lat(city)
    0
    """
    if change_abstraction.changed:
        return city["lat"]
    else:
        return city[1]

def get_lon(city):
    """
    >>> city = make_city('Berkeley', 0, 1)
    >>> get_lon(city)
    1
    """
    if change_abstraction.changed:
        return city["lon"]
    else:
        return city[2]
def distance(city_a, city_b):
    """
    >>> city_a = make_city('city_a', 0, 1)
    >>> city_b = make_city('city_b', 0, 2)
    >>> distance(city_a, city_b)
    1.0
    >>> city_c = make_city('city_c', 6.5, 12)
    >>> city_d = make_city('city_d', 2.5, 15)
    >>> distance(city_c, city_d)
    5.0
    """
    lenth2=(get_lat(city_a)-get_lat(city_b))**2
    width2=(get_lon(city_a)-get_lon(city_b))**2
    return sqrt(lenth2+width2)

def riffle(deck):
    "*** YOUR CODE HERE ***"
    return [deck[(int)(index % 2 != 0) * len(deck) // 2 + index // 2] for index in range(len(deck))]

def tree(label, branches=[]):
    """Construct a tree with the given label value and a list of branches."""
    if change_abstraction.changed:
        for branch in branches:
            assert is_tree(branch), 'branches must be trees'
        return {'label': label, 'branches': list(branches)}
    else:
        for branch in branches:
            assert is_tree(branch), 'branches must be trees'
        return [label] + list(branches)
def label(tree):
    """Return the label value of a tree."""
    if change_abstraction.changed:
        return tree['label']
    else:
        return tree[0]
def branches(tree):
    """Return the list of branches of the given tree."""
    if change_abstraction.changed:
        return tree['branches']
    else:
        return tree[1:]
def is_tree(tree):
    """Returns True if the given tree is a tree, and False otherwise."""
    if change_abstraction.changed:
        if type(tree) != dict or len(tree) != 2:
            return False
        for branch in branches(tree):
            if not is_tree(branch):
                return False
        return True
    else:
        if type(tree) != list or len(tree) < 1:
            return False
        for branch in branches(tree):
            if not is_tree(branch):
                return False
        return True
def is_leaf(tree):
    """Returns True if the given tree's list of branches is empty, and False
    otherwise.
    """
    return not branches(tree)
def change_abstraction(change):
    change_abstraction.changed = change
change_abstraction.changed = False
def print_tree(t, indent=0):
    """Print a representation of this tree in which each node is
    indented by two spaces times its depth from the root.

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    """
    print('  ' * indent + str(label(t)))
    for b in branches(t):
        print_tree(b, indent + 1)
def add_trees(t1, t2):
    "*** YOUR CODE HERE ***"
    if is_leaf(t1): # base case1
        return tree(label(t1)+label(t2),branches(t2))
    elif is_leaf(t2): # base case2
        return tree(label(t1)+label(t2),branches(t1))
    else:
        len_tree=min(len(branches(t1)),len(branches(t2)))
        mul_tree=[add_trees(branches(t1)[index],branches(t2)[index]) for index in range(len_tree)]
        # note :mul_tree最后加上branches最后没有做add_trees(t1,t2)的部分.
        mul_tree+=branches(t1)[len_tree:]+branches(t2)[len_tree:]
        return tree(label(t1)+label(t2),mul_tree)
#print_tree(add_trees(tree(2, [tree(3)]), tree(2, [tree(3), tree(4)])))
#print_tree(add_trees(tree(2), tree(3, [tree(4), tree(5)])))
#print_tree(add_trees(tree(2, [tree(3, [tree(4), tree(5)])]),tree(2, [tree(3, [tree(4)]), tree(5)])))

def build_successors_table(tokens):
    """Return a dictionary: keys are words; values are lists of successors.

    >>> text = ['We', 'came', 'to', 'investigate', ',', 'catch', 'bad', 'guys', 'and', 'to', 'eat', 'pie', '.']
    >>> table = build_successors_table(text)
    >>> sorted(table)
    [',', '.', 'We', 'and', 'bad', 'came', 'catch', 'eat', 'guys', 'investigate', 'pie', 'to']
    >>> table['to']
    ['investigate', 'eat']
    >>> table['pie']
    ['.']
    >>> table['.']
    ['We']
    """
    table = {}
    prev = '.'
    for word in tokens:
        if prev not in table:
            table[prev]=[word]
        else:
            table[prev]+=[word]
        prev = word
    return table
def construct_sent(word, table):
    """Prints a random sentence starting with word, sampling from
    table.
    """
    import random
    result = ''
    while word not in ['.', '!', '?']:
        result+=word+' '
        word=random.choice(table[word])
    return result.strip() + word

