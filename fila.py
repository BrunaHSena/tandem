class Fila:
    def __init__(self, nome, servidores, capacidade, atendimento_min, atendimento_max):
        self.nome = nome  # Ex: "Fila1"
        self.servidores = servidores
        self.capacidade = capacidade
        self.atendimento_min = atendimento_min
        self.atendimento_max = atendimento_max

        # Estado da fila
        self.ocupados = 0  # servidores ocupados
        self.fila_espera = 0  # clientes esperando
        self.perdas = 0

        # Estatísticas
        self.tempo_estado = {}  # tempo acumulado para cada estado
        self.tempo_ultimo_evento = 0.0

        # Roteamento (inicialmente vazio, será preenchido no main)
        self.roteamento_temp = []  # lista de dicionários vindos do YAML
        self.roteamento = {}       # dict com {Fila: probabilidade}

    def atualiza_tempo_estado(self, tempo_atual):
        """Acumula o tempo no estado atual da fila."""
        estado = self.ocupados + self.fila_espera
        tempo = tempo_atual - self.tempo_ultimo_evento
        self.tempo_estado[estado] = self.tempo_estado.get(estado, 0) + tempo
        self.tempo_ultimo_evento = tempo_atual
