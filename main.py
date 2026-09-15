import socket


class Server:
    """
    Classe responsável por criar e gerenciar o socket do servidor.
    Cuida apenas da parte de "abrir a porta e aceitar conexões" —
    a lógica de chat (broadcast, threads, etc.) fica no server.py.
    """

    def __init__(self):
        # Cria o socket: AF_INET = IPv4, SOCK_STREAM = TCP
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Permite reutilizar a porta imediatamente depois que o programa
        # fecha (sem isso, às vezes dá erro "Address already in use"
        # ao reiniciar o servidor logo em seguida).
        self.servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Associa o socket ao endereço e porta.
        # '0.0.0.0' = escuta em todas as interfaces de rede da máquina.
        self.servidor.bind(('0.0.0.0', 4444))

        # Coloca o socket em modo de escuta.
        # O "5" é o número máximo de conexões pendentes na fila de espera.
        self.servidor.listen(5)

    def aceitar(self):
        """
        Bloqueia a execução até um cliente se conectar.
        Retorna:
            conn -> socket específico da conexão com aquele cliente
            addr -> tupla (ip, porta) do cliente
        """
        conn, addr = self.servidor.accept()
        return conn, addr

    def fechar(self):
        """Fecha o socket principal do servidor."""
        self.servidor.close()