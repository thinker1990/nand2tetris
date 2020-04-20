from parse_tree import *


def to_xml(parsed):
    return f_class(parsed)


def f_class(jack_class: JackClass):
    tags = [
        '<class>',
        f'{keyword("class")}',
        f'{identifier(jack_class.name())}',
        f'{symbol("{")}',
        f'{f_class_vars(jack_class.variables())}',
        f'{f_routines(jack_class.routines())}',
        f'{symbol("}")}',
        '</class>'
    ]
    return assemble(tags)


def f_class_vars(variables):
    varis = map(f_class_var, variables)
    return assemble(varis)


def f_routines(routines):
    routs = map(f_routine, routines)
    return assemble(routs)


def f_class_var(variable: ClassVariable):
    tags = [
        '<classVarDec>',
        f'{keyword(variable.modifier())}',
        f'{f_var_type(variable.v_type())}',
        f'{f_var_names(variable.names())}',
        f'{symbol(";")}',
        '</classVarDec>'
    ]
    return assemble(tags)


def f_routine(routine: Subroutine):
    tags = [
        '<subroutineDec>',
        f'{keyword(routine.modifier())}',
        f'{f_var_type(routine.return_type())}',
        f'{identifier(routine.name())}',
        f'{symbol("(")}',
        f'{f_parameters(routine.parameters())}',
        f'{symbol(")")}',
        f'{f_routine_body(routine.body())}',
        '</subroutineDec>'
    ]
    return assemble(tags)


def f_var_type(v_type):
    if v_type in ('int', 'char', 'boolean', 'void'):
        return keyword(v_type)
    else:
        return identifier(v_type)


def f_parameters(params):
    plist = map(f_parameter, params)
    combinator = f'\n{symbol(",")}\n'
    tags = [
        '<parameterList>',
        f'{assemble(plist, combinator)}',
        '</parameterList>'
    ]
    return assemble(tags)


def f_parameter(param: Parameter):
    return (
        f'{f_var_type(param.param_type())}\n' +
        f'{identifier(param.name())}'
    )


def f_routine_body(body: RoutineBody):
    tags = [
        '<subroutineBody>',
        f'{symbol("{")}',
        f'{f_local_vars(body.local_variables())}',
        f'{f_statements(body.statements())}',
        f'{symbol("}")}',
        '</subroutineBody>'
    ]
    return assemble(tags)


def f_local_vars(variables):
    varis = map(f_local_var, variables)
    return assemble(varis)


def f_local_var(variable: LocalVariable):
    tags = [
        '<varDec>',
        f'{keyword("var")}',
        f'{f_var_type(variable.v_type())}',
        f'{f_var_names(variable.names())}',
        f'{symbol(";")}',
        '</varDec>'
    ]
    return assemble(tags)


def f_var_names(names):
    nlist = map(f_var_name, names)
    combinator = f'\n{symbol(",")}\n'
    return assemble(nlist, combinator)


def f_var_name(name):
    return f'{identifier(name)}'


def f_statements(statements):
    slist = map(f_statement, statements)
    return (
        '<statements>\n' +
        f'{assemble(slist)}\n' +
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
    tags = [
        '<letStatement>',
        f'{keyword("let")}',
        f'{f_let_target(statement.target())}',
        f'{symbol("=")}',
        f'{f_expression(statement.value())}',
        f'{symbol(";")}',
        '</letStatement>'
    ]
    return assemble(tags)


def f_if(statement: IfStatement):
    tags = [
        '<ifStatement>',
        f'{keyword("if")}',
        f'{f_exp_in_parenthesis(statement.condition())}',
        f'{symbol("{")}',
        f'{f_statements(statement.consequent())}',
        f'{symbol("}")}',
        f'{f_if_else(statement.alternative())}',
        '</ifStatement>'
    ]
    return assemble(tags)


def f_while(statement: WhileStatement):
    tags = [
        '<whileStatement>',
        f'{keyword("while")}',
        f'{f_exp_in_parenthesis(statement.test())}',
        f'{symbol("{")}',
        f'{f_statements(statement.loop_body())}',
        f'{symbol("}")}',
        '</whileStatement>'
    ]
    return assemble(tags)


def f_do(statement: DoStatement):
    tags = [
        '<doStatement>',
        f'{keyword("do")}',
        f'{f_routine_call(statement.routine_call())}',
        f'{symbol(";")}',
        '</doStatement>'
    ]
    return assemble(tags)


def f_return(statement: ReturnStatement):
    tags = [
        '<returnStatement>',
        f'{keyword("return")}',
        f'{f_expression(statement.value())}',
        f'{symbol(";")}',
        '</returnStatement>'
    ]
    return assemble(tags)


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
        return (
            f'{keyword("else")}\n' +
            f'{symbol("{")}\n' +
            f'{f_statements(statements)}\n' +
            f'{symbol("}")}'
        )


def f_routine_call(call):
    if isinstance(call, InClassCall):
        return f_inclass_call(call)
    else:
        return f_exclass_call(call)


def f_inclass_call(call: InClassCall):
    tags = [
        f'{identifier(call.routine())}',
        f'{symbol("(")}',
        f'{f_arguments(call.arguments())}',
        f'{symbol(")")}'
    ]
    return assemble(tags)


def f_exclass_call(call: ExClassCall):
    tags = [
        f'{identifier(call.target())}',
        f'{symbol(".")}',
        f'{identifier(call.routine())}',
        f'{symbol("(")}',
        f'{f_arguments(call.arguments())}',
        f'{symbol(")")}'
    ]
    return assemble(tags)


def f_arguments(args):
    alist = map(f_expression, args)
    combinator = f'\n{symbol(",")}\n'
    tags = [
        '<expressionList>',
        f'{assemble(alist, combinator)}',
        '</expressionList>'
    ]
    return assemble(tags)


def f_variable(variable: Variable):
    return f'{identifier(variable.name())}'


def f_array_entry(entry: ArrayEntry):
    tags = [
        f'{identifier(entry.name())}',
        f'{symbol("[")}',
        f'{f_expression(entry.index())}',
        f'{symbol("]")}'
    ]
    return assemble(tags)


def f_expression(exp: Expression):
    if not exp:
        return ''
    elist = map(f_op_term, exp.content())
    tags = [
        '<expression>',
        f'{assemble(elist)}',
        '</expression>'
    ]
    return assemble(tags)


def f_op_term(item):
    if isinstance(item, Operator):
        return f_op(item)
    else:
        return f_term(item)


def f_op(op: Operator):
    return f'{symbol(op.value())}'


def f_term(term):
    if isinstance(term, IntegerConstant):
        seg = f_int(term)
    elif isinstance(term, StringConstant):
        seg = f_string(term)
    elif isinstance(term, KeywordConstant):
        seg = f'{keyword(term.value())}'
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
    return (
        f'{symbol("(")}\n' +
        f'{f_expression(term)}\n' +
        f'{symbol(")")}'
    )


def f_unary(term: UnaryTerm):
    return (
        f'{symbol(term.operator())}\n' +
        f'{f_term(term.term())}'
    )


def symbol(token):
    return f'<symbol> {encode(token)} </symbol>'


def keyword(token):
    return f'<keyword> {token} </keyword>'


def identifier(token):
    return f'<identifier> {token} </identifier>'


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
