import random
import copy
import time
from termcolor import colored

edades_conejos_muertos = []
edades_zorros_muertos = []

def crear_grilla(N,dc,dz,dp,ec,ez):
  """
  Genera la grilla inicial y retorna una lista de listas con el estado de 
  cada celda.
  """
  grilla = []

  for i in range(N):
      fila = []
      for j in range(N):
          r1 = random.random() # Genera un número aleatorio entre 0 y 1
          if r1 <= dc:
             celda = {'tipo': 'conejo','energia': ec,'edad': 0}
          elif r1 <= (dc + dz):
              celda = {'tipo': 'zorro','energia': ez,'edad': 0}
          else:
              r2 = random.random()
              if r2 <= dp:
                  celda = 'pasto'
              else:
                  celda = None
          fila.append(celda)
      grilla.append(fila)
  return grilla


def imprimir_grilla(grilla):
  """
  Imprime la grilla con el color correspondiente en cada celda.
  """
  texto_completo = ''
  for fila in grilla:
      for celda in fila:
          if celda is None:
            texto_completo += '  '
          elif celda == 'pasto':
            texto_completo += colored ('▓▓', 'green')
          elif type(celda) is dict:                     # Para verificar que el tipo de celda es un diccionario
            if celda['tipo'] == 'conejo':
              texto_completo += colored ('▓▓', 'cyan')
            elif celda['tipo'] == 'zorro':
              texto_completo += colored ('▓▓', 'red')
      texto_completo += '\n'
  print(texto_completo)                                           


def vecinos(i, j, N):
  """
  Devuelve una lista de tuplas con las coordenadas de los vecinos 
  válidos de la celda.
  """
  lista_vecinos = []

  if i > 0:
    lista_vecinos.append((i - 1, j)) # Vecino arriba
  if i < N - 1:
    lista_vecinos.append((i + 1, j)) # Vecino abajo
  if j > 0:
    lista_vecinos.append((i, j - 1)) # Vecino izquierda
  if j < N - 1:
    lista_vecinos.append((i, j + 1)) # Vecino derecha

  return lista_vecinos


def crecer_pasto(snapshot, nueva, pp, N):
  """
  Hace crecer el pasto en celdas vacías si tienen pasto vecino.
  """
  for i in range(N):
    for j in range(N):
      if snapshot[i][j] is None:
        lista_vecinos = vecinos(i,j, N)
        
        tiene_pasto_vecino = False
        
        for par in lista_vecinos:
          x = par[0]
          y = par[1]
          if 0 <= x < N and 0 <= y < N:
            if snapshot[x][y] == 'pasto':
              tiene_pasto_vecino = True
              break
        
        if tiene_pasto_vecino:
          if random.random() <= pp:
            nueva[i][j] = 'pasto'


def elegir_destino_zorro(snapshot, i, j, N):
  """
  Elige aleatoriamente una celda destino para el zorro que no tenga
  un zorro en el snapshot.
  """
  lista_vecinos = vecinos(i,j, N)
  vecinos_validos = []
  for par in lista_vecinos: 
    x = par[0]
    y = par[1]
    celda_vecina = snapshot[x][y]
    es_zorro = type(celda_vecina) is dict and celda_vecina['tipo'] == 'zorro'
    if not es_zorro:
      vecinos_validos.append(par)
  if len(vecinos_validos) == 0:
    return (i, j)
  
  return random.choice(vecinos_validos) # Elige una vecino al azar de la lista de vecinos válidos


def mover_y_reproducir_zorros(snapshot, nueva, edades_zorros_muertos, e_min, prz, ez, gz, N):
  """
  Actualiza la información de los zorros, los mueve y los reproduce.
  """
  for i in range(N):
    for j in range(N):
      celda = snapshot[i][j]

      if type(celda) is dict and celda['tipo'] == 'zorro':
        zorro = {}
        zorro['tipo'] = 'zorro'
        zorro['energia'] = celda['energia'] - 2
        zorro['edad'] = celda['edad'] + 1

        if zorro['energia'] <= 0:
          edades_zorros_muertos.append(zorro['edad'])
          nueva[i][j] = None
        else:
          destino = elegir_destino_zorro(snapshot, i, j, N)
          x = destino[0]
          y = destino[1]
          if type(nueva[x][y]) is dict and nueva[x][y]['tipo'] == 'zorro':
            nueva[i][j] = zorro
          else:
            nueva[x][y] = zorro
            if (x,y) != (i,j) and zorro['energia'] >= e_min and random.random() <= prz:
              nueva[i][j] = {'tipo': 'zorro', 'energia': ez, 'edad': 0}
            elif (x,y) != (i,j):
              nueva[i][j] = None


def elegir_destino_conejo(snapshot, i, j, N):
  """
  Elige aleatoriamente una celda destino para el conejo que no tenga
  un animal en el snapshot.
  """
  lista_vecinos = vecinos(i,j, N)
  vecinos_validos = []
  for par in lista_vecinos: 
    x = par[0]
    y = par[1]
    celda_vecina = snapshot[x][y]
    if type(celda_vecina) is not dict:
      vecinos_validos.append(par)
  if len(vecinos_validos) == 0:
    return (i, j)
  
  return random.choice(vecinos_validos) # Elige una vecino al azar de la lista de vecinos válidos


def mover_y_reproducir_conejos(snapshot, nueva, edades_conejos_muertos, e_min, prc, ec, gc, gz, N):
  """
  Actualiza la información de los conejos, los mueve y los reproduce.
  """
  for i in range(N):
    for j in range(N):
      celda = snapshot[i][j]

      if type(celda) is dict and celda['tipo'] == 'conejo':
        if type(nueva[i][j]) is dict and nueva[i][j]['tipo'] == 'zorro':
          edades_conejos_muertos.append(celda['edad'])
          continue
        conejo = {}
        conejo['tipo'] = 'conejo'
        conejo['energia'] = celda['energia'] - 1
        conejo['edad'] = celda['edad'] + 1

        if conejo['energia'] == 0:
          edades_conejos_muertos.append(conejo['edad'])
          if type(nueva[i][j]) is dict and nueva[i][j]['tipo'] == 'conejo':
            nueva[i][j] = None

        else:
          destino = elegir_destino_conejo(snapshot, i, j, N)
          x = destino[0]
          y = destino[1]
          
          celda_destino_nueva = nueva[x][y]

          es_zorro = type(celda_destino_nueva) is dict and celda_destino_nueva['tipo'] == 'zorro'
          es_conejo = type(celda_destino_nueva) is dict and celda_destino_nueva['tipo'] == 'conejo'

          if es_zorro:
            nueva[x][y]['energia'] += gz
            edades_conejos_muertos.append(conejo['edad'])
            if (x,y) != (i,j) and (type(nueva[i][j]) is dict and nueva[i][j]['tipo'] == 'conejo'):
              nueva[i][j] = None
          elif es_conejo:
            nueva[i][j] = conejo
          else:
            if snapshot[x][y] == 'pasto':
              conejo['energia'] += gc
            nueva[x][y] = conejo
            if (x,y) != (i,j) and conejo['energia'] >= e_min and random.random() <= prc:
              nueva[i][j] = {'tipo': 'conejo', 'energia': ec, 'edad': 0}
            elif (x,y) != (i,j):
              nueva[i][j] = None


def contar_animales(snapshot, N):
  """
  Lleva un conteo de conejos y zorros en cada turno.
  """
  conejos = 0
  zorros = 0
  for i in range(N):
    for j in range(N):
      celda = snapshot[i][j]
      if type(celda) is dict and celda['tipo'] == 'conejo':
        conejos += 1
      elif type(celda) is dict and celda['tipo'] == 'zorro':
        zorros += 1
  return conejos, zorros


def simular_turno(N, grilla_inicial, turnos_totales, e_min, prz, prc, ez, ec, gc, gz, pp, edades_zorros_muertos, edades_conejos_muertos, animar=True):
  """
  Simula un turno utilizando las funciones creadas.
  """
  grilla = copy.deepcopy(grilla_inicial)
  for turno in range(turnos_totales):
    conejos, zorros = contar_animales(grilla, N)
    if animar:
      print('\n' * 50)
      print('-' * 50)
      print(f'Turno: {turno}  |  🐇  Conejos: {conejos}  |  🦊  Zorros: {zorros}')
      print('-' * 50)
      imprimir_grilla(grilla)
      time.sleep(0.2)
    if conejos == 0:
      if animar:
        print('=' * 50)
        print('Los conejos se extinguieron.')
      break
    elif zorros == 0:
      if animar:
        print('=' * 50)
        print('Los zorros se extinguieron.')
      break
    elif turno == turnos_totales - 1 and animar:
      print('=' * 50)
      print('Se alcanzó el límite de 200 turnos.')
    
    snapshot = copy.deepcopy(grilla)
    crecer_pasto(snapshot, grilla, pp, N)
    mover_y_reproducir_zorros(snapshot, grilla, edades_zorros_muertos, e_min, prz, ez, gz, N)
    mover_y_reproducir_conejos(snapshot, grilla, edades_conejos_muertos, e_min, prc, ec, gc, gz, N)
    
  return grilla, edades_zorros_muertos, edades_conejos_muertos