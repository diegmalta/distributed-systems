# Exemplo basico socket (lado passivo)

import socket

HOST = ''     # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORTA = 5060  # porta onde chegarao as mensagens para essa aplicacao

# cria um socket para comunicacao
sock = socket.socket() # valores default: socket.AF_INET, socket.SOCK_STREAM

# vincula a interface e porta para comunicacao
sock.bind((HOST, PORTA))

# define o limite maximo de conexoes pendentes e coloca-se em modo de espera por conexao
sock.listen(5)

print("Pronto para receber conexões...")
novoSock, endereco = sock.accept() # retorna um novo socket e o endereco do par conectado
print ('Conectado com: ', endereco)

while True:
    # aceita a primeira conexao da fila (chamada pode ser BLOQUEANTE)
    # depois de conectar-se, espera uma mensagem (chamada pode ser BLOQUEANTE))
    msg = novoSock.recv(1024) # argumento indica a qtde maxima de bits
    msg_received = str(msg, encoding='utf-8')
    if not(msg_received == ''): print(str(msg,  encoding='utf-8'))
    else: break
    # envia mensagem de resposta
    novoSock.send(msg)

# fecha o socket da conexao
novoSock.close()

# fecha o socket principal  
sock.close()
