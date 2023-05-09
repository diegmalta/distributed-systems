Atividade 1:
Estilo arquitetural em camada.
Componentes:
Camada de aplicação: interface com o usuário
Funcionalidades: Realiza a comunicação com o usuário sobre qual procedimento ele deseja realizar.
Camada de processamento - cliente: processamento das requisições do cliente
Funcionalidades: Processa as entradas fornecidas pelo cliente e envia requisições ao servidor. Processa mensagens recebidas pelo servidor.
Camada de processamento - servidor: processamento das requisições do servidor
Funcionalidades: Processa as mensagens recebidas pelo usuário. Envia mensagens para o usuário, requisitando entradas.
Camada de dados: acesso e persistência dos dados
Funcionalidades: Cria o arquivo do dicionário. Acessa o dicionário para leitura ou escrita.
Conector entre camada de aplicação e processamento do cliente:
Conexões: conecta a interface para enviar as entradas inseridas para o processamento.
Conector entre camada de processamento do usuário e processamento do servidor:
Conexões: Conecta o processamento de informações entre usuário e servidor.
Conector entre camada de processamento do servidor e de dados:
Conexões: Pega os dados processados e grava os dados ou deleta, ou busca dados e processa eles.

Atividade 2:
A camada de processamento já foi escolhida onde ficaria, a partir do momento em que ela teria sido subdividida em duas camadas: a camada de processamento - servidor e a camada de processamento - cliente.
Para o cliente, teremos os componentes camada de aplicação e camada de processamento - cliente.
Para o servidor, teremos os componentes camada de dados e camada de processamento - servidor.
Conteúdo ordenado:
Cliente enviará para o servidor, o número do procedimento e uma palavra (chave) e/ou uma definição (valor).
Servidor receberá a mensagem, decodificará e processará. Ele irá chamar uma função de acordo com o número de procedimento chamado, e passará a chave e/ou valor para a função como parâmetro.
O servidor irá abrir o arquivo de dicionário, ler ou editá-lo (criando-o caso não exista ainda) e retornará para a função que abriu o arquivo. 
Dependendo da função, ela terá mais comunicação entre cliente e servidor dentro dela, como por exemplo, para adicionar uma definição nova a uma palavra.
Primeiro, o cliente enviará o número do procedimento junto com a palavra (chave).
O servidor checará se a palavra existe.
Se a palavra existir, o servidor irá enviar pro cliente uma mensagem pedindo para ele digitar a definição e esperará receber a resposta.
Se a palavra não existir, retornará um erro.
