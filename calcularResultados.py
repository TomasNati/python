class Equipo:
    def __init__ (self, nombre):
        self.nombre = nombre
        self.puntos = 0

    def sumar_puntos(self, puntos):
        self.puntos += puntos    

river = Equipo('River Plate')
monterrey = Equipo('Monterrey') 
inter = Equipo('Inter')
el_de_japon = Equipo('El de Japón')

class Partido:
    def __init__(self,equipo1: Equipo, equipo2: Equipo, goles1: int, goles2: int):
        self.equipo1 = equipo1
        self.equipo2 = equipo2  
        self.goles1 = goles1
        self.goles2 = goles2

    def es_igual(self, otro_partido: 'Partido') -> bool:
        return (self.equipo1.nombre == otro_partido.equipo1.nombre and self.equipo2.nombre == otro_partido.equipo2.nombre) or \
               (self.equipo1.nombre == otro_partido.equipo2.nombre and self.equipo2.nombre == otro_partido.equipo1.nombre)
    
    def ganandor(self) -> Equipo | None:
        if self.goles1 > self.goles2:
            return self.equipo1
        elif self.goles2 > self.goles1:
            return self.equipo2
        else:
            return None
        
class Torneo:
    def __init__(self, partidos: list[Partido]):
        self.partidos = []
        self.equipos = [river, monterrey, inter, el_de_japon]
        for partido in partidos:
            self.agregar_partido(partido)

    def agregar_partido(self, partido: Partido):
        partido__existe = False
        for p in self.partidos:
            if (p.es_igual(partido)):
                partido__existe = True
                break
        if not partido__existe:
            self.partidos.append(partido)
            ganador = partido.ganandor()
            if ganador:
                ganador.sumar_puntos(3)
            else:
                partido.equipo1.sumar_puntos(1)
                partido.equipo2.sumar_puntos(1)

    def buscar_partido(self, equipo1: Equipo, equipo2: Equipo) -> Partido | None:
        for partido in self.partidos:
            if partido.es_igual(Partido(equipo1, equipo2, 0, 0)):
                return partido
        return None
    
    def mostrar_tabla_posiciones(self) -> None:
        max_length_name = max(len(equipo.nombre) for equipo in self.equipos)
        tabla = "Tabla de Posiciones:\n"
        for equipo in self.equipos:
            tabla += f"{equipo.nombre.ljust(max_length_name)} : {equipo.puntos} puntos\n"
        print(tabla)
    

    

partidos: list[Partido] =[
    Partido(river, el_de_japon, 3, 1) # River Plate 3 vs El de Japón 1
    , Partido(monterrey, inter, 1, 1) # Monterrey 1 vs Inter 1
    , Partido(river, monterrey, 0, 0), # River Plate 0 vs Monterrey 0
    Partido(inter, el_de_japon, 2, 1) # Inter 2 vs El de Japón 1
]

torneo = Torneo(partidos)

torneo.mostrar_tabla_posiciones()

