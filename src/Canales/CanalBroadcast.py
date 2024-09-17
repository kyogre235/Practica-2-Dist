import simpy
from Canales.Canal import Canal


class CanalBroadcast(Canal):
    '''
    Clase que modela un canal, permite enviar mensajes one-to-many.
    '''

    def __init__(self, env, capacidad=simpy.core.Infinity):
        self.env = env
        self.capacidad = capacidad
        self.canales = []

    def envia(self, mensaje, vecinos):
        '''
        Envia un mensaje a los canales de salida de los vecinos.
        '''
        # Tu código aquí
        for vecino in vecinos:
        # Obtiene el canal de entrada del vecino
            vecino.canal_entrada = vecino.getCanal_entrada()
        # Envia el mensaje al canal de entrada del vecino
            yield self.env.process(vecino.canal_entrada.put(mensaje))

    def crea_canal_de_entrada(self):
        '''
        Creamos un canal de entrada
        '''
        canal_entrada = simpy.Store(self.env, capacity=self.capacidad)
        self.canales.append(canal_entrada)
        return canal_entrada
