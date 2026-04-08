from __future__ import annotations
import urllib.request, urllib.parse, urllib.error
import ssl
import datetime
import re
import logging
import traceback

logging.basicConfig(level=logging.ERROR)

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

cotizacion_url = 'https://www.bna.com.ar/Cotizador/DescargarPorFecha?RadioButton=on&filtroEuroDescarga=0&filtroDolarDescarga=1&fechaDesde={desde}&fechaHasta={hasta}&id=billetes&descargar='

class FechaCotizacion:
           
    def __init__(self, fecha_string: str, usar_dias_previos=False):
        cantidad_de_dias_previos = 5
        parts = fecha_string.split('/')
        if len(parts) != 3:
            raise Exception(f"\033[91mInvalid date format: '{fecha_string}'. Expected format: dd/mm/aaaa (e.g. 5/3/2026 or 05/03/2026)\033[0m")
        day_str, month_str, year_str = parts
        try:
            day = int(day_str)
            month = int(month_str)
            year = int(year_str)
        except ValueError:
            raise Exception(f"\033[91mInvalid date: '{fecha_string}'. Day, month and year must be numbers. Expected format: dd/mm/aaaa\033[0m")
        try:
            self.fecha = datetime.date(year, month, day)
        except ValueError:
            raise Exception(f"\033[91mInvalid date: '{fecha_string}'. Please enter a valid date in format dd/mm/aaaa\033[0m")
        self.fecha_original = self.fecha
        if usar_dias_previos:
            self.fecha = self.fecha - datetime.timedelta(days=cantidad_de_dias_previos)
    
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

        show_data_in_columns: str = input("Show results for Spreasheets? Y/y for Yes, other key for No:")

        if from_date.es_mayor(to_date):
            raise Exception("From date should be lesser than To date")

        url = cotizacion_url.format(desde=from_date.encoded(), hasta=to_date.encoded())
        try:
            response = urllib.request.urlopen(url, context=ssl_context)
        except urllib.error.URLError as e:
            raise Exception(f"\033[91mError connecting to BNA: {e.reason}\033[0m")
        except urllib.error.HTTPError as e:
            raise Exception(f"\033[91mHTTP error from BNA: {e.code} {e.reason}\033[0m")
        fechas_y_cotizaciones = list()
        fecha_desde_encontrada = False

        for line in response:
            parts = line.decode().strip().split(';')
            if len(parts) != 4:
                print('Line with invalid format: ', line)
            fecha, compra, venta, libre = parts

            venta = venta.replace('.', ',')

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
            print(f'{fecha}  ${venta}')

        print('\n')
        print(f'Cantidad de fechas encontradas: {len(fechas_y_cotizaciones)}')
        print(f'Suma de Ventas: ${suma_ventas}')
        promedio = 0 if len(fechas_y_cotizaciones) == 0 else round(suma_ventas / len(fechas_y_cotizaciones), 2)
        print(f'El valor promedio de Venta en el período es: ${promedio}')

        if show_data_in_columns.lower() == 'y':
            print('\n')
            # to copy in excel
            for fecha, venta in fechas_y_cotizaciones:
                print(f'{fecha}')
            for fecha, venta in fechas_y_cotizaciones:
                print(f'{venta}')

        input('Press any key to continue.')
        
    except Exception:
        logging.error("Something went wrong:\n%s", traceback.format_exc())
        input('Press any key to continue.')

main()
