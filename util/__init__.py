# coding: utf-8

"""工具,及其公共方法"""

from functools import partial, update_wrapper


def _update_method_wrapper(_wrapper, decorator):
    # _multi_decorate()'s bound_method isn't available in this scope. Cheat by
    # using it on a dummy function.
    @decorator
    def dummy(*args, **kwargs):
        pass

    update_wrapper(_wrapper, dummy)


def _multi_decorate(decorators, method):
    """
    Decorate `method` with one or more function decorators. `decorators` can be
    a single decorator or an iterable of decorators.
    """
    if hasattr(decorators, '__iter__'):
        # Apply a list/tuple of decorators if 'decorators' is one. Decorator
        # functions are applied so that the call order is the same as the
        # order in which they appear in the iterable.
        decorators = decorators[::-1]
    else:
        decorators = [decorators]

    def _wrapper(self, *args, **kwargs):
        # bound_method has the signature that 'decorator' expects i.e. no
        # 'self' argument, but it's a closure over self so it can call
        # 'func'. Also, wrap method.__get__() in a function because new
        # attributes can't be set on bound method objects, only on functions.
        bound_method = partial(method.__get__(self, type(self)))
        for dec in decorators:
            bound_method = dec(bound_method)
        return bound_method(*args, **kwargs)

    # Copy any attributes that a decorator adds to the function it decorates.
    for dec in decorators:
        _update_method_wrapper(_wrapper, dec)
    # Preserve any existing attributes of 'method', including the name.
    update_wrapper(_wrapper, method)
    return _wrapper


def add_decorator_for_public_method(decorator,
                                    except_methods=None,
                                    contain=False):
    """
    这是一个装饰器,给class中指定的多个方法添加装饰器,不包括以_开头或结尾的方法.不依赖其他库,兼容py2.
    :param decorator: 需要加的装饰器
    :param except_methods: 排除的方法列表或元祖
    :param contain: 是否包含或不包含列表中的方法
    :return: 加完装饰器后的类本身
    """
    if not isinstance(except_methods, (list, tuple)):
        except_methods = []

    def _dec(obj):
        if not isinstance(obj, type):
            return _multi_decorate(decorator, obj)
        methods = (list(filter(
            lambda m: not (m.startswith("_") or m.endswith("_"))
                      and ((m not in except_methods)
                           if (not contain) else (m in except_methods))
                      and callable(getattr(obj, m)), dir(obj))))
        for name in methods:
            if not (name and hasattr(obj, name)):
                raise ValueError(
                    "The keyword argument `name` must be the name of a method "
                    "of the decorated class: %s. Got '%s' instead." % (obj, name)
                )
            method = getattr(obj, name)
            if not callable(method):
                raise TypeError(
                    "Cannot decorate '%s' as it isn't a callable attribute of "
                    "%s (%s)." % (name, obj, method)
                )
            _wrapper = _multi_decorate(decorator, method)
            setattr(obj, name, _wrapper)
        return obj

    # Don't worry about making _dec look similar to a list/tuple as it's rather
    # meaningless.
    if not hasattr(decorator, '__iter__'):
        update_wrapper(_dec, decorator)
    # Change the name to aid debugging.
    obj = decorator if hasattr(decorator, '__name__') else decorator.__class__
    # 还原方法自己的name
    _dec.__name__ = 'add_decorator_for_public_method(%s)' % obj.__name__
    return _dec
