# AFLL-MiniProject

## Simple Language Parser with Variable Declarations and Control Flow
This project implements a simple lexer and parser for a small programming language that supports variable declarations, while and for loops, if statements, and integer array declarations. The lexer tokenizes input, while the parser processes variable declarations, assignments, and various control flow constructs. Syntax errors are caught and reported to the user.

## Features
**Lexer:** Tokenizes input based on predefined rules for identifiers, integer literals, keywords (like int, while, for, if), assignment (=), commas, semicolons, and parentheses.

**Parser:** Parses variable declarations, control flow statements (while, for, if), and array declarations.

**Error Handling:** Prints error messages for illegal characters or syntax errors.

## Supported Constructs
**Variable Declarations:**
- Supports declarations with or without initialization (e.g., int x;, int x = 10;).
- Allows multiple variables in one declaration (e.g., int x, y = 5;).

**Control Flow Statements:**
- **While Loops:** Supports while loops with conditions (e.g., while (x < 10) { ... ;}).
- **For Loops:** Supports for loops with initialization, conditions, and increments (e.g., for (i = 0; i < 10; i++) { ... ;}).
- **If Statements:** Supports conditional statements (e.g., if (x > 0) { ... ;}).

**Array Declarations:**
- Supports declarations of integer arrays (e.g., int arr[10] = {...};).

**Error Handling:**

- Provides feedback on syntax errors or illegal characters in the input.


## Getting Started

### Prerequisites

You need Python 3.x and the ply library. To install ply, run:
```bash
pip install ply
```

### Usage
- Clone or download this repository to your local machine.
- Run the desired parser file:

```bash
python file_name.py
```

- The program will prompt you for input (Input > ). You can enter a variety of statements, including variable declarations, loops, and if statements.
- The program will parse and output the corresponding declarations and control flow structures.

### Example Test Cases:
1. **int declaration:**
    - `int x;`   `int x = 10;`   `int x,y;`   `int x, y=10;`
2. **while loop declaration:**
   - `while(x<=10){a=a+b;}`   `while(1){i++;}`   
3. **for loop declaration:**
   - `for (i = 0; i < 10; i++){ a = a + b;}`   `for(k = 0; k >= 5; k++) { j--;}`
4. **if statement:**
   - `if(x > 0){ a = 10;}`
5. **Integer array declaration:**
   - `int a[5];`   `int a[4] = {1,2,3,4};`   `int a[2], b[7];`
  

### Lexical Rules
- `int` is a reserved keyword indicating variable declarations or array types.
- Identifiers must start with a letter or underscore, followed by letters, numbers, or underscores.
- Integer literals are positive numbers (e.g., 5).
- Semicolons `;` are mandatory after declarations and initializations.
- Arrays are declared using square brackets (e.g., *int arr[10];*).
- The while loop syntax is: *while (condition) { ... ;}*.
- The for loop syntax is: *for (initialization; condition; increment/decrement) { ... ;}*.
- The if statement syntax is: *if (condition) { ... ;}*.
