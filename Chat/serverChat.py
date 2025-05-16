import socket
import threading

# Configuração do servidor
HOST = 'localhost'
PORT = 15000
clientes = {}  # Dicionário para armazenar clientes {socket: nome}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

def broadcast(mensagem, remetente=None):
    """Envia uma mensagem para todos os clientes conectados, exceto o remetente."""
    for cliente in clientes:
        if cliente != remetente:
            cliente.send(mensagem.encode('utf-8'))

def handle_client(client_socket, addr):  # ✅ Agora a função aceita 2 argumentos corretamente
    """Gerencia a comunicação com cada cliente"""
    client_socket.send("\nBem-vindo ao chat! Digite seu nome: ".encode('utf-8'))
    nome = client_socket.recv(1024).decode('utf-8').strip()

    # Verificar se o nome já existe
    if nome in clientes.values():
        client_socket.send("Nome já existe! Escolha outro.\n".encode('utf-8'))
        client_socket.close()
        return
    
    clientes[client_socket] = nome
    print(f"{nome} entrou no chat.")
    broadcast(f"{nome} entrou no chat.", remetente=client_socket)

    client_socket.send("\nComandos disponíveis:\n/listar - Ver usuários\n/sair - Sair do chat\n".encode('utf-8'))

    while True:
        try:
            client_socket.send("Digite o nome do destinatário (/listar para ver usuários, /sair para sair): ".encode('utf-8'))
            destinatario = client_socket.recv(1024).decode('utf-8').strip()

            if destinatario.lower() == "/sair":
                break
            elif destinatario.lower() == "/listar":
                client_socket.send("Usuários online: {}\n".format(', '.join(clientes.values())).encode('utf-8'))
                continue
            
            if destinatario not in clientes.values():
                client_socket.send("Destinatário não encontrado.\n".encode('utf-8'))
                continue

            client_socket.send("Digite sua mensagem: ".encode('utf-8'))
            mensagem = client_socket.recv(1024).decode('utf-8').strip()

            # Enviar mensagem para destinatário
            for cliente, nome_cliente in clientes.items():
                if nome_cliente == destinatario:
                    cliente.send(f"{nome} ➡ {destinatario}: {mensagem}".encode('utf-8'))
                    print(f"{nome} enviou uma mensagem para {destinatario}: {mensagem}")
                    break

        except:
            break

    print(f"{nome} saiu do chat.")
    del clientes[client_socket]
    broadcast(f"{nome} saiu do chat.")
    client_socket.close()

print("Servidor de chat iniciado... Aguardando conexões.")

while True:
    client_socket, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket, addr)).start()
