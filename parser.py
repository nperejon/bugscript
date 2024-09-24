class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.is_at_end():
            stmt = self.declaration()
            if stmt:
                statements.append(stmt)
        return statements

    def declaration(self):
        try:
            if self.match('KW_INT', 'KW_BOOL', 'KW_STRING'):
                return self.var_declaration()
            return self.statement()
        except SyntaxError as error:
            self.synchronize()
            return None

    def var_declaration(self):
        type_token = self.previous()
        name = self.consume('IDENT', "Expect variable name.")
        
        initializer = None
        if self.match('EQUAL'):
            initializer = self.expression()
        
        self.consume('NEWLINE', "Expect newline after variable declaration.")
        return {'type': 'VAR_DECLARATION', 'var_type': type_token, 'name': name, 'initializer': initializer}

    def statement(self):
        if self.match('KW_WHILE'):
            return self.while_statement()
        if self.match('KW_IF'):
            return self.if_statement()
        if self.match('KW_OUTPUT'):
            return self.output_statement()
        if self.match('KW_BREAK'):
            return self.break_statement()
        if self.check('IDENT'):
            return self.assignment_statement()
        return self.expression_statement()

    def while_statement(self):
        condition = self.expression()
        self.consume('COLON', "Expect ':' after while condition.")
        self.consume('NEWLINE', "Expect newline after ':'.")
        
        body = []
        while not self.check('KW_BREAK') and not self.is_at_end():
            stmt = self.statement()
            if stmt:
                body.append(stmt)
        
        self.consume('KW_BREAK', "Expect 'flyAway' to end while loop.")
        self.consume('NEWLINE', "Expect newline after 'flyAway'.")
        
        return {'type': 'WHILE', 'condition': condition, 'body': body}

    def if_statement(self):
        condition = self.expression()
        self.consume('COLON', "Expect ':' after if condition.")
        self.consume('NEWLINE', "Expect newline after ':'.")
        
        then_branch = []
        while not self.check('KW_ELSE') and not self.is_at_end():
            stmt = self.statement()
            if stmt:
                then_branch.append(stmt)
        
        else_branch = None
        if self.match('KW_ELSE'):
            self.consume('COLON', "Expect ':' after 'endBugCheck'.")
            self.consume('NEWLINE', "Expect newline after ':'.")
            else_branch = []
            while not self.check('KW_IF') and not self.check('KW_WHILE') and not self.is_at_end():
                stmt = self.statement()
                if stmt:
                    else_branch.append(stmt)
        
        return {'type': 'IF', 'condition': condition, 'then_branch': then_branch, 'else_branch': else_branch}

    def output_statement(self):
        value = self.expression()
        self.consume('NEWLINE', "Expect newline after output statement.")
        return {'type': 'OUTPUT', 'value': value}

    def break_statement(self):
        self.consume('NEWLINE', "Expect newline after 'flyAway'.")
        return {'type': 'BREAK'}

    def assignment_statement(self):
        name = self.consume('IDENT', "Expect variable name.")
        self.consume('EQUAL', "Expect '=' after variable name.")
        value = self.expression()
        self.consume('NEWLINE', "Expect newline after assignment.")
        return {'type': 'ASSIGNMENT', 'name': name, 'value': value}

    def expression_statement(self):
        expr = self.expression()
        self.consume('NEWLINE', "Expect newline after expression.")
        return {'type': 'EXPR_STMT', 'expression': expr}

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()
        
        while self.match('EQUAL_EQUAL', 'BANG_EQUAL'):
            operator = self.previous()
            right = self.comparison()
            expr = {'type': 'BINARY', 'left': expr, 'operator': operator, 'right': right}
        
        return expr

    def comparison(self):
        expr = self.term()
        
        while self.match('GREATER_THAN', 'LESS_THAN'):
            operator = self.previous()
            right = self.term()
            expr = {'type': 'BINARY', 'left': expr, 'operator': operator, 'right': right}
        
        return expr

    def term(self):
        expr = self.factor()
        
        while self.match('ADD_OPERATOR', 'SUB_OPERATOR'):
            operator = self.previous()
            right = self.factor()
            expr = {'type': 'BINARY', 'left': expr, 'operator': operator, 'right': right}
        
        return expr

    def factor(self):
        expr = self.unary()
        
        while self.match('STAR', 'SLASH'):
            operator = self.previous()
            right = self.unary()
            expr = {'type': 'BINARY', 'left': expr, 'operator': operator, 'right': right}
        
        return expr

    def unary(self):
        if self.match('SUB_OPERATOR'):
            operator = self.previous()
            right = self.unary()
            return {'type': 'UNARY', 'operator': operator, 'right': right}
        
        return self.primary()

    def primary(self):
        if self.match('KW_FALSE'): return {'type': 'LITERAL', 'value': False}
        if self.match('KW_TRUE'): return {'type': 'LITERAL', 'value': True}
        if self.match('NUMBER'):
            return {'type': 'LITERAL', 'value': float(self.previous()[1])}
        if self.match('IDENT'):
            return {'type': 'VARIABLE', 'name': self.previous()}
        if self.match('KW_ADDITION'):
            return self.function_call()
        
        raise SyntaxError(f"Expect expression. Got {self.peek()}")

    def function_call(self):
        function = self.previous()
        arguments = []
        
        while not self.check('NEWLINE'):
            if len(arguments) > 0:
                self.consume('COMMA', "Expect ',' between arguments.")
            arguments.append(self.expression())
        
        return {'type': 'CALL', 'function': function, 'arguments': arguments}

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        raise SyntaxError(f"Error at '{self.peek()}': {message}")

    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek()[0] == type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek()[0] == 'EOF'

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous()[0] == 'NEWLINE':
                return

            if self.peek()[0] in ['KW_INT', 'KW_BOOL', 'KW_STRING', 'KW_IF', 'KW_WHILE', 'KW_BREAK', 'KW_OUTPUT']:
                return

            self.advance()