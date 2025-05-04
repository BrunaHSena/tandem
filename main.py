import yaml
import random
from fila import Fila
from evento import Evento
from escalonador import Escalonador

aleatorios_usados = 0

def next_random():
    global aleatorios_usados
    aleatorios_usados += 1
    return random.random()

def sortear_tempo(min_valor, max_valor):
    return min_valor + (max_valor - min_valor) * next_random()

def carregar_modelo(arquivo):
    with open(arquivo, 'r') as f:
        return yaml.safe_load(f)

def inicializar_filas(dados):
    filas = {}
    for f in dados['filas']:
        fila = Fila(f['id'], f['servidores'], f['capacidade'], f['atendimento_min'], f['atendimento_max'])
        filas[f['id']] = fila
    return filas

def imprimir_resultados(filas, tempo_global):
    for id, fila in filas.items():
        print(f"\n--- Resultados da {fila.nome} ---")
        total_tempo = sum(fila.tempo_estado.values())
        for estado, tempo in sorted(fila.tempo_estado.items()):
            prob = tempo / tempo_global if tempo_global > 0 else 0
            print(f"Estado {estado} cliente(s): Tempo acumulado = {tempo:.2f}, Probabilidade = {prob:.5f}")
        print(f"Clientes perdidos: {fila.perdas}")
    print(f"\nTempo total de simulação: {tempo_global:.2f}")

def main():
    global aleatorios_usados
    aleatorios_usados = 0

    dados = carregar_modelo('simulador.yml')
    filas = inicializar_filas(dados)

    # Define roteamento: 100% dos clientes da Fila1 vão para Fila2
    fila1 = filas['Fila1']
    fila2 = filas['Fila2']
    fila1.roteamento = {fila2: 1.0}
    fila2.roteamento = {}  # Clientes saem após atendimento

    escalonador = Escalonador()

    tempo_atual = 1.5
    escalonador.adicionar_evento(Evento(tempo_atual, 'CHEGADA', fila1))

    while aleatorios_usados < 100000 and not escalonador.esta_vazio():
        evento = escalonador.proximo_evento()

        for fila in filas.values():
            fila.atualiza_tempo_estado(evento.tempo)

        tempo_atual = evento.tempo
        fila = evento.fila_origem

        if evento.tipo == 'CHEGADA':
            if fila.ocupados < fila.servidores:
                fila.ocupados += 1
                tempo_serv = sortear_tempo(fila.atendimento_min, fila.atendimento_max)
                destino = list(fila.roteamento.keys())[0]
                escalonador.adicionar_evento(Evento(tempo_atual + tempo_serv, 'PASSAGEM', fila, destino))
            elif fila.fila_espera < fila.capacidade:
                fila.fila_espera += 1
            else:
                fila.perdas += 1

            # Agendar próxima chegada externa
            chegada = dados['chegadas_externas'][0]
            intervalo = sortear_tempo(chegada['intervalo_min'], chegada['intervalo_max'])
            escalonador.adicionar_evento(Evento(tempo_atual + intervalo, 'CHEGADA', fila))

        elif evento.tipo == 'PASSAGEM':
            fila.ocupados -= 1
            if fila.fila_espera > 0:
                fila.fila_espera -= 1
                fila.ocupados += 1
                destino = list(fila.roteamento.keys())[0]
                tempo_serv = sortear_tempo(fila.atendimento_min, fila.atendimento_max)
                escalonador.adicionar_evento(Evento(tempo_atual + tempo_serv, 'PASSAGEM', fila, destino))

            destino = evento.fila_destino
            if destino.ocupados < destino.servidores:
                destino.ocupados += 1
                tempo_serv = sortear_tempo(destino.atendimento_min, destino.atendimento_max)
                escalonador.adicionar_evento(Evento(tempo_atual + tempo_serv, 'SAIDA', destino))
            elif destino.fila_espera < destino.capacidade:
                destino.fila_espera += 1
            else:
                destino.perdas += 1

        elif evento.tipo == 'SAIDA':
            fila.ocupados -= 1
            if fila.fila_espera > 0:
                fila.fila_espera -= 1
                fila.ocupados += 1
                tempo_serv = sortear_tempo(fila.atendimento_min, fila.atendimento_max)
                escalonador.adicionar_evento(Evento(tempo_atual + tempo_serv, 'SAIDA', fila))

    imprimir_resultados(filas, tempo_atual)

if __name__ == '__main__':
    main()
