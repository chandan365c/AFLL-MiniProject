import ply.lex as lex
import ply.yacc as yacc

# Define tokens
tokens = (
    'FOR',
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
    'INCREMENT', 'DECREMENT',
    'AND', 'OR'
)

# Reserved words
reserved = {
    'for': 'FOR',
    'true': 'NUMBER',  # Treat 'true' as a special case for the sake of this example
    'false': 'NUMBER'
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
t_AND = r'&&'
t_OR = r'\|\|'

# Identifier and reserved word handling
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Check if it's a reserved word
    return t

# Integer literal
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value) if t.value != 'true' else True  # Convert 'true' to boolean
    t.value = False if t.value == 'false' else t.value  # Convert 'false' to boolean
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
    """program : for_loop"""
    print("Program successfully parsed.")

def p_for_loop(p):
    """for_loop : FOR LPAREN initialization SEMI condition SEMI increment RPAREN LBRACE statement_block RBRACE"""
    # Now printing initialization, condition, and increment separately
    print(f"Initialization: {p[3]}")
    print(f"Condition: {p[5]}")
    print(f"Increment: {p[7]}")
    print("Parsed a for loop.")

def p_initialization(p):
    """initialization : ID ASSIGN expression"""
    p[0] = f"{p[1]} = {p[3]}"  # initialization

def p_condition(p):
    """condition : expression relop expression
                 | expression AND expression
                 | expression OR expression
                 | NUMBER
                 | ID"""
    if len(p) == 4:
        p[0] = f"{p[1]} {p[2]} {p[3]}"  # handle relational operators
    elif len(p) == 3:
        p[0] = f"{p[1]} {p[2]}"  # handle logical operators
    else:
        p[0] = str(p[1])  # For just a number or ID condition

def p_increment(p):
    """increment : ID INCREMENT
                 | ID DECREMENT
                 | expression"""
    if len(p) == 3:  # Handling the increment and decrement expressions (i++ or i--)
        p[0] = f"{p[1]} {p[2]}"
    elif len(p) == 2:  # Handling compound expressions like (i = i + 1)
        p[0] = f"{p[1]} = {p[2]}"

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
