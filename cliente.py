import socket
import threading


class Client:
    """
    Cliente do chat: conecta ao servidor, manda seu apelido logo de
    cara, e depois fica trocando mensagens em duas threads
    (uma para enviar, outra para receber).
    """

    def __init__(self, nome):
        self.nome = nome
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Troque '0.0.0.0' pelo IP real do servidor se ele estiver
        # rodando em outra máquina.
        self.sock.connect(('0.0.0.0', 4444))

        # Primeira coisa que mandamos ao conectar: o apelido.
        # O servidor está esperando exatamente isso como primeira
        # mensagem (ver server.py -> tratar_cliente).
        self.sock.send(self.nome.encode("utf-8"))

    def enviar(self):
        """
        Loop que lê o que o usuário digita e envia pro servidor.
        O servidor já sabe nosso nome, então aqui só mandamos o
        texto puro da mensagem.
        """
        while True:
            msg = input()
            self.sock.send(msg.encode("utf-8"))

    def receber(self):
        """
        Loop que fica esperando mensagens do servidor.
        Essas mensagens já chegam prontas, no formato "nome: texto"
        (foi o server.py que montou isso), então só exibimos.
        """
        while True:
            msg = self.sock.recv(1024)

            if not msg:
                print("Conexão encerrada pelo servidor.")
                break

            print(msg.decode("utf-8"))


# Pergunta o apelido antes de conectar.
nome = input("Digite seu apelido: ").strip() or "Anônimo"

c = Client(nome)

# target=c.enviar / c.receber SEM parênteses: queremos passar a função
# em si para a Thread executar, e não o resultado de chamá-la agora
# (chamar agora travaria o programa aqui, pois enviar()/receber() têm
# while True).
t1 = threading.Thread(target=c.enviar)
t2 = threading.Thread(target=c.receber)

t1.start()
t2.start()

t1.join()
t2.join()