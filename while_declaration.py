import ply.lex as lex
import ply.yacc as yacc

# Define tokens
tokens = (
    'WHILE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'ID',
    'NUMBER',
    'ASSIGN',
    'SEMI',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LT', 'GT', 'LE', 'GE', 'EQ', 'NE',
    'INCREMENT', 'DECREMENT'
)

# Reserved words
reserved = {
    'while': 'WHILE',
    'true': 'NUMBER'  # Treat 'true' as a special case for the sake of this example
}

# Tokenizing rules
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ASSIGN = r'='
t_SEMI = r';'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'

# Identifier and reserved word handling
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Check if it's a reserved word
    return t

# Integer literal
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value) if t.value != 'true' else True  # Convert 'true' to boolean
    return t

# Ignore whitespace and newlines
t_ignore = ' \t\n'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parsing rules
def p_program(p):
    """program : while_loop"""
    print("Program successfully parsed.")

def p_while_loop(p):
    """while_loop : WHILE LPAREN condition RPAREN LBRACE statement_block RBRACE"""
    print("Parsed a while loop.")

def p_condition(p):
    """condition : expression relop expression
                 | NUMBER
                 | ID
                 | ID INCREMENT
                 | ID DECREMENT"""
    print(f"Condition: {p[1]} {p[2]} {p[3]}" if len(p) == 4 else f"Condition: {p[1]}")

def p_relop(p):
    """relop : LT
             | GT
             | LE
             | GE
             | EQ
             | NE"""
    p[0] = p[1]

def p_expression(p):
    """expression : expression PLUS term
                  | expression MINUS term
                  | term"""
    if len(p) == 4:
        p[0] = f"({p[1]} {p[2]} {p[3]})"  # Format the expression
    else:
        p[0] = p[1]

def p_term(p):
    """term : term TIMES factor
            | term DIVIDE factor
            | factor"""
    if len(p) == 4:
        p[0] = f"({p[1]} {p[2]} {p[3]})"  # Format the term
    else:
        p[0] = p[1]

def p_factor(p):
    """factor : NUMBER
              | ID
              | LPAREN expression RPAREN
              | ID INCREMENT
              | ID DECREMENT"""
    
    if len(p) == 2:  # Simple ID or NUMBER
        p[0] = p[1]
    elif len(p) == 3:  # Increment or decrement
        p[0] = f"{p[1]}++" if p[2] == '++' else f"{p[1]}--"
    else:
        p[0] = p[1]  # Return the value directly

def p_statement_block(p):
    """statement_block : statement
                       | statement statement_block"""
    # No print statements here; just accumulate statements for future processing if needed
    pass

def p_statement(p):
    """statement : ID ASSIGN expression SEMI
                 | ID INCREMENT SEMI
                 | ID DECREMENT SEMI"""
    if len(p) == 5:
        print(f"Assignment: {p[1]} = {p[3]}")
    else:
        print(f"Increment/Decrement: {p[1]} {'++' if p[2] == '++' else '--'}")

# Error handling rule
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Test the parser
if __name__ == "__main__":
    while True:
        try:
            s = input('Input > ')

            if s.strip().lower() == 'exit':
                break
        except EOFError:
            break
        if s.strip():
            parser.parse(s)
