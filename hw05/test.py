def is_bst(t):
    root_label=t.label
    if t.is_leaf():
        return True
    else:
        if len(t.branches) == 1:
            return is_bst(t.branches[0])
        elif len(t.branches) == 2:
            left_branch, right_branch = t.branches[0], t.branches[1]
            if left_branch.label <= root_label and right_branch.label >= root_label:
                return is_bst(left_branch) and is_bst(right_branch)
            else:
                return False
        else:
            return False

class Tree:
    def __init__(self, label, branches=[]):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = list(branches)

    def is_leaf(self):
        return not self.branches

    def map(self, fn):
        self.label = fn(self.label)
        for b in self.branches:
            b.map(fn)

    def __contains__(self, e):
        if self.label == e:
            return True
        for b in self.branches:
            if e in b:
                return True
        return False

    def __repr__(self):
        if self.branches:
            branch_str = ', ' + repr(self.branches)
        else:
            branch_str = ''
        return 'Tree({0}{1})'.format(self.label, branch_str)

    def __str__(self):
        def print_tree(t, indent=0):
            tree_str = '  ' * indent + str(t.label) + "\n"
            for b in t.branches:
                tree_str += print_tree(b, indent + 1)
            return tree_str
        return print_tree(self).rstrip()


t2 = Tree(8, [Tree(2, [Tree(9), Tree(1)]), Tree(3, [Tree(6)]), Tree(5)])
print(is_bst(t2))