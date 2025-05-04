class Evento:
    def __init__(self, tempo, tipo, fila_origem, fila_destino=None):
        self.tempo = tempo
        self.tipo = tipo  # 'CHEGADA', 'SAIDA', 'PASSAGEM'
        self.fila_origem = fila_origem
        self.fila_destino = fila_destino

    def __lt__(self, other):
        return self.tempo < other.tempo

    def __repr__(self):
        if self.tipo == "PASSAGEM":
            return f"[{self.tempo:.2f}] {self.tipo} de {self.fila_origem.nome} para {self.fila_destino.nome}"
        else:
            return f"[{self.tempo:.2f}] {self.tipo} em {self.fila_origem.nome}"
