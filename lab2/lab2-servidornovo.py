#Servidor dicionário: lado servidor
import socket
import select
import sys
import threading
import os

HOST = ''
PORT = 1031

#Dicionario
Dicionario = []
#conexoes ativas
conexoes = {}
#entradas para escuta do select
entradas = [sys.stdin]
#cria um lock para acesso a estrutura 'conexoes'
lock = threading.Lock()

def iniciaServidor():
    #Internet (IPv4 + TCP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)
    sock.setblocking(False)
    return sock

def aceitaConexao(sock):
    clisock, endr = sock.accept()
    return clisock, endr

#Classes----------------------------------------------------------------------------------
class Palavra:
    def _init_(self, chave, valor):
        self.chave = chave
        self.valores = valor
#-----------------------------------------------------------------------------------------
#Funções para tratar o arquivo do dicionário----------------------------------------------
def dicionarioAppend():
    pass

def salvarDicionario():
    #Arquivo = open("dicionario.txt", 'w')
    Arquivo = open("dicionario.txt", "a+")
    for palavra in Dicionario:
        Arquivo.write(str(palavra.chave)+'$')
        for definicao in palavra.valores:
            Arquivo.write(str(definicao))
        Arquivo.write("\n")
    Arquivo.close()
    return 1

def removerPalavraArquivo(palavra):
    with open("dicionario.txt", "r") as f:
        linhas = f.readlines()

    with open("dicionario.txt", "w") as f:
        for linha in linhas:
            if linha.startswith(palavra+"$"):
                continue
            f.write(linha)

def lerDicionario():
    Arquivo = open("dicionario.txt", "r")
    linhas = Arquivo.read().splitlines()
    for palavras in linhas:
        i = palavras.split('$')
        adicionaChave(i[0], i[1:])
    Arquivo.close()
    return

def listarPalavrasArquivo():
    palavras = []
    with open("dicionario.txt", "r") as f:
        for linha in f:
            # separa a linha em chave e valores
            chave, *valores = linha.strip().split("$")
            palavras.append(chave)
    return palavras

def limparDicionario():
    # Fecha o arquivo, se estiver aberto
    try:
        arquivo = open("dicionario.txt", "w")
        arquivo.close()
    except:
        pass

    # Remove o arquivo, se existir
    if os.path.exists("dicionario.txt"):
        os.remove("dicionario.txt")

    # Cria um novo arquivo vazio
    arquivo = open("dicionario.txt", "w")
    arquivo.close()

#-----------------------------------------------------------------------------------------
#Funções de palavras e definições---------------------------------------------------------
def listarPalavras():
    chaves = listarPalavrasArquivo()
    chaves.sort()
    return chaves

def buscarPalavra(chave):
    with open("dicionario.txt", "r") as f:
        for linha in f:
            palavras = linha.strip().split("$")
            if chave == palavras[0]:
                return palavras[1:]
    return 0


def imprimirPalavra(chave):
    for palavra in Dicionario:
        if chave == palavra.chave:
            print("\nPalavra: ", palavra.chave, "\nDefinição: ", palavra.valores)
            print("\n")
            return
    print("\nPalavra não encontrada!\n")
    return

def adicionarPalavra(palavra, definicao):
    if not buscarPalavra(palavra):
        Dicionario.append(Palavra(palavra, definicao))
        isSalvo = salvarDicionario()
        if isSalvo == 1:
            return 1
    else:
        print("A palavra já existe no dicionário")
        return 2

def removerPalavra(chave):
    Object = buscarPalavra(chave)
    if Object:
        removerPalavraArquivo(chave)
        return 1
    else:
        return 0

def removerDefinicaoPalavra(chave, numDefinicao):
    definicoes = buscarPalavra(chave)
    if definicoes:
        del definicoes[int(numDefinicao)-1]
        definicoes = '$'.join(definicoes)
        with open('dicionario.txt', 'r') as f:
            linhas = f.readlines()
        with open('dicionario.txt', 'w') as f:
            for linha in linhas:
                if chave in linha:
                    f.write(f"{chave}${definicoes}\n")
                else:
                    f.write(linha)
        return 1
    else:
        print("A palavra não foi encontrada")
        return 0


def adicionarNovaDefinicao(chave, novaDefinicao):
    with open("dicionario.txt", "r") as f:
        linhas = f.readlines()
    encontrada = False
    for i, linha in enumerate(linhas):
        palavra, definicoes = linha.strip().split("$", 1)
        if palavra == chave:
            linhas[i] = f"{palavra}${definicoes}${novaDefinicao}\n"
            encontrada = True
            break
    if not encontrada:
        linhas.append(f"{chave}${novaDefinicao}\n")
    with open("dicionario.txt", "w") as f:
        f.writelines(linhas)
    if encontrada:
        return 1
    else:
        return 2
    
#--------------------------------------------------------------------------------------------
def traduzMsg(msg, clisock, endr):
    if msg[0] == '1':
        isSucesso = adicionarPalavra(msg[1],msg[2])
        if isSucesso == 1:
            newMsg = "Palavra \'" + msg[1] + "\' adicionada com sucesso.\n"
            sendNewMsg(clisock, newMsg)
            return
        elif isSucesso == 2:
            newMsg = "A palavra já existe no dicionário."
            errorNewMsg(clisock, newMsg)
            return
        else:
            errorMsg(clisock)
            return
    elif msg[0] == '2':
        isSucesso = adicionarNovaDefinicao(msg[1], msg[2])
        if isSucesso == 1:
            newMsg = "Definição adicionada à palavra com sucesso!\n"
            sendNewMsg(clisock, newMsg)
        elif isSucesso == 2:
            newMsg = "A palavra não foi encontrada. Cheque novamente a escrita ou adicione a palavra ao dicionário."
            sendNewMsg(clisock, newMsg)
        else:
            errorMsg(clisock)
    elif msg[0] == '3':
        palavraBuscada = buscarPalavra(msg[1])
        if palavraBuscada == 0:
            errorMsg(clisock)
        else:
            valores = palavraBuscada[0:]
            newMsg = "Definições:\n"
            i = 1
            for valor in valores:
                newMsg = newMsg + "\t " + str(i) + " - "+ valor.replace('%', '') + "\n"
                i += 1
            sendNewMsg(clisock, newMsg)
    elif msg[0] == '4':
        palavras = listarPalavras()
        if len(palavras) >= 1:
            newMsg = 'Palavras:\n'
            for palavra in palavras:
                newMsg = newMsg + '\t-' + palavra + '\n'
            sendNewMsg(clisock, newMsg)
        else:
            errorMsg(clisock)
    elif msg[0] == '5':
        isSucesso = removerPalavra(msg[1])
        if isSucesso == 1:
            newMsg = "Palavra removida."
            sendNewMsg(clisock, newMsg)
        if isSucesso == 0:
            newMsg = "A palavra não foi encontrada"
            errorNewMsg(clisock, newMsg)
    elif msg[0] == '6':
        isSucesso = removerDefinicaoPalavra(msg[1], msg[2])
        if isSucesso == 1:
            newMsg = "Definição removida."
            sendNewMsg(clisock, newMsg)
        if isSucesso == 0:
            errorMsg(clisock)
        return
    else:
        errorMsg(clisock)
    return
    
def errorMsg(clisock):
    newMsg = "Ocorreu um erro!"
    clisock.send(newMsg.encode('utf-8'))

def errorNewMsg(clisock, newMsg):
    newErrorMsg = "Ocorreu um erro! " + newMsg
    clisock.send(newErrorMsg.encode('utf-8'))
    
def sendNewMsg(clisock, newMsg):
    clisock.send(newMsg.encode('utf-8'))

def atendeRequisicoes(clisock, endr):
    mensagem_completa = b''  # Inicializa uma variável para armazenar a mensagem completa recebida
    while True:
        while True:
            data = clisock.recv(1024)
            if not data: #dados vazios: cliente encerrou
                print(str(endr) + '-> encerrou')
                lock.acquire()
                del conexoes[clisock]
                lock.release()
                clisock.close()
                return
            mensagem_completa += data  # Adiciona os dados recebidos à mensagem completa
            if b'%' in data:
                mensagem_completa = mensagem_completa.replace(b'%', b'')
                break
        opcao = str(mensagem_completa, encoding='utf-8')
        msg = opcao.split("$")
        traduzMsg(msg, clisock, endr)
        mensagem_completa = b''
        print(str(endr) + ': ' + str(data, encoding='utf-8'))

def main():
    sock = iniciaServidor()
    print('Pronto para receber conexoes...')
    entradas.append(sock)
    while True: #SERVIDOR NAO FINALIZA
        salvarDicionario()
        r, w, e = select.select(entradas, [], [])
        for pronto in r:
            if pronto == sock:
                clisock, endr = aceitaConexao(sock)
                print("Conectado com: ", endr)
                lock.acquire()
                conexoes[clisock] = endr
                lock.release()
                cliente = threading.Thread(target=atendeRequisicoes, args=(clisock, endr))
                cliente.start()
            elif pronto == sys.stdin:
                cmd = input()
                if cmd == 'fim':
                    if not conexoes:
                        sock.close()
                        sys.exit()
                    else:
                        print("Ha conexoes ativas.")
                        print(conexoes)
                if cmd == 'admin mode':
                    print('Digite a ação que quer realizar:')
                    print('\t1 - Remover palavra do dicionário')
                    print('\t2 - Remover definição de palavra do dicionário')
                    print('\t3 - Cancelar')
                    cmd = input()
                    if cmd == '1':
                        print('Digite a palavra a ser removida: ')
                        cmd = input()
                        removerPalavra(cmd)
                    elif cmd == '2':
                        print('Digite a palavra a ter a definição removida: ')
                        cmd = input()
                        print('Digite o número da definição a ser removida: ')
                        cmd2 = input()
                        removerDefinicaoPalavra(cmd, cmd2)
                    elif cmd == '3':
                        print('Cancelado')
                    else:
                        print('Comando inválido!')
main()
