import heapq

class Escalonador:
    def __init__(self):
        self.eventos = []

    def adicionar(self, evento):
        heapq.heappush(self.eventos, evento)

    def proximo(self):
        return heapq.heappop(self.eventos) if self.eventos else None

    def vazio(self):
        return len(self.eventos) == 0
