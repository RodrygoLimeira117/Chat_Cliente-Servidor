# Chat com Sockets em Python

Este é um projeto simples de chat em rede utilizando `sockets` e `threads` com Python. Ele permite que vários usuários se conectem simultaneamente a um servidor, escolham um nome de usuário e troquem mensagens privadas entre si.

## 🚀 Funcionalidades

- Múltiplos clientes conectados simultaneamente
- Troca de mensagens privadas entre usuários
- Comandos disponíveis:
  - `/listar` — lista os usuários online
  - `/sair` — encerra a conexão com o chat
- Prevenção de nomes duplicados

## 📁 Estrutura

- `servidor.py`: código do servidor que aceita conexões de clientes e faz o gerenciamento.
- `cliente.py`: código do cliente que se conecta ao servidor, envia comandos e mensagens.


