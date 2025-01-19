import lldb

debug_funcs = {}

def debug_function_summary(valobj, internal_dict):
    type_name = valobj.GetTypeName().strip(' *')
    target = lldb.debugger.GetSelectedTarget()
    debug_function = debug_funcs[type_name]
    val = valobj.GetValueAsUnsigned()

    expr = '((char *(*)(void *))0x%x)((void *)0x%x)' % (debug_function, val)
    result = target.EvaluateExpression(expr)

    if result.IsValid():# and result.GetError().Success():
        result.SetFormat(lldb.eFormatCString)
        return result.GetValue()
    else:
        return f"<Error: Could not call {debug_function}>"

def __lldb_init_module(debugger, internal_dict):
    target = debugger.GetSelectedTarget()

    for module in target.modules:
        for symbol in module:
            func_name = symbol.name

            if '::debug' in func_name:
                type_name = func_name.split('::debug')[0]
                addr = symbol.addr.GetFileAddress()
                debug_funcs[type_name] = addr
                debugger.HandleCommand('type summary add -F formatters.debug_function_summary "%s *"' % type_name)
