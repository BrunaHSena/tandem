class Evento:
    def __init__(self, tempo, tipo, origem, destino=None):
        self.tempo = tempo
        self.tipo = tipo  # 'CHEGADA', 'SAIDA', 'PASSAGEM'
        self.origem = origem
        self.destino = destino

    def __lt__(self, other):
        return self.tempo < other.tempo
