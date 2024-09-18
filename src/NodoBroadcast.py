import simpy
import time
from Nodo import *
from Canales.CanalBroadcast import *

# La unidad de tiempo
TICK = 1


class NodoBroadcast(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, mensaje=None):
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.mensaje = mensaje

    def broadcast(self, env):
        ''' Algoritmo de Broadcast. Desde el nodo distinguido (0)
            vamos a enviar un mensaje a todos los demás nodos.'''
        data="sus"
        if self.id_nodo == 0:
            self.canal_salida.envia(data,self.vecinos)
            yield env.timeout(TICK)
        while (True):
            mensaje = yield self.canal_entrada.get()
            if data == self.mensaje:
                self.canal_salida.envia(mensaje,self.vecinos)
    

