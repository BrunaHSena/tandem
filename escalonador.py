import heapq

class Escalonador:
    def __init__(self):
        self.eventos = []

    def adicionar_evento(self, evento):
        heapq.heappush(self.eventos, evento)

    def proximo_evento(self):
        return heapq.heappop(self.eventos) if self.eventos else None

    def esta_vazio(self):
        return len(self.eventos) == 0

    def ver_proximo_tempo(self):
        return self.eventos[0].tempo if self.eventos else None
