class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.statement())
        return statements

    def statement(self):
        print(f"Token atual: {self.tokens[self.current_token_index]}")
        if self.peek() == 'KW_INT' or self.peek() == 'KW_STRING' or self.peek() == 'KW_BOOL':
            self.consume('KW_INT')
            name_token = self.consume('IDENT', "Expect variable name.")
            if self.peek() == 'EQUAL':
                self.consume('EQUAL', "Expect '=' after variable name.")
                if self.peek() == 'OPEN_BRACKET':
                    elements = self.array_elements()
                    self.consume('CLOSE_BRACKET', "Expect ']' after array elements.")
                    return {'type': 'ARRAY_DECLARATION', 'element_type': self.previous(), 'name': name_token, 'elements': elements}
                else:
                    expression = self.expression()
                    return {'type': 'VARIABLE_DECLARATION', 'var_type': self.previous(), 'name': name_token, 'value': expression}
            else:
                raise SyntaxError(f"Expect '=' after variable name. Got {self.peek()} instead.")
        elif self.peek() == 'KW_WHILE':
            return self.while_statement()
        elif self.peek() == 'KW_IF':
            return self.if_statement()
        elif self.peek() == 'KW_OUTPUT':
            return self.output_statement()
        elif self.peek() == 'IDENT':
            return self.assignment_or_function_call()
        raise SyntaxError(f"Unexpected token: {self.peek()}")

    def variable_declaration(self):
        type_token = self.previous()
        name_token = self.consume('IDENT', "Expect variable name.")
        self.consume('EQUAL', "Expect '=' after variable name.")
        if self.peek() == 'OPEN_BRACKET':
            elements = self.array_elements()
            self.consume('CLOSE_BRACKET', "Expect ']' after array elements.")
            return {'type': 'ARRAY_DECLARATION', 'element_type': type_token, 'name': name_token, 'elements': elements}
        else:
            expression = self.expression()
            return {'type': 'VARIABLE_DECLARATION', 'var_type': type_token, 'name': name_token, 'value': expression}

    def array_elements(self):
        elements = []
        if not self.check('CLOSE_BRACKET'):
            elements.append(self.expression())
            while self.peek() == 'COMMA':
                self.consume('COMMA')
                elements.append(self.expression())
        return elements

    def while_statement(self):
        if self.peek() == 'KW_WHILE':
            self.consume('KW_WHILE')
            condition = self.expression()
            self.consume('COLON', "Expect ':' after while condition")
            body = self.block()
            return {'type': 'WHILE', 'condition': condition, 'body': body}
        raise SyntaxError(f"Unexpected token: {self.peek()}")

    def if_statement(self):
        if self.peek() == 'KW_IF':
            self.consume('KW_IF')
            condition = self.expression()
            self.consume('COLON', "Expect ':' after if condition")
            then_branch = self.block()
            else_branch = None
            if self.peek() == 'KW_ELSE':
                self.consume('KW_ELSE')
                self.consume('COLON', "Expect ':' after 'endBugCheck'")
                else_branch = self.block()
            return {'type': 'IF', 'condition': condition, 'then_branch': then_branch, 'else_branch': else_branch}
        raise SyntaxError(f"Unexpected token: {self.peek()}")

    def output_statement(self):
        if self.peek() == 'KW_OUTPUT':
            self.consume('KW_OUTPUT')
            self.consume('OPEN_PARENTHESIS', "Expect '(' after 'outBug'")
            expression = self.expression()
            self.consume('CLOSE_PARENTHESIS', "Expect ')' after expression")
            return {'type': 'OUTPUT', 'expression': expression}
        raise SyntaxError(f"Unexpected token: {self.peek()}")

    def assignment_or_function_call(self):
        if self.peek() == 'IDENT':
            name = self.consume('IDENT')
            if self.peek() == 'EQUAL':
                value = self.expression()
                return {'type': 'ASSIGNMENT', 'name': name, 'value': value}
            elif self.peek() == 'OPEN_PARENTHESIS':
                return self.finish_function_call(name)
            else:
                return {'type': 'VARIABLE', 'name': name}
        raise SyntaxError(f"Unexpected token: {self.peek()}")

    def finish_function_call(self, name):
        if self.peek() == 'OPEN_PARENTHESIS':
            self.consume('OPEN_PARENTHESIS')
            arguments = []
            if not self.check('CLOSE_PARENTHESIS'):
                arguments.append(self.expression())
                while self.peek() == 'COMMA':
                    self.consume('COMMA')
                    arguments.append(self.expression())
            self.consume('CLOSE_PARENTHESIS', "Expect ')' after arguments")
            return {'type': 'FUNCTION_CALL', 'name': name, 'arguments': arguments}
        raise SyntaxError(f"Unexpected token: {self.peek()}")

    def block(self):
        statements = []
        while not self.check('KW_BREAK') and not self.is_at_end():
            statements.append(self.statement())
        if self.check('KW_BREAK'):
            self.consume('KW_BREAK', "Expect 'flyAway' at end of block")
        return statements

    def expression(self):
        return self.binary_operation()

    def binary_operation(self):
        left = self.primary()
        while self.peek() == 'ADD_OPERATOR' or self.peek() == 'SUB_OPERATOR' or self.peek() == 'GREATER_THAN' or self.peek() == 'LESS_THAN':
            operator = self.consume(self.peek())
            right = self.primary()
            left = {'type': 'BINARY_OP', 'left': left, 'operator': operator, 'right': right}
        return left

    def primary(self):
        if self.peek() == 'NUMBER':
            return {'type': 'NUMBER', 'value': self.consume('NUMBER').split()}
        if self.peek() == 'IDENT':
            return {'type': 'VARIABLE', 'name': self.consume('IDENT').split()}
        if self.peek() == 'KW_TRUE' or self.peek() == 'KW_FALSE':
            return {'type': 'BOOLEAN', 'value': self.consume(self.peek())}
        if self.peek() == 'KW_INT' or self.peek() == 'KW_STRING' or self.peek() == 'KW_BOOL':
            return {'type': 'TYPE', 'value': self.consume(self.peek())}
        if self.peek() == 'OPEN_PARENTHESIS':
            self.consume('OPEN_PARENTHESIS')
            expr = self.expression()
            self.consume('CLOSE_PARENTHESIS', "Expect ')' after expression.")
            return expr
        if self.peek() == 'KW_ADDITION':
            return self.function_call('KW_ADDITION')
        raise SyntaxError(f"Unexpected token: {self.peek()}")

    def function_call(self, function_name):
        if self.peek() == 'OPEN_PARENTHESIS':
            self.consume('OPEN_PARENTHESIS')
            arguments = []
            if not self.check('CLOSE_PARENTHESIS'):
                arguments.append(self.expression())
                while self.peek() == 'COMMA':
                    self.consume('COMMA')
                    arguments.append(self.expression())
            self.consume('CLOSE_PARENTHESIS', f"Expect ')' after {function_name} arguments")
            return {'type': 'FUNCTION_CALL', 'name': function_name, 'arguments': arguments}
        raise SyntaxError(f"Unexpected token: {self.peek()}")

    def consume(self, type, message=None):
        if self.check(type):
            self.advance()
            return self.previous()
        raise SyntaxError(f"{message} Got {self.peek()} instead.")

    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek() == type

    def advance(self):
        if not self.is_at_end():
            self.current_token_index += 1

    def is_at_end(self):
        return self.current_token_index >= len(self.tokens)

    def peek(self):
        return self.tokens[self.current_token_index]

    def previous(self):
        return self.tokens[self.current_token_index - 1]