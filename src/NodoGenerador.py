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
        
        # Si es el nodo raíz, inicia el flooding enviando un mensaje a sus vecinos
        if self.padre == 0:
            mensaje = [self.id_nodo, "Go"]
            self.canal_salida.envia(mensaje, self.vecinos)
            yield env.timeout(TICK)

        while(True):
            mensaje = yield self.canal_entrada.get()
            tipo_mensaje = mensaje[1]

            if tipo_mensaje == "Go":
                # Si el nodo no tiene padre, significa que es la primera vez que recibe el mensaje
                if self.padre is None:
                    self.padre = mensaje[0]  # Asignamos el nodo que envió "Go" como padre
                    self.mensajes_esperados -= 1

                    # Si ya no esperamos más mensajes, enviamos "Back" a nuestro padre
                    if self.mensajes_esperados == 0:
                        mensaje_back = [self.id_nodo, "Back"]
                        self.canal_salida.envia(mensaje_back, [self.padre])
                    else:
                        # Propagamos el mensaje "Go" a nuestros vecinos, excepto al que lo envió
                        for vecino in self.vecinos:
                            if vecino != mensaje[0]:
                                mensaje_go = [self.id_nodo, "Go"]
                                self.canal_salida.envia(mensaje_go, [vecino])
                else:
                    # Si ya tiene padre, rechazamos el mensaje reenviando "Back" vacío
                    mensaje_back = [None, "Back"]
                    self.canal_salida.envia(mensaje_back, [mensaje[0]])

            elif tipo_mensaje == "Back":
                self.mensajes_esperados -= 1
                # Si el mensaje es de un hijo válido, lo agregamos a la lista de hijos
                if mensaje[0] is not None and mensaje[0] != self.id_nodo:
                    self.hijos.append(mensaje[0])

                # Cuando ya no esperamos más mensajes, enviamos "Back" a nuestro padre
                if self.mensajes_esperados == 0 and self.padre is not None:
                    mensaje_back = [self.id_nodo, "Back"]
                    self.canal_salida.envia(mensaje_back, [self.padre])
