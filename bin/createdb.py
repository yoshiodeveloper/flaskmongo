# -*- encoding: utf-8 -*-

"""
Script para criar o DB e dados iniciais de aeroportos e voos.
"""

import csv

from pymongo import MongoClient

from flaskmongo.config import MONGO_DB, MONGO_URI
from flaskmongo.utils import normalize_text


def main():
    msg = '### Atenção! ###\nTodos so dados nas collection "airports" e "flights" no DB "%s" serão permanentemente apagados.\nDeseja continuar? (s/n)' % (MONGO_URI)
    res = input(msg)
    if res != 's':
        return
    
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]

    airports = []

    print('Removendo collection "airports" (se houver).')
    db.airports.drop()

    print('Removendo collection "flights" (se houver).')
    db.flights.drop()

    with open('./airport_compact.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            '''
            0 - Airport ID 	Unique OpenFlights identifier for this airport.
            1 - Name 	Name of airport. May or may not contain the City name.
            2 - City 	Main city served by airport. May be spelled differently from Name.
            3 - Country 	Country or territory where airport is located. See countries.dat to cross-reference to ISO 3166-1 codes.
            4 - IATA 	3-letter IATA code. Null if not assigned/unknown.
            5 - ICAO 	4-letter ICAO code. Null if not assigned.
            6 - Latitude 	Decimal degrees, usually to six significant digits. Negative is South, positive is North.
            7 - Longitude 	Decimal degrees, usually to six significant digits. Negative is West, positive is East.
            8 - Altitude 	In feet.
            9 - Timezone 	Hours offset from UTC. Fractional hours are expressed as decimals, eg. India is 5.5.
            10 - DST 	Daylight savings time. One of E (Europe), A (US/Canada), S (South America), O (Australia), Z (New Zealand), N (None) or U (Unknown). See also: Help: Time
            11 - Tz database time zone 	Timezone in "tz" (Olson) format, eg. "America/Los_Angeles".
            12 - Type 	Type of the airport. Value "airport" for air terminals, "station" for train stations, "port" for ferry terminals and "unknown" if not known. In airports.csv, only type=airport is included.
            13 - Source 	Source of this data. "OurAirports" for data sourced from OurAirports, "Legacy" for old data not matched to OurAirports (mostly DAFIF), "User" for unverified user contributions. In airports.csv, only source=OurAirports is included.
            '''
            _id = row[0].strip()
            name = row[1].strip()
            city = row[2].strip()
            country = row[3].strip()
            searchable = normalize_text('%s %s' % (city, name))
            searchable = '%s;%s' % (searchable, _id)
            airports.append({
                '_id': _id,
                'name': name,
                'city': city,
                'country': country,
                'searchable': searchable
            })
    total = len(airports) ** 2
    cnt = 0
    for a in airports:
        print('Adicionando na collection "airports":', a['searchable'])
        db.airports.insert(a)
        for b in airports:
            cnt += 1
            if a['_id'] == b['_id']:
                continue
            doc = {
                'from_airport': a,
                'to_airport': b,
                'available': True
            }
            if cnt % 1000 == 0:
                print('    %d/%d - Inserindo voos...' % (cnt, total))
            db.flights.insert(doc)
    print('Criando índice em "searchable" na colletion "airports"')
    db.airports.create_index('searchable')
    print('Criando índice em "from_airport.searchable" na colletion "flights"')
    db.flights.create_index('from_airport.searchable')
    print('Criando índice em "to_airport.searchable" na colletion "flights"')
    db.flights.create_index('to_airport.searchable')
    print('Finalizado')

if __name__ == '__main__':
    main()