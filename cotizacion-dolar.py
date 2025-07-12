import urllib.request, urllib.parse
import datetime

cotizacion_url = 'https://www.bna.com.ar/Cotizador/DescargarPorFecha?RadioButton=on&filtroEuroDescarga=0&filtroDolarDescarga=1&fechaDesde={desde}&fechaHasta={hasta}&id=billetes&descargar='

def get_dates():
    from_date_string = input("Enter From date dd/mm/aaaa: ")
    day,month,year = from_date_string.split('/')
    from_date = datetime.date(int(year), int(month), int(day))

    to_date_string = input("Enter To date dd/mm/aaaa:")
    day,month,year = to_date_string.split("/")
    to_date = datetime.date(int(year), int(month), int(day))

    if from_date > to_date:
        raise Exception("From date should be lesser than To date")

    from_encoded  = urllib.parse.quote(from_date.strftime('%d/%m/%Y'), safe='')
    to_encoded = urllib.parse.quote(to_date.strftime('%d/%m/%Y'), safe='')

    return from_encoded, to_encoded

try:

    from_encoded, to_encoded = get_dates()
    url = cotizacion_url.format(desde=from_encoded, hasta=to_encoded)
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
