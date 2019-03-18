#!/usr/bin/python
# coding: utf-8
import json

__author__ = "Xavier Chopin"
__copyright__ = "Copyright 2018, University of Lorraine"
__license__ = "ECL-2.0"
__version__ = "1.0.0"
__email__ = "xavier.chopin@univ-lorraine.fr"
__status__ = "Production"

import csv
import sys
sys.path.append(os.path.dirname(__file__) + '/../../..')
from bootstrap.helpers import *

jwt = OpenLrw.generate_jwt()  # Generate a JSON Web Token for using OneRoster routes

csv_file = open('data/BAC_IC0_2018.csv', 'r')
counter = 0
with csv_file:
    has_header = csv.Sniffer().has_header(csv_file.read(1024))
    csv_file.seek(0)  # Rewind
    reader = csv.reader(csv_file, delimiter=';')

    next(reader) if has_header else None
    for row in reader:
        user_id, serie_bac, year, mention = row
        if year == '' or serie_bac == '':
            continue
        user = OpenLrw.get_user(user_id, jwt)
        if user:
            user = json.loads(user)
            user["metadata"]["bac_serie"] = serie_bac
            user["metadata"]["bac_annee"] = year
            user["metadata"]["bac_mention"] = mention

            OpenLrw.post_user(user, jwt, True)  # Replace the user with the new value
            counter += 1

    time = measure_time()

    OpenLrw.mail_server(sys.argv[0] + " executed", str(counter) + " users edited in " + measure_time() + " seconds")