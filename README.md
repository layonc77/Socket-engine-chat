# Socket-engine-chat

# Chat via Sockets (TCP)

Chat simples em Python usando `socket` e `threading`, com suporte a
múltiplos clientes conectados simultaneamente e identificação por
apelido.

## Como funciona

- O **servidor** abre uma porta TCP e fica esperando conexões.
- Cada **cliente** que conecta manda um apelido e passa a trocar
  mensagens com todos os outros clientes conectados (broadcast).
- Cada cliente roda em **duas threads**: uma para enviar (ler do
  teclado) e outra para receber (mostrar mensagens na tela).
- O servidor também roda **uma thread por cliente**, permitindo
  atender vários usuários ao mesmo tempo.

## Estrutura do projeto

```
.
├── main.py       # Classe Server: cria, faz bind e listen no socket
├── server.py     # Lógica do chat: aceita conexões, broadcast, apelidos
├── cliente.py    # Classe Client: conecta, envia e recebe mensagens
└── README.md
```

| Arquivo      | Responsabilidade                                              |
|--------------|-----------------------------------------------------------------|
| `main.py`    | Infraestrutura pura de socket do servidor (bind, listen, accept) |
| `server.py`  | Lógica de negócio: gerencia clientes, apelidos e broadcast       |
| `cliente.py` | Conecta ao servidor e troca mensagens via terminal               |

## Requisitos

- Python 3.9+ (ver `pyproject.toml`)
- Nenhuma dependência externa — só biblioteca padrão (`socket`,
  `threading`)

## Como rodar

### 1. Suba o servidor

```bash
python3 server.py
```

Você verá:

```
Servidor à espera...
```

### 2. Conecte um ou mais clientes

Em terminais separados (pode ser na mesma máquina ou em outras, desde
que ajuste o IP — ver seção abaixo):

```bash
python3 cliente.py
```

O terminal vai pedir um apelido:

```
Digite seu apelido: João
```

Digite qualquer mensagem e pressione Enter — ela aparece nos demais
clientes conectados, prefixada com o seu nome:

```
João: oi pessoal!
```

### 3. Encerrar

`Ctrl+C` em cada terminal, ou feche o processo. O servidor detecta a
desconexão automaticamente e avisa os demais clientes.

## Configuração de rede

Por padrão, tudo roda em `localhost` (`0.0.0.0`), na porta `4444`.

Para conectar **de outra máquina na mesma rede**, troque em
`cliente.py`:

```python
self.sock.connect(('0.0.0.0', 4444))
```

pelo IP real do servidor, por exemplo:

```python
self.sock.connect(('192.168.0.10', 4444))
```

## Limitações conhecidas / próximos passos

- Sem criptografia — mensagens trafegam em texto puro (não usar em
  rede pública sem TLS).
- Sem histórico de mensagens — quem entra não vê o que já foi dito.
- Sem comandos especiais (ex: `/sair`, `/lista` para ver quem está
  online, mensagens privadas).
- Sem tratamento de apelidos duplicados.

## Sobre threads e sockets (resumo rápido)

- **Socket**: ponto de comunicação via rede usando TCP
  (`AF_INET` + `SOCK_STREAM`), que garante entrega ordenada dos dados.
- **Thread**: permite ao programa fazer duas coisas em paralelo — por
  exemplo, esperar entrada do teclado (`input()`) e esperar dados da
  rede (`recv()`) ao mesmo tempo, sem uma travar a outra.
- **Broadcast**: o servidor repassa cada mensagem recebida para todos
  os clientes conectados, e não só para o remetente.
