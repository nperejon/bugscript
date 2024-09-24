Aqui está o raw do markdown:
# Documentação do Analisador Léxico (Lexer) do BugScript

## Visão Geral

O Analisador Léxico do BugScript é responsável por transformar o código-fonte em uma série de tokens. Ele é implementado na classe `BugScriptLexicalAnalyzer` dentro do arquivo `lexer.py`.

## Classe: BugScriptLexicalAnalyzer

### Inicialização

```python
def __init__(self, content: str):
```

content: O código-fonte como uma string.

Método Principal
```python
def tokenize_content(self) -> None:
```

Este método orquestra o processo de tokenização chamando uma série de métodos auxiliares.
Métodos Auxiliares

```python
def remove_comments(self) -> None:
```

Remove comentários (linhas que começam com #) do código.

```python
def remove_empty_lines(self) -> None:
```

Remove linhas vazias do código.

```python
def replace_key_words(self) -> None:
```

Substitui palavras-chave do BugScript por tokens específicos.

```python
def replace_numbers(self) -> None:
```

Identifica e tokeniza números.

```python
def replace_identifiers(self) -> None:
```

Identifica e tokeniza identificadores (nomes de variáveis, funções, etc.).

```python
def replace_symbols_and_characters(self) -> None:
```

Tokeniza símbolos e caracteres especiais.

```python
def spacing_tokens(self) -> None:
```

Ajusta o espaçamento entre tokens.


Dicionário de Palavras-chave
O analisador léxico usa um dicionário para mapear palavras-chave do BugScript para seus respectivos tokens:
```python
keywords = {
    'cryInt': 'KW_INT',
    'cryString': 'KW_STRING',
    'cryBool': 'KW_BOOL',
    'inBug': 'KW_INPUT',
    'outBug': 'KW_OUTPUT',
    'minusBug': 'KW_SUBTRACTION',
    'moreBug': 'KW_ADDITION',
    'bugCheck': 'KW_IF',
    'endBugCheck': 'KW_ELSE',
    'goAway': 'KW_WHILE',
    'flyAway': 'KW_BREAK',
    'true': 'KW_TRUE',
    'false': 'KW_FALSE',
    'end': 'KW_END'
}
```

Expressões Regulares
O analisador léxico utiliza extensivamente a biblioteca re para correspondência de padrões e substituições.
Tratamentos Especiais

Identificadores são tratados cuidadosamente para evitar conflitos com palavras-chave.
Números são identificados e marcados com um prefixo 'NUMBER='.

Saída
O analisador léxico produz uma string onde cada token é separado por espaços. Esta string pode ser facilmente dividida em uma lista de tokens para ser consumida pelo analisador sintático (parser).
Exemplo
Entrada:



```python
cryInt x = 5
outBug(x)
```

Saída:

KW_INT IDENT=x EQUAL NUMBER=5 NEWLINE KW_OUTPUT OPEN_PARENTHESIS IDENT=x CLOSE_PARENTHESIS NEWLINE

## Tratamento de Erros

O analisador léxico não realiza verificações extensivas de erros. Erros de sintaxe são principalmente detectados pelo analisador sintático.

## Fluxo de Processamento

1. O código-fonte é passado para o analisador léxico.
2. Comentários e linhas vazias são removidos.
3. Palavras-chave são substituídas por seus tokens correspondentes.
4. Números são identificados e tokenizados.
5. Identificadores são processados.
6. Símbolos e caracteres especiais são tokenizados.
7. O espaçamento entre tokens é ajustado.
8. A string final de tokens é produzida.

## Considerações Finais

O analisador léxico é a primeira etapa no processo de compilação do BugScript. Ele prepara o código-fonte para ser analisado pelo analisador sintático, transformando o texto bruto em uma sequência de tokens significativos. Esta etapa é crucial para simplificar o trabalho do analisador sintático e permitir uma análise mais eficiente e precisa da estrutura do programa.
