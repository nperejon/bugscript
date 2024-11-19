# Linguagem de programação BugScript

## Como testar?

### Requisitos
```
python >= 3.8
```

### Executar teste com debug
Ele irá executar o arquivo `tests/teste.bug` e irá exibir no console os passos da compilação. Use esse metodo para debugar código.

1. Executar o seguinte comando em um terminal na pasta raíz do projeto:
```
python main.py 
```

### Executar conjunto de tests
Ele irá executar os arquivos que estão na pasta `tests/` em sequência. Caso deseje alterar a ordem, nome dos arquivos ou adicionar um novo, lembrar de alterar o arquivo `tests.py`

1. Executar o seguinte comando em um terminal na pasta raíz do projeto:
```
python tests.py 
```

### Testar próprio scipt
1. Escrever um código bugscript em um arquivo `.bug` no mesmo diretório do projeto. Ex: 
test_file.bug
```
# Set CryInt Variables by Input
cryInt n1 = int(inBug("Digite um número: "))
cryInt n2 = int(inBug("Digite outro número: "))

# String interpolation
outBug(f"A soma entre {n1} e {n2} é igual a {moreBug(n1, n2)}")
outBug(f"A subtração entre {n1} e {n2} é igual a {minusBug(n1, n2)}")
```

2. Executar o seguinte comando em um terminal na pasta raíz do projeto passando o nome do arquivo criado:
```
python compiler.py test_file.bug 
```