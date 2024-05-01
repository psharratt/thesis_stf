#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 12:38:25 2024

@author: paulsharratt
"""

def augur_db_connect(file_path):
    """ Connects to the Augur database using the configuration from 
        config.json
            {
                "connection_string": "sqlite:///:memory:",
                "database": "xxxxx",
                "host": "xxxx.xxxx.xx",
                "password": "xxxxx",
                "port": xxxx,
                "schema": "augur_data",
                "user": "xxxx",
                "user_type": "read_only"
            }
        Returns
        -------
        engine : sqlalchemy database object
    """
    import psycopg2
    import sqlalchemy as s
    import json

    with open(file_path) as config_file:
        config = json.load(config_file)

    database_connection_string = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(config['user'], config['password'], config['host'], config['port'], config['database'])

    dbschema='augur_data'
    engine = s.create_engine(
        database_connection_string,
        connect_args={'options': '-csearch_path={}'.format(dbschema)})

    return engine