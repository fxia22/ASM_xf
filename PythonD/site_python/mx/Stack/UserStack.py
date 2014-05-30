import string

class UserStack:

    def __init__(self):

        self.stack = ()

    def push(self,x):

        self.stack = (x,self.stack)

    def pop(self):

        x, self.stack = self.stack
        return x

    def not_empty(self):

        return len(self.stack) != 0

    def top(self):

        return self.stack[0]

    def __len__(self):

        i = 0
        s = self.stack
        while len(s) != 0:
            s = s[1]
            i = i + 1
        return i

    def __repr__(self):

        l = []
        s = self.stack
        while len(s) != 0:
            l.append(repr(s[0]))
            s = s[1]
        return '<UserStack [%s]>' % string.join(l,', ')

    def __str__(self):

        l = []
        s = self.stack
        while len(s) != 0:
            l.append(s[0])
            s = s[1]
        return 's' + repr(l)
