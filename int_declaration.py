import ply.lex as lex
import ply.yacc as yacc

# Token definitions
tokens = (
    'INT',
    'IDENTIFIER',
    'EQUALS',
    'INTEGER_LITERAL',
    'SEMI',
    'COMMA',
)

# Regular expression rules for simple tokens
t_EQUALS = r'='
t_SEMI = r';'
t_COMMA = r','

# Reserved words
reserved = {
    'int': 'INT'
}

# Token for IDENTIFIER (e.g., variable names)
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check for reserved words
    return t

# Integer literal
def t_INTEGER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Newline rule to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parsing rules
def p_declaration(p):
    """declaration : INT var_list SEMI"""
    print(f"Declarations: {', '.join(p[2])}")

def p_var_list_single(p):
    """var_list : IDENTIFIER
    | IDENTIFIER EQUALS expression"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [f"{p[1]} = {p[3]}"]
        
def p_var_list_multiple(p):
    """var_list : var_list COMMA var_list"""
    p[0] = p[1] + p[3]

def p_expression(p):
    """expression : INTEGER_LITERAL"""
    p[0] = p[1]

def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()

while True:
    try:
        s = input('Input > ')
        if s.strip().lower() == 'exit':
            break
    except EOFError:
        break
    if s.strip():
        parser.parse(s)