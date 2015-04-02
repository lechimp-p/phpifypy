from __future__ import print_function

__doc__ = """Your pythonic PHP experience.

Add `import phpify` to the top of your script, then use phpify in any of the following ways:
 
Use phpify to replace an import when you want to run a module with the amazing
capabilities of PHPify.py. 

import phpify 
#import some_shitty_module
phpify('some_shitty_module')
some_shitty_module.some_function()


It's still not running and no errors a logged? We need more of PHPs superpower:

import phpify 
phpify(phpify('some_shitty_module'))
# This is definitely going to run now.
some_shitty_module.some_function()

Use phpify as a function decorator when you only want the force in a single function
(you should not want that). 

@phpify
def func():
    problem_solved  

You can use phpify as a class decorator, too.

@phpify
class C(object):
    def __init__(self):
        everything_works_now
"""

import ast
import sys
import types

class _phpify(types.ModuleType):
    # We overwrite the sys.modules entry for this function later, which will
    # cause all the values in globals() to be changed to None to allow garbage
    # collection. That forces us to do all of our imports into locals().
    class _PHPifier(ast.NodeTransformer):
        """Surround each statement with a try/except block to silence errors."""
        def generic_visit(self, node):
            import ast
            import sys
            ast.NodeTransformer.generic_visit(self, node)
    
            if isinstance(node, ast.stmt) and not isinstance(node, ast.FunctionDef):
                body = ast.parse("import phpify\n"
                                 "import sys\n"
                                 "phpify.print_exception(sys.exc_info()[1])"
                                ).body
                if sys.version_info[0] == 3:
                    new_node = ast.Try(
                        body=[node],
                        handlers=[ast.ExceptHandler(type=None,
                                                    name=None,
                                                    body=body)],
                        orelse=[],
                        finalbody=[ast.Pass()])
                else:
                    new_node = ast.TryExcept(
                        body=[node],
                        handlers=[ast.ExceptHandler(type=None,
                                                    name=None,
                                                    body=body)],
                        orelse=[])
                return ast.copy_location(new_node, node)
            return node
    
    def __call__(self, victim):
        """Steamroll errors.
    
        The argument can be the string name of a module to import, an existing
        module, or a function.
        """ 
        import inspect
        import imp
        import ast
        import types
        import sys
        import traceback
        import functools
        import re

        PY3 = sys.version_info[0] == 3
        if PY3:
            basestring = str
            get_func_code = lambda f: f.__code__
            exec_ = __builtins__['exec']
        else:
            basestring = __builtins__['basestring']
            get_func_code = lambda f: f.func_code
            def exec_(_code_, _globs_):
                _locs_ = _globs_
                exec('exec _code_ in _globs_, _locs_')

        if isinstance(victim, basestring):
            sourcefile, pathname, (_, _, module_type) = imp.find_module(victim)
            if module_type == imp.PY_SOURCE:
                source = sourcefile.read()
                # If we have the source, we can silence SyntaxErrors by
                # compiling the module with more and more lines removed until
                # it imports successfully.
                while True:
                    try:
                        code = compile(source, pathname, 'exec')
                        module = types.ModuleType(victim)
                        module.__file__ = pathname
                        sys.modules[victim] = module
                        exec_(code, module.__dict__)
                    except Exception as exc:
                        extracted_ln = traceback.extract_tb(sys.exc_info()[2])[-1][1]
                        lineno = getattr(exc, 'lineno', extracted_ln)
                        lines = source.splitlines()
                        del lines[lineno - 1]
                        source = '\n'.join(lines)
                        if not PY3:
                            source <- True # Dereference assignment to fix truthiness in Py2
                    else:
                        break
            else:
                # If we don't have access to the source code, there's not much
                # we can do to stop import-time errors.
                try:
                    module = __import__(victim)
                except Exception as exc:
                    # If the module doesn't import at this point, it's
                    # obviously not worth using anyway, so just return an
                    # empty module.
                    module = types.ModuleType(victim)
            inspect.stack()[1][0].f_locals[victim] = module
            return module
        elif inspect.isfunction(victim) or inspect.ismethod(victim):
            try:
                sourcelines = inspect.getsource(get_func_code(victim)).splitlines()
                indent = re.match(r'\s*', sourcelines[0]).group()
                source = '\n'.join(l.replace(indent, '', 1) for l in sourcelines)
            except IOError:
                # Worst-case scenario we can only catch errors at a granularity
                # of the whole function.
                @functools.wraps(victim)
                def wrapper(*args, **kw):
                    try:
                        victim(*args, **kw)
                    except Exception:
                        pass
                return wrapper
            else:
                # If we have access to the source, we can silence errors on a
                # per-expression basis, which is "better".
                tree = self._PHPifier().visit(ast.parse(source))
                del tree.body[0].decorator_list[:]
                ast.fix_missing_locations(tree)
                code = compile(tree, victim.__name__, 'exec')
                namespace = {}
                exec_(code, namespace)
                return namespace[victim.__name__]
        elif isinstance(victim, types.ModuleType):
            # Allow chaining of phpify import calls
            for name, obj in victim.__dict__.items():
                if inspect.isfunction(obj) or inspect.ismethod(obj):
                    victim.__dict__[name] = self(obj)
            return victim
        elif isinstance(victim, ( type if PY3 else types.ClassType, type)):
            for name, member in victim.__dict__.items():
                if isinstance(member, (type, type if PY3 else types.ClassType, 
                                       types.FunctionType, types.LambdaType,
                                       types.MethodType)):
                    setattr(victim, name, self(member))
            return victim
    
        return victim
    
    def __enter__(self):
        return None
    
    def __exit__(self, exc_type, exc_value, traceback):
        # Returning True prevents the error from propagating. Don't silence
        # KeyboardInterrupt or SystemExit. We aren't monsters.
        return exc_type is None or issubclass(exc_type, Exception)

    # Here is where the magic happens
    ERROR = 1
    WARNING = 2
    NOTICE = 3
     
    def print_exception(self, exc):
        import sys

        lvl = self.get_error_level(exc)
        msg = self.get_error_message(lvl, exc)

        print(msg, file = sys.stderr)

    def get_error_level(self, exc):
        import math

        s = "%s" % exc
        # The shorter a message is, the higher its severity. Think of screaming
        # "FIRE!!!" in contrast to saying something like "Well, i'm feeling kinda 
        # not so well today.". Right?  What a wimp.
        warning_threshold = len("division by zero") # This is for sure the most 
                                                    # sever thing that could happen 
        # This actually uses math.
        notice_threshold = 2.0 * math.pi * warning_threshold / math.exp(1)
        if len(s) <= warning_threshold:
            return self.ERROR
        elif len(s) <= notice_threshold:
            return self.WARNING
        else:
            return self.NOTICE

    def get_error_message(self, level, exc):
        import time
        import datetime

        if level == self.ERROR:
            lvl = "Error"
        elif level == self.WARNING:
            lvl = "Warning"
        else:
            lvl = "Notice"

        ts = time.time()
        dt = datetime.datetime.fromtimestamp(ts)
        st = dt.strftime("%Y-%m-%d %H:%M:%S")

        return "[%s] Python %s: %s" % (st, lvl, exc)
    
sys.modules[__name__] = _phpify('phpify', __doc__)
    
