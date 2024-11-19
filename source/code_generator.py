import re


class CodeGenerator:
    def __init__(self, formated_tokens:str):
        self.result = formated_tokens
    
    def __built_in_methods(self):
        if 'moreBug' in self.result:
            self.result = 'def plus(x, y):\n\treturn x + y\n\n' + self.result
        if 'minusBug' in self.result:
            self.result = 'def minus(x, y):\n\treturn x - y\n\n' + self.result

    def __variables_types(self):
        self.result = self.result.replace("KW_INT - cryInt\n", "")
        self.result = self.result.replace("KW_BOOL - cryBool\n", "")

    def __block_statements(self):
        self.result = re.sub("\nKW_WHILE - (.*)\n", "\n\nwhile ", self.result)
        self.result = re.sub("\nKW_IF - (.*)\n", "\n\nif ", self.result)
        self.result = re.sub("\nKW_ELSE - (.*)\n", "\n\nelse ", self.result)

    def __values_and_identifiers(self):
        self.result = re.sub("IDENT - (.*)\n", r"\1", self.result)
        self.result = self.result.replace("EQUAL - =\n", "=")
        self.result = re.sub("NUMBER - (\d+)\n", r"\1", self.result)
        self.result = re.sub('TEXT - (".*")\n', r"\1", self.result)
        self.result = re.sub("KW_TRUE - (.*)\n", "True", self.result)
        self.result = re.sub("KW_FALSE - (.*)\n", "False", self.result)

    def __operators(self):
        self.result = self.result.replace("COMMA - ,\n", " , ")
        self.result = self.result.replace("OPEN_PAREN - (\n", " ( ")
        self.result = self.result.replace("CLOSE_PAREN - )\n", " )\n")
        self.result = self.result.replace("MORE_THAN - >\n", " >")
        self.result = self.result.replace("LESS_THAN - <\n", " <")
        self.result = self.result.replace("COLON - :", " : ")

    def __handle_scope_blocks(self):
        self.result_lines = self.result.split("\n")
        inBlock = False
        teste = []
        for line in self.result_lines: 
            if 'flyAway' in line or 'endCheck' in line:
                inBlock = False
                continue

            if 'else' in line:
                inBlock = False

            if inBlock:
                line = '\t' + line

            if 'while' in line or 'if' in line:
                inBlock = True

            teste.append(line)

            if 'else' in line:
                inBlock = True
        self.result = "\n".join(teste)


    def generate(self) -> str:
        self.__built_in_methods()        

        self.result = self.result.replace("EOF - ", "")
        self.result = self.result.replace("NEWLINE - \n", "")

        self.__variables_types() 
        self.__block_statements()        
        
        self.result = self.result.replace("KW_ADDITION - moreBug\n", "plus")
        self.result = self.result.replace("moreBug", "plus")
        self.result = self.result.replace("KW_SUBTRACTION - minusBug\n", "minus")
        self.result = self.result.replace("minusBug", "minus") 

        self.__values_and_identifiers()

        self.__operators()

        self.result = self.result.replace("KW_OUTPUT - outBug\n", "\nprint")
        self.result = self.result.replace("inBug", "input")

        # self.result = re.sub("KW_FALSE - (.*)", "False", self.result)

        self.__handle_scope_blocks()

        return self.result
