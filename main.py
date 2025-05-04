import yaml, random
from fila import Fila
from evento import Evento
from escalonador import Escalonador

aleatorios_usados = 0

def next_random():
    global aleatorios_usados
    aleatorios_usados += 1
    return random.random()

def sortear(minimo, maximo):
    return minimo + (maximo - minimo) * next_random()

def carregar_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def simular():
    global aleatorios_usados
    aleatorios_usados = 0

    dados = carregar_yaml("simulador.yml")
    filas = {f['id']: Fila(f['id'], f['servidores'], f['capacidade'],
                           f['atendimento_min'], f['atendimento_max']) for f in dados['filas']}

    fila1 = filas['Fila1']
    fila2 = filas['Fila2']

    escalonador = Escalonador()
    tempo = 1.5
    escalonador.adicionar(Evento(tempo, 'CHEGADA', fila1))

    chegada_cfg = dados['chegadas_externas'][0]

    while aleatorios_usados < 100000:
        evento = escalonador.proximo()
        if evento is None:
            break

        tempo_passado = evento.tempo - tempo
        tempo = evento.tempo

        for f in filas.values():
            estado = f.ocupados + f.fila
            f.tempo_estado[estado] = f.tempo_estado.get(estado, 0) + tempo_passado

        if evento.tipo == 'CHEGADA':
            f = evento.origem
            if f.ocupados < f.servidores:
                f.ocupados += 1
                servico = sortear(f.atendimento_min, f.atendimento_max)
                escalonador.adicionar(Evento(tempo + servico, 'PASSAGEM', f, fila2))
            elif f.fila < f.capacidade:
                f.fila += 1
            else:
                f.perdas += 1

            intervalo = sortear(chegada_cfg['intervalo_min'], chegada_cfg['intervalo_max'])
            escalonador.adicionar(Evento(tempo + intervalo, 'CHEGADA', f))

        elif evento.tipo == 'PASSAGEM':
            f1 = evento.origem
            f2 = evento.destino
            f1.ocupados -= 1

            if f1.fila > 0:
                f1.fila -= 1
                f1.ocupados += 1
                servico = sortear(f1.atendimento_min, f1.atendimento_max)
                escalonador.adicionar(Evento(tempo + servico, 'PASSAGEM', f1, f2))

            if f2.ocupados < f2.servidores:
                f2.ocupados += 1
                servico = sortear(f2.atendimento_min, f2.atendimento_max)
                escalonador.adicionar(Evento(tempo + servico, 'SAIDA', f2))
            elif f2.fila < f2.capacidade:
                f2.fila += 1
            else:
                f2.perdas += 1

        elif evento.tipo == 'SAIDA':
            f = evento.origem
            f.ocupados -= 1
            if f.fila > 0:
                f.fila -= 1
                f.ocupados += 1
                servico = sortear(f.atendimento_min, f.atendimento_max)
                escalonador.adicionar(Evento(tempo + servico, 'SAIDA', f))

    for f in filas.values():
        print(f"\n--- Resultados da {f.id} ---")
        total = sum(f.tempo_estado.values())
        for estado, t in sorted(f.tempo_estado.items()):
            print(f"Estado {estado}: Tempo = {t:.2f}, Prob = {t / tempo:.5f}")
        print(f"Clientes perdidos: {f.perdas}")
    print(f"\nTempo total de simulação: {tempo:.2f}")

if __name__ == '__main__':
    simular()
