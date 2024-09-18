import simpy
from Nodo import *
from Canales.CanalBroadcast import *

TICK = 1

class NodoGenerador(Nodo):
    '''Implementa la interfaz de Nodo para el algoritmo de flooding.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        
        # Atributos propios del algoritmo
        self.padre = None if id_nodo != 0 else id_nodo # Si es el nodo distinguido, el padre es el mismo 
        self.hijos = list()
        self.mensajes_esperados = len(vecinos) # Cantidad de mensajes que esperamos
    
    def genera_arbol(self, env):
        
        if self.padre == 0:
            mensaje = [self.id_nodo,"Go"]
            self.canal_salida.envia(mensaje,self.vecinos)
            yield env.timeout(TICK)
        

        while(True):
            mensaje = yield self.canal_entrada.get()
            data = mensaje[1]
            if data == "Go":
                if self.padre is None:
                    self.padre = mensaje[0]
                    self.mensajes_esperados -= 1
                    if self.mensajes_esperados == 0:
                        mensaje = [self.id_nodo,"Back"]
                        self.canal_salida.envia(mensaje,[self.padre])
                    else:
                        for vecino in self.vecinos:
                            if vecino != mensaje[0]:
                                mensaje = [self.id_nodo,"Go"]
                                self.canal_salida.envia(mensaje,[vecino])
                else:
                    mensaje = [None,"Back"]
                    self.canal_salida.envia(mensaje,[mensaje[0]])

            elif tipo == "Back":
                self.mensajes_esperados -= 1
                mensaje = yield self.canal_entrada.get()
                if mensaje[0] != None:
                    self.hijos.append(mensaje[0])
                if self.mensajes_esperados == 0:
                    if self.padre != self.id_nodo:
                        mensaje = [self.id_nodo,"Back"]
                        self.canal_salida.envia(mensaje,self.padre)
