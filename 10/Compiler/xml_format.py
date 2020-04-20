from parse_tree import *


def to_xml(parsed):
    return f_class(parsed)


def f_class(jack_class: JackClass):
    return merge(
        '<class>',
        keyword('class'),
        identifier(jack_class.name()),
        symbol('{'),
        f_class_vars(jack_class.variables()),
        f_routines(jack_class.routines()),
        symbol('}'),
        '</class>'
    )


def f_class_vars(variables):
    varis = map(f_class_var, variables)
    return assemble(varis)


def f_routines(routines):
    routs = map(f_routine, routines)
    return assemble(routs)


def f_class_var(variable: ClassVariable):
    return merge(
        '<classVarDec>',
        keyword(variable.modifier()),
        f_var_type(variable.v_type()),
        f_var_names(variable.names()),
        symbol(';'),
        '</classVarDec>'
    )


def f_routine(routine: Subroutine):
    return merge(
        '<subroutineDec>',
        keyword(routine.modifier()),
        f_var_type(routine.return_type()),
        identifier(routine.name()),
        symbol('('),
        f_parameters(routine.parameters()),
        symbol(')'),
        f_routine_body(routine.body()),
        '</subroutineDec>'
    )


def f_var_type(v_type):
    if v_type in ('int', 'char', 'boolean', 'void'):
        return keyword(v_type)
    else:
        return identifier(v_type)


def f_parameters(params):
    plist = map(f_parameter, params)
    combinator = f'\n{symbol(",")}\n'
    return merge(
        '<parameterList>',
        assemble(plist, combinator),
        '</parameterList>'
    )


def f_parameter(param: Parameter):
    return merge(
        f_var_type(param.param_type()),
        identifier(param.name())
    )


def f_routine_body(body: RoutineBody):
    return merge(
        '<subroutineBody>',
        symbol('{'),
        f_local_vars(body.local_variables()),
        f_statements(body.statements()),
        symbol('}'),
        '</subroutineBody>'
    )


def f_local_vars(variables):
    varis = map(f_local_var, variables)
    return assemble(varis)


def f_local_var(variable: LocalVariable):
    return merge(
        '<varDec>',
        keyword('var'),
        f_var_type(variable.v_type()),
        f_var_names(variable.names()),
        symbol(';'),
        '</varDec>'
    )


def f_var_names(names):
    nlist = map(identifier, names)
    combinator = f'\n{symbol(",")}\n'
    return assemble(nlist, combinator)


def f_statements(statements):
    slist = map(f_statement, statements)
    return merge(
        '<statements>',
        assemble(slist),
        '</statements>'
    )


def f_statement(statement):
    if isinstance(statement, LetStatement):
        return f_let(statement)
    elif isinstance(statement, IfStatement):
        return f_if(statement)
    elif isinstance(statement, WhileStatement):
        return f_while(statement)
    elif isinstance(statement, DoStatement):
        return f_do(statement)
    elif isinstance(statement, ReturnStatement):
        return f_return(statement)
    else:
        raise Exception('Illegal statement type.')


def f_let(statement: LetStatement):
    return merge(
        '<letStatement>',
        keyword('let'),
        f_let_target(statement.target()),
        symbol('='),
        f_expression(statement.value()),
        symbol(';'),
        '</letStatement>'
    )


def f_if(statement: IfStatement):
    return merge(
        '<ifStatement>',
        keyword('if'),
        f_exp_in_parenthesis(statement.condition()),
        symbol('{'),
        f_statements(statement.consequent()),
        symbol('}'),
        f_if_else(statement.alternative()),
        '</ifStatement>'
    )


def f_while(statement: WhileStatement):
    return merge(
        '<whileStatement>',
        keyword('while'),
        f_exp_in_parenthesis(statement.test()),
        symbol('{'),
        f_statements(statement.loop_body()),
        symbol('}'),
        '</whileStatement>'
    )


def f_do(statement: DoStatement):
    return merge(
        '<doStatement>',
        keyword('do'),
        f_routine_call(statement.routine_call()),
        symbol(';'),
        '</doStatement>'
    )


def f_return(statement: ReturnStatement):
    return merge(
        '<returnStatement>',
        keyword('return'),
        f_expression(statement.value()),
        symbol(';'),
        '</returnStatement>'
    )


def f_let_target(target):
    if isinstance(target, Variable):
        return f_variable(target)
    elif isinstance(target, ArrayEntry):
        return f_array_entry(target)
    else:
        raise Exception('Illegal type.')


def f_if_else(statements):
    if not statements:
        return ''
    else:
        return merge(
            keyword('else'),
            symbol('{'),
            f_statements(statements),
            symbol('}')
        )


def f_routine_call(call):
    if isinstance(call, InClassCall):
        return f_inclass_call(call)
    else:
        return f_exclass_call(call)


def f_inclass_call(call: InClassCall):
    return merge(
        identifier(call.routine()),
        symbol('('),
        f_arguments(call.arguments()),
        symbol(')')
    )


def f_exclass_call(call: ExClassCall):
    return merge(
        identifier(call.target()),
        symbol('.'),
        identifier(call.routine()),
        symbol('('),
        f_arguments(call.arguments()),
        symbol(')')
    )


def f_arguments(args):
    alist = map(f_expression, args)
    combinator = f'\n{symbol(",")}\n'
    return merge(
        '<expressionList>',
        assemble(alist, combinator),
        '</expressionList>'
    )


def f_variable(variable: Variable):
    return identifier(variable.name())


def f_array_entry(entry: ArrayEntry):
    return merge(
        identifier(entry.name()),
        symbol('['),
        f_expression(entry.index()),
        symbol(']')
    )


def f_expression(exp: Expression):
    if not exp:
        return ''
    elist = map(f_op_term, exp.content())
    return merge(
        '<expression>',
        assemble(elist),
        '</expression>'
    )


def f_op_term(item):
    if isinstance(item, Operator):
        return f_op(item)
    else:
        return f_term(item)


def f_op(op: Operator):
    return symbol(op.value())


def f_term(term):
    if isinstance(term, IntegerConstant):
        seg = f_int(term)
    elif isinstance(term, StringConstant):
        seg = f_string(term)
    elif isinstance(term, KeywordConstant):
        seg = keyword(term.value())
    elif isinstance(term, Variable):
        seg = f_variable(term)
    elif isinstance(term, ArrayEntry):
        seg = f_array_entry(term)
    elif isinstance(term, InClassCall):
        seg = f_inclass_call(term)
    elif isinstance(term, ExClassCall):
        seg = f_exclass_call(term)
    elif isinstance(term, Expression):
        seg = f_exp_in_parenthesis(term)
    elif isinstance(term, UnaryTerm):
        seg = f_unary(term)
    else:
        raise Exception('Illegal term type.')
    return f'<term>\n{seg}\n</term>'


def f_int(term: IntegerConstant):
    return f'<integerConstant> {term.value()} </integerConstant>'


def f_string(term: StringConstant):
    return f'<stringConstant> {term.value()} </stringConstant>'


def f_exp_in_parenthesis(term: Expression):
    return merge(
        symbol('('),
        f_expression(term),
        symbol(')')
    )


def f_unary(term: UnaryTerm):
    return merge(
        symbol(term.operator()),
        f_term(term.term())
    )


def symbol(token):
    return f'<symbol> {encode(token)} </symbol>'


def keyword(token):
    return f'<keyword> {token} </keyword>'


def identifier(token):
    return f'<identifier> {token} </identifier>'


def merge(*parts):
    return assemble(parts)


def assemble(parts, combinator='\n'):
    parts = filter(lambda i: i, parts)
    return combinator.join(parts)


def encode(symbol):
    if symbol == '<':
        return '&lt;'
    elif symbol == '>':
        return '&gt;'
    elif symbol == '"':
        return '&quot;'
    elif symbol == '&':
        return '&amp;'
    else:
        return symbol
