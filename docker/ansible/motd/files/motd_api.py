#!/usr/bin/env python3

import sqlite3
import datetime
import json
from flask_restful import Resource, Api, reqparse
from flask import Flask, request

DB_NAME='motd.db'

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

parser.add_argument('host_data',dest='host_data',location='form')
parser.add_argument('host_ip',dest='host_ip',location='form')

with sqlite3.connect(DB_NAME) as db_conn:
    dbc = db_conn.cursor()
    dbc.execute('CREATE TABLE IF NOT EXISTS motd (date, time, ip, hash)')

def _get_db():
    with sqlite3.connect(DB_NAME) as db_conn:
        dbc = db_conn.cursor()
        dbc.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
        dbc.execute("SELECT * FROM motd ORDER BY time;")
        ret = dbc.fetchall()
        return ret

class SetMotdData(Resource):
    def post(self):
        args = parser.parse_args()
                
        if not args.host_data:
            return 'We need JSON containing date, time, ip and date hash. Cannot proceed.'
        print(args.host_data)
        host_data = json.loads(args.host_data)
        db_data = _get_db()
        exists = False
        for row in db_data:
            if host_data['local_ip'] is row['ip']:
                exists = True

        with sqlite3.connect(DB_NAME) as db_conn:
            dbc = db_conn.cursor()
            if not exists:
                dbc.execute('INSERT INTO motd values (?, ?, ?, ?)',
                    (host_data['current_date'], host_data['current_time'], host_data['local_ip'], host_data['current_date_hash']))
            else:
                dbc.execute('UPDATE {} SET date=?, time=?, hash=? WHERE ip=?',
                    (host_data['current_date'],host_data['current_time'], host_data['current_date_hash'], host_data['local_ip']))
        return 'Data added !'

class GetMotdData(Resource):
    def get(self):
        args = parser.parse_args()
        if not args.host_ip:
            return 'We need an IP address, so we return the correct motd data for the host'

        db_data = _get_db()
        for row in db_data:
            if row['ip'] == args.host_ip:
                return json.dumps(row)
            return 'Unknown IP'


api.add_resource(SetMotdData, '/set_motd_data')
api.add_resource(GetMotdData, '/info')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
