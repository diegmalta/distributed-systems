
# Laboratório 2 - Aplicação cliente/servidor básica

## Introdução
O objetivo deste Laboratório é desenvolver uma aplicação distribuída para aplicar os conceitos estudados sobre arquitetura de software e arquitetura de sistema; servidores
multiplexados e concorrentes; e seguir praticando com a programação usando sockets.

A aplicação que vamos desenvolver será um dicionário remoto que poderá ser consultado e alterado. As chaves e valores do dicionário serão strings. O dicionário deverá ser armazenado em disco para ser restaurado em uma execução futura.
- Para a consulta, o usuário informará uma chave e receberá como resposta a lista de valores associados a essa chave, em ordem alfabética (lista vazia caso a entrada não exista).
- Para a escrita, o usário informará um par chave e valor e receberá como resposta a confirmação que a nova entrada foi inserida, ou que 0 novo valor foi acrescentado em uma entrada existente.
- A remoção de uma entrada no dicionário somente poderá ser feita pelo administrador do dicionário.
## Linguagem utilizada

[![Python](https://img.shields.io/badge/Language-Python-yellow)](https://www.python.org)

## Atividade 1

- 1 - Estilo arquitetural em camada. 
- 2 - Componentes, Funcionalidades e modos de conexão:
    - Componentes: 
        - Camada de aplicação: interface com o usuário
            - Funcionalidades: Realiza a comunicação com o usuário sobre qual procedimento ele deseja realizar, por meio de uma interface. 
        - Camada de processamento: processamento das requisições 
            - Funcionalidades: Processa as entradas fornecidas pela interface e envia requisições à camada de banco de dados. Também recebe informações da camada de dados e envia para a camada de interface. 
        - Camada de dados: acesso e persistência dos dados 
            - Funcionalidades: Cria o arquivo do dicionário. Acessa o dicionário para leitura ou escrita.
    - Conexões:
        - Conector entre camada de aplicação e processamento: 
            - Conexões: conecta a interface para enviar as entradas inseridas para o processamento. 
        - Conector entre camada de processamento e de dados: 
            - Conexões: Pega os dados processados e grava os dados ou deleta, ou busca dados e processa eles.
## Atividade 2

- 1: Componente de interface
- 2: Componente de processamento e componente de dados
- 3: Conteúdo ordenado:
    - Cliente enviará para o servidor, o número do procedimento e uma palavra (chave) e/ou uma definição (valor). 
    - Servidor receberá a mensagem, decodificará e processará. Ele irá chamar uma função de acordo com o número de procedimento chamado, e passará a chave e/ou valor para a função como parâmetro. 
    - O servidor irá abrir o arquivo de dicionário, ler ou editá-lo (criando-o caso não exista ainda) e retornará para a função que abriu o arquivo.
    - Dependendo da função, ela terá mais comunicação entre cliente e servidor dentro dela, como por exemplo, para adicionar uma definição nova a uma palavra.
    - Primeiro, o cliente enviará o número do procedimento junto com a palavra (chave). 
    - O servidor checará se a palavra existe.
    - Se a palavra existir, o servidor irá enviar pro cliente uma mensagem pedindo para ele digitar a definição e esperará receber a resposta.
    - Se a palavra não existir, retornará um erro.
## Principais decisões tomadas:

- Primeiro, foi feito um lado cliente e um lado servidor com base no programa construído nas aulas. E a primeira camada a ser construída foi a interface.
- Depois de uma interface básica estar pronta, foi construída uma forma de receber a mensagem. Para conseguir codificar tudo em uma mensagem, foi feito um caractere que não existe em palavras da língua portuguesa. O caractere especial escolhido foi $.
- Este caractere se insere no meio dos comandos inseridos antes de ser enviado pelo cliente ao servidor. Por exemplo, para inserir a palavra "arroz" no dicionário com significado "comida", será enviado ao servidor a string "1$arroz$comida%". 1 é o comando de inserir palavra no dicionário e % é um outro caractere especial para indicar o fim da mensagem enviada para o servidor.
- O servidor agora lê o número contido até o primeiro caractere $. Dependendo do número lido, ele chamará uma função diferente no dicionário e dará um retorno de sucesso, conteúdo ou erro para a interface do cliente.
- Palavra é uma classe que contém chave e valor, dentro do servidor.
## Imagem da arquitetura

![](https://raw.githubusercontent.com/diegmalta/distributed-systems/main/lab2/image.png)
## Referências

 - BM. van Steen and A.S. Tanenbaum, Distributed Systems, 4th ed., distributed-systems.net, 2023.
 - Slides e aulas das semanas 3 (Arquiteturas de sistemas distribuídos) e 4 (Processos e threads em sistemas distribuı́dos) da disciplina Sistemas Distribuídos da Professora Silvana Rossetto.
## Autores

- [@diegmalta](https://www.github.com/diegmalta)

