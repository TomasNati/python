from __future__ import annotations
import urllib.request, urllib.parse
import datetime
import logging
import traceback

logging.basicConfig(level=logging.ERROR)


cotizacion_url = 'https://www.bna.com.ar/Cotizador/DescargarPorFecha?RadioButton=on&filtroEuroDescarga=0&filtroDolarDescarga=1&fechaDesde={desde}&fechaHasta={hasta}&id=billetes&descargar='

class FechaCotizacion:
           
    def __init__(self, fecha_string: str, usar_dias_previos=False):
        try:
            cantidad_de_dias_previos = 5
            day,month,year = fecha_string.split('/')
            self.fecha = datetime.date(int(year), int(month), int(day))
            self.fecha_original = datetime.date(int(year), int(month), int(day))
            if usar_dias_previos:
                self.fecha = self.fecha - datetime.timedelta(days=cantidad_de_dias_previos)
        except Exception as e:
            raise("There was an error creating the date: ", e)
    
    def encoded(self):
        return urllib.parse.quote(self.fecha.strftime('%d/%m/%Y'), safe='')
    
    def es_mayor(self, other_fecha: FechaCotizacion):
        return self.fecha > other_fecha.fecha
    
    def menor_a_fecha_original(self, other_fecha: FechaCotizacion):
        return self.fecha_original > other_fecha.fecha

    def igual_a_fecha_original(self, other_fecha: FechaCotizacion):
        return self.fecha_original == other_fecha.fecha
    
    def mayor_a_fecha_original(self, other_fecha: FechaCotizacion):
        return self.fecha_original < other_fecha.fecha


def main():
    try:

        from_date_string = input("Enter From date dd/mm/aaaa: ")
        from_date = FechaCotizacion(from_date_string, True)

        to_date_string = input("Enter To date dd/mm/aaaa:")
        to_date = FechaCotizacion(to_date_string)

        if from_date.es_mayor(to_date):
            raise Exception("From date should be lesser than To date")

        url = cotizacion_url.format(desde=from_date.encoded(), hasta=to_date.encoded())
        response = urllib.request.urlopen(url)
        fechas_y_cotizaciones = list()
        fecha_desde_encontrada = False

        for line in response:
            parts = line.decode().strip().split(';')
            if len(parts) != 4:
                print('Line with invalid format: ', line)
            fecha, compra, venta, libre = parts

            if not '/' in fecha: continue

            if (not fecha_desde_encontrada):
                fecha_nueva = FechaCotizacion(fecha)
                if from_date.menor_a_fecha_original(fecha_nueva):
                    fechas_y_cotizaciones = [(fecha, int(venta.split(",")[0]))]
                elif from_date.igual_a_fecha_original(fecha_nueva):
                    fecha_desde_encontrada = True
                    fechas_y_cotizaciones = [(fecha, int(venta.split(",")[0]))]
                elif from_date.mayor_a_fecha_original(fecha_nueva):
                    fecha_desde_encontrada = True
                    fechas_y_cotizaciones.append((fecha, int(venta.split(",")[0])))

            else:
                fechas_y_cotizaciones.append((fecha, int(venta.split(",")[0])))

        suma_ventas = 0
        for fecha, venta in fechas_y_cotizaciones:
            suma_ventas += venta
            print(f'{fecha} - ${venta}')

        print('\n')
        print(f'Cantidad de fechas encontradas: {len(fechas_y_cotizaciones)}')
        print(f'Suma de Ventas: ${suma_ventas}')
        promedio = 0 if len(fechas_y_cotizaciones) == 0 else round(suma_ventas / len(fechas_y_cotizaciones), 2)
        print(f'El valor promedio de Venta en el período es: ${promedio}')
        
    except Exception:
        logging.error("Something went wrong:\n%s", traceback.format_exc())


main()
