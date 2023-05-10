#Cliente dicionário: lado cliente
import socket

HOST = 'localhost'
PORT = 1031

def iniciaCliente():
    #Internet (IPv4 + TCP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    return sock

def adminEscolheOpcao(sock, opcao):
    print()
    if opcao == "1":
        chave = input("Digite a nova palavra: ")
        definicao = input("Digite a definição da palavra: ")
        msg = "1$"+chave.strip()+"$"+definicao+"%"
        sock.send(msg.encode('utf-8'))
        msg = sock.recv(1024)
        print('\n'+str(msg, encoding='utf-8'))
    elif opcao == "2":
        chave = input("Digite a palavra a adicionar uma definição: ")
        novaDefinicao = input("Digite a nova definição: ")
        msg = '2$'+chave.strip()+'$'+novaDefinicao+'%'
        sock.send(msg.encode('utf-8'))
        msg = sock.recv(1024)
        print('\n'+str(msg, encoding='utf-8'))
    elif opcao == "3":
        chave = input("Digite a palavra a ser buscada: ")
        msg = '3$'+chave.strip()+'%'
        sock.send(msg.encode('utf-8'))
        msg = sock.recv(1024)
        print('\n'+str(msg, encoding='utf-8'))
    elif opcao == "4":
        msg = '4%'
        sock.send(msg.encode('utf-8'))
        msg = sock.recv(1024)
        print('\n'+str(msg, encoding='utf-8'))
    elif opcao == "5":
        chave = input("Digite a palavra a ser removida: ")
        msg = '5$'+chave.strip()+'%'
        sock.send(msg.encode('utf-8'))
        msg = sock.recv(1024)
        print('\n'+str(msg, encoding='utf-8'))
    elif opcao == "6":
        chave = input("Digite a palavra a ter a definição removida: ")
        numDefinicao = input("Digite o número da definição a ser removida (começando em 1): ")
        msg = '6$'+chave.strip()+'$'+numDefinicao+'%'
        sock.send(msg.encode('utf-8'))
        msg = sock.recv(1024)
        print('\n'+str(msg, encoding='utf-8'))
    elif opcao == "9":
        print()
        return 0
    else:
        print("Opção inválida!!!\n")
    return

def convidadoEscolheOpcao(sock, opcao):
    print()
    if opcao == "1":
        chave = input("Digite a nova palavra: ")
        definicao = input("Digite a definição da palavra: ")
        msg = "1$"+chave.strip()+"$"+definicao+"%"
        sock.send(msg.encode('utf-8'))
        msg = sock.recv(1024)
        print('\n'+str(msg, encoding='utf-8'))
    elif opcao == "2":
        chave = input("Digite a palavra a adicionar uma definição: ")
        novaDefinicao = input("Digite a nova definição: ")
        msg = '2$'+chave.strip()+'$'+novaDefinicao+'%'
        sock.send(msg.encode('utf-8'))
        msg = sock.recv(1024)
        print('\n'+str(msg, encoding='utf-8'))
    elif opcao == "3":
        chave = input("Digite a palavra a ser buscada: ")
        msg = '3$'+chave.strip()+'%'
        sock.send(msg.encode('utf-8'))
        msg = sock.recv(1024)
        print('\n'+str(msg, encoding='utf-8'))
    elif opcao == "4":
        msg = '4%'
        sock.send(msg.encode('utf-8'))
        msg = sock.recv(1024)
        print('\n'+str(msg, encoding='utf-8'))
    elif opcao == "9":
        print('Saindo...')
        return 0
    else:
        print("Opção inválida")
    return

#Interfaces de usuários diferentes
def dicionarioAdmin(sock):
    print("")
    while True:
        print("Dicionário - MODO CLIENTE ADMIN")
        print("Opções:")
        print("\t1 - Adicionar uma palavra ao dicionário")
        print("\t2 - Adicionar uma definição a uma palavra")
        
        print("\t3 - Buscar uma palavra no dicionário")
        print("\t4 - Listar todas as palavras do dicionário")
    
        print("\t5 - Remover uma palavra do dicionário")
        print("\t6 - Remover uma definição de uma palavra")
        
        print("\t9 - Sair")
    
        opcao = input("Escolha um dígito: ")
        retorno = adminEscolheOpcao(sock, opcao)
        if retorno == 0:
            break

def dicionarioConvidado(sock):
    print("")
    while True:
        print("Dicionário")
        print("Opções:")
        print("\t1 - Adicionar uma palavra ao dicionário")
        print("\t2 - Adicionar uma definição a uma palavra")
            
        print("\t3 - Buscar uma palavra no dicionário")
        print("\t4 - Listar todas as palavras do dicionário")
        print("\t9 - Sair")

        opcao = input("Escolha um dígito: ")
        retorno = convidadoEscolheOpcao(sock, opcao)
        if retorno == 0:
            break

#Função main, com a interface inicial de cliente
def main():
    sock = iniciaCliente()
    while True:
        print("Dicionário! Encontre palavras e suas definições, e colabore!")
        print("Caso não seja um administrador, insira como usuário \'convidado\'.")
        print("Para sair, digite 'sair' no lugar do usuário:")
        login = input("Usuário: ")
        if login == "admin":
            senha = input("Senha: ")
            if senha == "admin":
                dicionarioAdmin(sock)
            else:
                print("Senha incorreta.")
        elif login == 'convidado':
            dicionarioConvidado(sock)
        elif login == 'sair':
            break
        else:
            print("Usuário inválido!\n\n\n")
    sock.close()

main()
