from __future__ import annotations
import urllib.request, urllib.parse
import datetime

cotizacion_url = 'https://www.bna.com.ar/Cotizador/DescargarPorFecha?RadioButton=on&filtroEuroDescarga=0&filtroDolarDescarga=1&fechaDesde={desde}&fechaHasta={hasta}&id=billetes&descargar='

class FechaCotizacion:

    cantidad_de_dias_previos = 4
           
    def __init__(self, fecha_string: str):
        try:
            day,month,year = fecha_string.split('/')
            self.fecha = datetime.date(int(year), int(month), int(day))
        except Exception as e:
            raise("There was an error creating the date: ", e)
    
    def encoded(self):
        return urllib.parse.quote(self.fecha.strftime('%d/%m/%Y'), safe='')
    
    def es_mayor(self, other_fecha: FechaCotizacion):
        return self.fecha > other_fecha.fecha

def main():
    try:

        from_date_string = input("Enter From date dd/mm/aaaa: ")
        from_date = FechaCotizacion(from_date_string)

        to_date_string = input("Enter To date dd/mm/aaaa:")
        to_date = FechaCotizacion(to_date_string)

        if from_date.es_mayor(to_date):
            raise Exception("From date should be lesser than To date")

        url = cotizacion_url.format(desde=from_date.encoded(), hasta=to_date.encoded())
        response = urllib.request.urlopen(url)
        fechas_y_cotizaciones = list()

        for line in response:
            parts = line.decode().strip().split(';')
            if len(parts) != 4:
                print('Line with invalid format: ', line)
            fecha, compra, venta, libre = parts
            if not '/' in fecha: continue
            fechas_y_cotizaciones.append((fecha, int(venta.replace(',0000', ''))))

        suma_ventas = 0
        for fecha, venta in fechas_y_cotizaciones:
            suma_ventas += venta
            print(f'{fecha} - ${venta}')

        print('\n')
        promedio = round(suma_ventas / len(fechas_y_cotizaciones), 2)
        print(f'El valor promedio de Venta en el período es: ${promedio}')
        
    except Exception as e:
        print("There was an error getting the value: ", e)

main()
