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
        # verificamos que nustros canales no sean vacios
        if self.canales == []:
            return
        # verificamos que canales pertenecen a los vecinos y
        # mandamos el mensaje a cada vecino
        for canal in range(len(self.canales)):
            if canal in vecinos:
                self.canales[canal].put(mensaje)

    def crea_canal_de_entrada(self):
        '''
        Creamos un canal de entrada
        '''
        canal_entrada = simpy.Store(self.env, capacity=self.capacidad)
        self.canales.append(canal_entrada)
        return canal_entrada
