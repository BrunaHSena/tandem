class Fila:
    def __init__(self, id, servidores, capacidade, atendimento_min, atendimento_max):
        self.id = id
        self.servidores = servidores
        self.capacidade = capacidade
        self.atendimento_min = atendimento_min
        self.atendimento_max = atendimento_max
        self.ocupados = 0
        self.fila = 0
        self.perdas = 0
        self.tempo_estado = {}
        self.tempo_ultimo_evento = 0
