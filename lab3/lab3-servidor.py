#Servidor de dicionario usando RPyC
import rpyc  #modulo que oferece suporte a abstracao de RPC
from rpyc.utils.server import ThreadedServer
import pickle

from rpyc.utils.server import ThreadedServer

PORT = 10000
    
def carregarDicionario(dicionario):
    try:
        with open('dicionario.pickle', 'rb') as f:
            dicionarioCarregado = pickle.load(f)
            print("Dicionario restaurado!")
            dicionario.update(dicionarioCarregado)
    except FileNotFoundError:
        dicionario.clear()
        print("Dicionario novo criado")

def salvarDicionario():
    with open('dicionario.pickle', 'wb') as f:
        pickle.dump(dict(dicionario), f)
        print("Dicionario salvo")

class Dicionario(rpyc.Service):
    def on_connect(self, conn):
        print("Conexao estabelecida.")
    def on_disconnect(self, conn):
        print("Conexao encerrada.")
    def exposed_adicionarAoDicionario(self, chave, valor):
        resposta = adicionarChaveValor(chave, valor)
        salvarDicionario()
        return resposta
    def exposed_buscarPalavra(self, chave):
        return "--->" + str(buscarChave(chave))+"\n"
    def exposed_removerPalavra(self, chave):
        resposta = deletarChave(chave)
        salvarDicionario()
        return resposta
    
def adicionarChaveValor(chave, valor):
    if chave in dicionario:
        valores = dicionario[chave]
        if isinstance(valores, list):
            valores.append(valor)
            return "--->Chave já existia e novo valor adicionado.\n"
        else:
            dicionario[chave] = [valores, valor]
            return "--->Chave com novo valor adicionado.\n"
    else:
        dicionario[chave] = valor
        return "--->Chave com novo valor adicionado.\n"

def buscarChave(chave):
    if chave in dicionario:
        return dicionario.get(chave)
    else:
        return "--->Não tem essa chave! :0\n"

def deletarChave(chave):
    if chave in dicionario:
        del dicionario[chave]
        return "--->Entrada removida do dicionario.\n"
    else:
        return "--->Entrada inexistente no dicionario.\n"

dicionario = {}

carregarDicionario(dicionario)

dicionarioServer = ThreadedServer(Dicionario, port=PORT)
dicionarioServer.start()
