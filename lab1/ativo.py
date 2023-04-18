# Servidor de Echo (lado ativo)

import socket

HOST = 'localhost'  # maquina onde esta o par passivo
PORTA = 5060        # porta que o par passivo esta escutando

# cria socket
sock = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM

# conecta-se com o par passivo
sock.connect((HOST, PORTA))

# envia uma mensagem para o par conectado
while True:
    user_msg = input("Envie a sua mensagem: ")
    if user_msg == 'fim': break
    else:
        sock.send(bytes(user_msg, 'utf-8'))
        # espera a resposta do par conectado (chamada pode ser BLOQUEANTE)
        msg = sock.recv(1024) # argumento indica a qtde maxima de bytes da mensagem
        # imprime a mensagem recebida
        print('Mensagem recebida: ' + str(msg,  encoding='utf-8'))

#encerra a conexão
sock.close()
