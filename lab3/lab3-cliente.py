# Cliente de dicionario usando RPyC
import rpyc

#endereco do servidor
SERVER = 'localhost'
PORT = 10000

dicionario = rpyc.connect(SERVER, PORT)

def iniciaConexao():
    conn = rpyc.connect(SERVER, PORT)
    print(conn.root.get_service_name())
    return conn

def fazRequisicoes(conn):
    print("Dicionário! Encontre palavras e suas definições, e colabore!")
    while True:
        print("Opções:")
        print("\t1 - Adicionar uma palavra e/ou definição ao dicionário")
            
        print("\t2 - Buscar uma palavra e suas definições no dicionário")
        
        print("\t3 - Remover uma palavra do dicionário")
            
        print("\t0 - Sair")
        opcao = str(input("Selecione a opção:"))
    
        if opcao == '0':
            break
        elif opcao == '1':
            chave = str(input("Palavra a ser adicionada ou ter nova definição:"))
            valor = str(input("Nova definição da palavra:"))
            adicionarAoDicionario = dicionario.root.adicionarAoDicionario(chave, valor)
            print(adicionarAoDicionario)
        elif opcao == '2':
            chave = str(input("Palavra a ser buscada:"))
            buscarPalavra = dicionario.root.buscarPalavra(chave)
            print(buscarPalavra)
        elif opcao == '3':
            chave = str(input("Palavra a ser removida:"))
            removerPalavra = dicionario.root.removerPalavra(chave)
            print(removerPalavra)
        else:
            print("Essa entrada é inválida >:^(")

def main():
    conn = iniciaConexao()
    fazRequisicoes(conn)
    conn.close()

if __name__ == '__main__':
    main()
