# coding: utf-8

"""api库,公共方法"""

import inspect


def call_me(frame):
    """谁调用了我"""
    # 类方法
    method_name = frame.f_code.co_name
    if method_name.startswith("<") and method_name.endswith(">"):
        try:
            # 函数 或 类的静态方法
            method_name = frame.f_code.co_names[3]
        except:
            pass
    c = frame.f_code
    clazz_name = None
    # 有参数
    if c.co_argcount > 0:
        first_arg = frame.f_locals[c.co_varnames[0]]
        if hasattr(first_arg, method_name) and getattr(first_arg,
                                                       method_name).__code__ is c:
            if inspect.isclass(first_arg):
                clazz_name = first_arg.__qualname__
            else:
                clazz_name = first_arg.__class__.__qualname__
    # 无参数
    else:
        try:
            clazz_name = frame.f_back.f_code.co_names[5]
        except:
            pass
    who = ""
    if clazz_name is None:
        who = method_name
    else:
        who = f"{clazz_name}.{method_name}"
    del frame
    return who
