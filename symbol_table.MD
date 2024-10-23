# Documentação da Tabela de Símbolos (SymbolTable) do BugScript

## Visão Geral
A classe SymbolTable gerencia as variáveis declaradas no código, armazenando seus nomes, tipos e status de inicialização. Ela também garante a compatibilidade de tipos em atribuições e operações, além de verificar o uso adequado das variáveis e condições no BugScript.

## Classe: SymbolTable

### Inicialização
```python
def __init__(self):
```
Inicializa a tabela de símbolos como um dicionário vazio e define o mapeamento de palavras-chave (como KW_INT, KW_FLOAT, etc.) para os tipos específicos do BugScript (cryInt, cryFloat, etc.).

#### table: Dicionário que armazena informações sobre as variáveis.
#### TYPE_MAP: Mapeia palavras-chave internas para tipos customizados (ex.: KW_INT → cryInt).

## Métodos Principais

### Declaração de Variáveis
```python
def declare(self, name, var_type):
```
Declara uma variável no escopo atual. Se a variável já foi declarada, lança um erro semântico.

name: Nome da variável.
var_type: Tipo da variável (int, float, string, etc.).
Erros:

SemanticError: Lançado se a variável já foi declarada.

### Atribuição de Variáveis
```python
def assign(self, name, value_type):
```
Atribui um valor a uma variável. Verifica a compatibilidade entre o tipo do valor e o tipo da variável declarada. Após a atribuição, marca a variável como inicializada.

name: Nome da variável.
value_type: Tipo do valor atribuído à variável.
Erros:

SemanticError: Lançado se o tipo do valor não for compatível com o tipo da variável.

### Verificação de Declaração
```python
def check_declaration(self, name):
```
Verifica se uma variável foi declarada e se está inicializada antes de ser usada.

name: Nome da variável.
Erros:

SemanticError: Lançado se a variável não foi declarada ou se foi usada sem inicialização.

### Obtenção do Valor de uma Variável
```python
def get_variable_value(self, name):
```
Retorna o tipo da variável após verificar sua declaração e inicialização.

name: Nome da variável.
Retorna: O tipo da variável.

Erros:

SemanticError: Lançado se a variável não foi declarada ou não foi inicializada.

## Verificações de Tipos e Operações

### Verificação de Condições
```python
def check_condition_type(self, condition_type, actual_type):
```
Garante que a condição fornecida seja do tipo booleano (KW_BOOL). Esse método é utilizado principalmente em estruturas condicionais como if e while.

condition_type: Tipo da condição (espera-se KW_BOOL).
actual_type: Tipo da condição atual (para exibição no erro).
Erros:

SemanticError: Lançado se a condição não for do tipo KW_BOOL.

### Verificação de Operações Lógicas
```python
def check_logic_operation(self, left_type, operator, right_type):
```
Verifica se os tipos de operandos de uma operação lógica são compatíveis. Ambos os lados devem ter o mesmo tipo.

left_type: Tipo do operando esquerdo.
operator: Operador lógico (ex.: ==, !=, <, >).
right_type: Tipo do operando direito.
Erros:

SemanticError: Lançado se os tipos dos operandos forem incompatíveis.

### Verificação de Operações Numéricas
```python
def check_numeric_operation(self, left_type, right_type):
```
Verifica a compatibilidade de tipos em operações numéricas. Se um dos operandos for KW_FLOAT, o resultado será KW_FLOAT. Se ambos forem KW_INT, o resultado será KW_INT. Caso contrário, um erro será levantado.

left_type: Tipo do operando esquerdo.
right_type: Tipo do operando direito.
Retorna: O tipo resultante da operação.

Erros:

SemanticError: Lançado se os tipos dos operandos forem incompatíveis para operações numéricas.
Tratamento de Erros
Os erros semânticos são tratados pela classe SemanticError. Sempre que uma regra semântica é violada (como declaração duplicada, tipos incompatíveis ou uso de variáveis não inicializadas), uma exceção é levantada com uma mensagem descritiva.