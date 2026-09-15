import threading
from main import Server

# Agora, em vez de uma lista simples de sockets, usamos um dicionário
# que associa cada CONEXÃO (socket) ao NOME (apelido) do cliente.
# Isso permite sabermos quem enviou cada mensagem.
#
# Formato: { conn_socket: "nome_do_cliente", ... }
clientes = {}


def broadcast(mensagem_texto, remetente_conn=None):
    """
    Envia uma mensagem de texto (já formatada com o nome do remetente)
    para todos os clientes conectados.

    mensagem_texto: string pronta para enviar, ex: "João: oi pessoal"
    remetente_conn: socket de quem enviou (só usado se você quiser
                     pular o próprio remetente no envio — ver comentário
                     abaixo).
    """
    mensagem_bytes = mensagem_texto.encode("utf-8")
    mortos = []

    for conn in clientes:
        # Se quiser que o remetente NÃO receba eco da própria mensagem,
        # descomente a linha abaixo:
        # if conn == remetente_conn:
        #     continue
        try:
            conn.send(mensagem_bytes)
        except:
            mortos.append(conn)

    # Remove/desconecta quem falhou durante o envio.
    for c in mortos:
        remover_cliente(c)


def remover_cliente(conn):
    """Remove um cliente do dicionário e fecha a conexão dele com segurança."""
    nome = clientes.pop(conn, None)
    try:
        conn.close()
    except:
        pass
    if nome:
        print(f"{nome} desconectou.")
        broadcast(f"*** {nome} saiu do chat ***")


def tratar_cliente(conn):
    """
    Roda em uma thread por cliente.

    Primeiro passo: recebe o APELIDO que o cliente manda assim que
    conecta (o cliente.py já foi ajustado pra mandar isso automaticamente
    antes de qualquer outra mensagem).

    Depois disso, entra no loop normal de receber mensagens de chat.
    """
    try:
        # A primeira coisa que chega desse cliente é o nome dele.
        nome = conn.recv(1024).decode("utf-8").strip()
        if not nome:
            nome = "Anônimo"

        clientes[conn] = nome
        print(f"{nome} conectou.")
        broadcast(f"*** {nome} entrou no chat ***")

        while True:
            msg = conn.recv(1024)

            # recv() vazio = cliente fechou a conexão "de boas".
            if not msg:
                raise ConnectionError("Cliente desconectou")

            texto = msg.decode("utf-8")

            # Aqui é onde "carimbamos" a mensagem com o nome de quem enviou.
            broadcast(f"{nome}: {texto}", remetente_conn=conn)

    except:
        remover_cliente(conn)


# --- Programa principal do servidor ---

s = Server()
print("Servidor à espera...")

while True:
    conn, addr = s.aceitar()
    print(f'Conexão de {addr}, aguardando apelido...')

    # Cada cliente numa thread própria, assim várias pessoas
    # podem conversar ao mesmo tempo.
    t = threading.Thread(target=tratar_cliente, args=(conn,))
    t.start()