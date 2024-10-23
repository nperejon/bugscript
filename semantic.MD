# Documentação do Analisador Semântico (SemanticAnalyzer) do BugScript

## Visão Geral
O Analisador Semântico do BugScript, implementado na classe SemanticAnalyzer, é responsável por verificar a validade semântica do código, garantindo que o programa faça sentido logicamente. Ele trabalha sobre a Árvore Sintática Abstrata (AST) gerada pelo Analisador Sintático, verificando tipos de variáveis, declarações, atribuições e operações.

## Classe: SemanticAnalyzer

### Inicialização

```python
def __init__(self):
```
Inicializa o analisador semântico, criando uma instância da SymbolTable que gerencia as declarações de variáveis, atribuições e tipos.

### Método Principal
```python
def analyze(self, ast):
```
Realiza a análise semântica da AST. Para cada nó da árvore, chama o método visit.

### Método de Visita
```python
def visit(self, node):
```
Determina o tipo de declaração ou expressão que o nó representa e direciona para o método de tratamento adequado.

## Métodos de Tratamento

### Declaração de Variáveis
```python
def handle_var_declaration(self, node):
```
Verifica e declara variáveis no escopo atual. Se a variável possuir um valor inicial, este valor é validado e atribuído.

#### var_name: Nome da variável.
#### var_type: Tipo da variável (int, float, string, bool, etc.).
#### initializer: Expressão que define o valor inicial da variável (se houver).

### Atribuição de Variáveis

```python
def handle_assignment(self, node):
```

Verifica a atribuição de valor a uma variável já declarada e compatibiliza o tipo do valor com o tipo da variável.

### Estrutura Condicional (If-Else)
```python
def handle_if(self, node):
```
Valida a condição do if, garantindo que ela resulte em um valor booleano. Em seguida, analisa os blocos de código then_branch e else_branch.

### Estrutura de Repetição (While)
```python
def handle_while(self, node):
```
Valida a condição do while (espera-se um booleano) e verifica o corpo do loop.

### Declaração de Saída (Output)
```python
def handle_output(self, node):
```
Avalia a expressão de saída para garantir que ela seja válida.

### Avaliação de Expressões
```python
def evaluate_expression(self, expr):
```
Avalia expressões e retorna o tipo do valor resultante. Suporta:

#### LITERALS: Valores literais como números, booleanos e strings.
#### VARIABLES: Verifica o valor da variável.
#### BINARY: Avalia operações binárias, como adição e comparação, e garante compatibilidade de tipos.
#### CALL: Verifica e executa chamadas de funções pré-definidas (adição, subtração, etc.).

### Funções
```python
def call_function(self, function_name, arguments):
```
Avalia e valida as chamadas de funções. As operações aritméticas (como soma e multiplicação) são tratadas aqui.

### Integração com a Tabela de Símbolos
O SemanticAnalyzer utiliza a classe SymbolTable para armazenar informações sobre as variáveis (nome, tipo e status de inicialização). Também verifica:

### Declarações de variáveis (com o método declare).
Atribuições (com o método assign).
Compatibilidade de tipos em operações (como aritmética e lógica).
Tratamento de Erros Semânticos
Os erros semânticos são lançados por meio de exceções SemanticError. Quando uma violação de regra é detectada (como uma atribuição de tipo incorreto), o analisador interrompe o processo com uma mensagem descritiva.

### Considerações Finais
O Analisador Semântico do BugScript é uma etapa crítica que garante a integridade lógica do código, assegurando que tipos de dados sejam compatíveis, variáveis sejam corretamente declaradas e utilizadas, e que todas as expressões e operações sejam válidas.