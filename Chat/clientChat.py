import socket
import threading

# Configuração do cliente
HOST = 'localhost'
PORT = 15000

def receber_mensagens(client_socket):
    """Recebe e imprime mensagens enviadas pelo servidor"""
    while True:
        try:
            mensagem = client_socket.recv(1024).decode('utf-8')
            if mensagem:
                print("\n" + mensagem)
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Definição do nome
print(client_socket.recv(1024).decode('utf-8'))  # Exibe apenas uma mensagem de boas-vindas
nome = input("➡ Escolha seu nome: ").strip()
client_socket.send(nome.encode('utf-8'))

resposta_servidor = client_socket.recv(1024).decode('utf-8')
if "Nome já existe" in resposta_servidor:
    print(resposta_servidor)
    client_socket.close()
    exit()

print(resposta_servidor)

# Inicia uma thread para receber mensagens
threading.Thread(target=receber_mensagens, args=(client_socket,)).start()

while True:
    destinatario = input("Digite o nome do destinatário (/listar para ver usuários, /sair para sair): ").strip()
    client_socket.send(destinatario.encode('utf-8'))

    if destinatario.lower() == "/sair":
        client_socket.close()
        break

    mensagem = input("✏️ Digite sua mensagem: ").strip()
    client_socket.send(mensagem.encode('utf-8'))