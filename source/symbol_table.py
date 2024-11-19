from source.semantic_error import SemanticError

class SymbolTable:
    def __init__(self):
        self.table = {}
        self.TYPE_MAP = {
            'KW_INT': 'cryInt',
            'KW_FLOAT': 'cryFloat',
            'KW_BOOL': 'cryBool',
            'KW_STRING': 'cryString',
            'WHILE': 'goAway',
            'IF': 'bugCheck'
        }

    def declare(self, name, var_type):
        if name in self.table:
            raise SemanticError(f"Variable '{name}' is already declared.")
        self.table[name] = {'type': var_type, 'initialized': False}

    def assign(self, name, value_type):
        if self.table[name]['type'] != value_type:
            raise SemanticError(f"Type mismatch: cannot assign '{self.TYPE_MAP.get(value_type, 'Unknown')}' to variable '{name}' of type '{self.TYPE_MAP.get(self.table[name]['type'], 'Unknown')}'.")
        self.table[name]['initialized'] = True

    def check_declaration(self, name):
        if name not in self.table:
            raise SemanticError(f"Variable '{name}' is not declared.")
        if not self.table[name]['initialized']:
            raise SemanticError(f"Variable '{name}' is used without being initialized.")
        
    def get_variable_value(self, name):
        self.check_declaration(name)
        return self.table[name]['type']

    def check_condition_type(self, condition_type, actual_type):
        if condition_type != 'KW_BOOL':
            raise SemanticError(f"Condition in '{self.TYPE_MAP.get(actual_type, 'Unknown')}' must be of type 'KW_BOOL', got {condition_type}.")

    def check_logic_operation(self, left_type, operator, right_type):
        if left_type != right_type:
            raise SemanticError(f"Type mismatch in comparison: '{left_type}' {operator} '{right_type}'")
        
    def check_numeric_operation(self, left_type, right_type):
        has_float = 'KW_FLOAT' in [left_type, right_type]
        all_int = all(arg == 'KW_INT' for arg in [left_type, right_type])
        if has_float:
            return 'KW_FLOAT'
        elif all_int:
            return 'KW_INT'
        else:
            raise SemanticError(f"Type mismatch in numeric operation: '{left_type}' and '{right_type}'")