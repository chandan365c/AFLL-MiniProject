import ply.lex as lex
import ply.yacc as yacc

# Token definitions
tokens = (
    'INT',               # Type: int
    'IDENTIFIER',        # Variable/Array name
    'EQUALS',            # Assignment operator: =
    'INTEGER_LITERAL',   # Integer values: 10, 20, etc.
    'SEMI',              # Semicolon ;
    'COMMA',             # Comma ,
    'LBRACKET',          # Left bracket [
    'RBRACKET',          # Right bracket ]
    'LBRACE',            # Left brace {
    'RBRACE',            # Right brace }
)

# Reserved words (only 'int' for now)
reserved = {
    'int': 'INT',
}

# Regular expression rules for simple tokens
t_EQUALS = r'='
t_SEMI = r';'
t_COMMA = r','
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

# Token for IDENTIFIER (e.g., variable names or arrays)
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
    for var in p[2]:
        print(f"Declarations: {var[0]} [{var[1]}] = {var[2]}" if var[2] else f"{var[0]} [{var[1]}]")
    return


def p_var_list_single(p):
    """var_list : IDENTIFIER LBRACKET INTEGER_LITERAL RBRACKET
                | IDENTIFIER LBRACKET INTEGER_LITERAL RBRACKET EQUALS initializer"""
    if len(p) == 5:
        # Array with no initialization: e.g., int arr[10];
        p[0] = [(p[1], p[3], None)]  # No initializer
    elif len(p) == 7:
        # Array with initialization: e.g., int arr[5] = {1, 2, 3, 4, 5};
        initializer_elements = len(p[6])  # Count the number of elements in the initializer
        if initializer_elements > p[3]:
            print(f"Error: Array '{p[1]}' declared with size {p[3]} but initialized with {initializer_elements} elements.")
            p[0] = [(p[1], p[3], None)]  # Store an invalid declaration (for now)
        else:
            p[0] = [(p[1], p[3], p[6])]  # Store initializer values


def p_var_list_multiple(p):
    """var_list : var_list COMMA var_list"""
    p[0] = p[1] + p[3]  # Concatenate the two lists


def p_initializer(p):
    """initializer : LBRACE values RBRACE"""
    p[0] = p[2]  # Return a list of values inside the braces


def p_values(p):
    """values : INTEGER_LITERAL
              | values COMMA INTEGER_LITERAL"""
    if len(p) == 2:
        p[0] = [str(p[1])]
    else:
        p[0] = p[1] + [str(p[3])]  # Append new values


def p_expression(p):
    """expression : INTEGER_LITERAL"""
    p[0] = p[1]


def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

# Main loop to read input
while True:
    try:
        s = input('Input > ')
        if s.strip().lower() == 'exit':
            break
    except EOFError:
        break
    if s.strip():
        parser.parse(s)
