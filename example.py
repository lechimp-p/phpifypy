import phpify 
#import broke 
phpify(phpify('broke'))

@phpify
def broken_function():
    non_existant_variable # Let's create a NameError
    return 'Function decorator works'

@phpify
class BrokenClass(object):
    def f(self):
        self.black_hole = 1 / 0
        return 'Class decorator works'
    
print(broken_function())
print(BrokenClass().f())
broke.f()
