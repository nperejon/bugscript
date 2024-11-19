from source.symbol_table import SymbolTable
from source.semantic_error import SemanticError

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, ast):
        for statement in ast:
            self.visit(statement)

    def visit(self, node):
        node_type = node.get('type')

        if node_type == 'VAR_DECLARATION':
            self.handle_var_declaration(node)
        elif node_type == 'ASSIGNMENT':
            self.handle_assignment(node)
        elif node_type == 'IF':
            self.handle_if(node)
        elif node_type == 'WHILE':
            self.handle_while(node)
        elif node_type == 'OUTPUT':
            self.handle_output(node)
        elif node_type == 'EXPR_STMT':
            self.evaluate_expression(node['expression'])

    def handle_var_declaration(self, node):
        var_name = node['name'][1]
        var_type = node['var_type'][0]
        self.symbol_table.declare(var_name, var_type)

        if node['initializer'] is not None:
            initializer_type = self.evaluate_expression(node['initializer'])
            self.symbol_table.assign(var_name, initializer_type)
    
    def handle_assignment(self, node):
        var_name = node['name'][1]
        self.symbol_table.check_declaration(var_name)
        value_type = self.evaluate_expression(node['value'])
        self.symbol_table.assign(var_name, value_type)

    def handle_if(self, node):
        condition_type = self.evaluate_expression(node['condition'])
        self.symbol_table.check_condition_type(condition_type, node.get('type'))

        for stmt in node['then_branch']:
            self.visit(stmt)
        if node.get('else_branch'):
            for stmt in node['else_branch']:
                self.visit(stmt)

    def handle_while(self, node):
        condition_type = self.evaluate_expression(node['condition'])
        self.symbol_table.check_condition_type(condition_type, node.get('type'))
        for stmt in node['body']:
            self.visit(stmt)

    def handle_output(self, node):
        self.evaluate_expression(node['value'])

    def call_function(self, function_name, arguments):
        if function_name[0] in ['KW_ADDITION', 'KW_SUBTRACTION', 'KW_MULTIPLY', 'KW_DIVISION']:
            arg_types = []

            for arg in arguments:
                if arg['type'] == 'LITERAL':
                    value = arg['value']
                    if isinstance(value, int):
                        arg_types.append('KW_INT')
                    elif isinstance(value, float):
                        arg_types.append('KW_FLOAT')
                    elif isinstance(value, bool):
                        arg_types.append('KW_BOOL')
                    elif isinstance(value, tuple) and value[0] == 'TEXT':
                        arg_types.append('KW_STRING')
                    else:
                        raise TypeError(f"Invalid literal type: {value}")
                elif arg['type'] == 'VARIABLE':
                    var_name = arg['name'][1]
                    value = self.symbol_table.get_variable_value(var_name)
                    arg_types.append(value)

            return self.symbol_table.check_numeric_operation(arg_types[0], arg_types[1])

        raise Exception(f"Function '{function_name[1]}' not defined.")

    def evaluate_expression(self, expr):
        expr_type = expr.get('type')

        if expr_type == 'LITERAL':
            value = expr['value']
            if isinstance(value, tuple) and value[0] == 'TEXT':
                return 'KW_STRING'
            elif isinstance(value, bool):
                return 'KW_BOOL'
            elif isinstance(value, int):
                return 'KW_INT'
            elif isinstance(value, float):
                return 'KW_FLOAT'
        elif expr_type == 'VARIABLE':
            var_name = expr['name'][1]
            return self.symbol_table.get_variable_value(var_name)
        elif expr_type == 'BINARY':
            left_type = self.evaluate_expression(expr['left'])
            right_type = self.evaluate_expression(expr['right'])
            operator = expr['operator'][1]

            if operator in ['==', '!=', '<', '>']:
                self.symbol_table.check_logic_operation(left_type, operator, right_type)
                return 'KW_BOOL'
            else:
                return self.symbol_table.check_numeric_operation(left_type, right_type)
        elif expr_type == 'CALL':
            function_name = expr['function']
            arguments = expr['arguments']
            return self.call_function(function_name, arguments)
        else:
            raise SemanticError("Unknown expression type.")