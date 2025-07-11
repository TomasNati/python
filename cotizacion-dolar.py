import urllib.request, urllib.parse
import datetime

cotizacion_url = 'https://www.bna.com.ar/Cotizador/DescargarPorFecha?RadioButton=on&filtroEuroDescarga=0&filtroDolarDescarga=1&fechaDesde={desde}&fechaHasta={hasta}&id=billetes&descargar='

try:
    from_date_string = input("Enter From date dd/mm/aaaa: ")
    day,month,year = from_date_string.split('/')
    from_date = datetime.date(int(year), int(month), int(day))

    to_date_string = input("Enter To date dd/mm/aaaa:")
    day,month,year = to_date_string.split("/")
    to_date = datetime.datetime(int(year), int(month), int(day))

    from_encoded  = urllib.parse.quote(from_date.strftime('%d/%m/%Y'), safe='')
    to_encoded = urllib.parse.quote(to_date.strftime('%d/%m/%Y'), safe='')

    url = cotizacion_url.format(desde=from_encoded, hasta=to_encoded)
    response = urllib.request.urlopen(url)

    for line in response:
        line_length = len(line)
        print(line.decode().strip())
    
except Exception as e:
    print("There was an error getting the value: ", e)
