#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   simple library for stroring python dictionaries in sqlite database
#


import os
import inspect
import sqlite3

from dblite.sql import WhereBuilder
from urlparse import urlparse


SUPPORTED_BACKENDS = ['sqlite',]


def open(item, uri, autocommit=False):
    ''' open sqlite database by uri and Item class
    '''
    return Storage(item, uri, autocommit)


class Storage(object):
    ''' Storage
    
    store simple dictionaries in sqlite database
    '''
    def __init__(self, item, uri, autocommit=False):
        ''' __init__
        
        item        - Scrapy item class
        uri         - URI to sqlite database, sqlite://<sqlite-database>:<table>
        autocommit  - few variations are possible: boolean (False/True) or integer
                     True - autocommit after each put()
                     False - no autocommit, commit() only manual
                     [integer] - autocommit after N[integer] put()
        '''
        self._item_class = item
        self._fieldnames = set()
        if item is not None:
            fields = [m[1] for m in inspect.getmembers(item) if m[0] == 'fields']
            if len(fields) != 1:
                raise RuntimeError('Unknown item type, no fields: %s' % item)
            self._fieldnames = set(fields[0].keys())
        else:
            raise RuntimeError('Item class is not defined, %s' % item)

        database, table = self.parse_uri(uri)
        # database file
        if database:
            self._db = database
        else:
            raise RuntimeError('Empty database name, "%s"' % database)
        # database table
        if table:
            self._table = table.split(' ')[0]
        else:
            raise RuntimeError('Empty table name, "%s"' % table)
        
        # sqlite connection
        try:
            self._conn = sqlite3.connect(database)
        except sqlite3.OperationalError, err:
            raise RuntimeError("%s, database: %s" % (err, database))
            
        # sqlite cursor
        self._cursor = self._conn.cursor()
        # autocommit data after put()
        self._autocommit = autocommit
        # commit counter increased every time after put without commit()
        self._commit_counter = 0 

        self._create_table(self._table, self._fieldnames)

    @staticmethod
    def parse_uri(uri):
        ''' parse URI
        '''
        if not uri or uri.find('://') <= 0:
            raise RuntimeError('Incorrect URI definition: {}'.format(uri))
        backend, rest_uri = uri.split('://')
        if backend not in SUPPORTED_BACKENDS:
            raise RuntimeError('Unknown backend: {}'.format(backend))
        database, table = rest_uri.split(':')

        return database, table

    @property
    def fieldnames(self):
        ''' return fieldnames
        '''
        return self._fieldnames

    def _create_table(self, table_name, fieldnames):
        ''' create sqlite's table for storing simple dictionaries
        '''
        if not fieldnames:
            raise RuntimeError('Item fieldnames are not defined')
        sql_fields = ','.join([f for f in fieldnames])
        SQL = 'CREATE TABLE IF NOT EXISTS %s (%s);' % (table_name, sql_fields)
        try:
            self._cursor.execute(SQL)
        except sqlite3.OperationalError, err:
            raise RuntimeError('%s, SQL: %s' % (err, SQL))

    def get(self, criteria=None):
        ''' returns dicts selected by criteria
        
        If the criteria is not defined, get() returns all documents.
        '''
        SQL = "SELECT rowid,* FROM %s" % self._table
        WHERE = WhereBuilder().parse(criteria)
        if WHERE:
            SQL = ' '.join((SQL, 'WHERE', WHERE, ';'))
        else:
            SQL = ''.join((SQL, ';'))

        self._cursor.execute(SQL)
        for r in self._cursor.fetchall():
            _id = r[0]
            fields = [f.split(' ')[0] for f in self._fieldnames]
            dict_res = dict([(fields[i], v) for i, v in enumerate(r[1:])])
            yield (_id, self._item_class(dict_res))
        
    def _do_autocommit(self):
        ''' perform autocommit
        '''
        # commit()
        self._commit_counter += 1
        # autocommit as boolean
        if isinstance(self._autocommit, bool) and self._autocommit:
            self.commit()
            self._commit_counter = 0
        
        # autocommit as counter
        elif isinstance(self._autocommit, int) and self._autocommit > 0:
            if (self._commit_counter % self._autocommit) == 0:
                self.commit()
                self._commit_counter = 0

    def put(self, item):
        ''' store item in sqlite database
        '''
        # prepare SQL
        if not isinstance(item, self._item_class):
            raise RuntimeError('Items mismatch for %s and %s' % (self._item_class, type(item)))

        fieldnames = ','.join([v for v in item.keys()])
        fields_template = ','.join(['?' for f in item])
        SQL = 'INSERT INTO %s (%s) VALUES (%s);' % (self._table, fieldnames, fields_template)
        try:
            self._cursor.execute(SQL, [v for v in item.values()])
        except sqlite3.OperationalError, err:
            raise RuntimeError('%s, SQL: %s, values: %s' % (err, SQL, [v for v in item.values()]) )
        self._do_autocommit()        

    def put_many(self, items):
        ''' store items in sqlite database
        '''
        for item in items:
            self.put(item)

    def delete(self, criteria=None, _all=False):
        ''' delete dictionary(ies) in sqlite database
        
        _all = True - delete all items
        '''
        SQL = 'DELETE FROM %s' % self._table
        WHERE = WhereBuilder().parse(criteria)
        if WHERE:
            SQL = ' '.join((SQL, 'WHERE', WHERE, ';'))
        elif not _all:
            raise RuntimeError('Criteria is not defined')
        
        if _all:    
            SQL = ''.join((SQL, ';'))
        
        self._cursor.execute(SQL)
                
    def __len__(self):
        ''' return size of storage
        '''
        SQL = 'SELECT count(*) FROM %s;' % self._table
        self._cursor.execute(SQL)
        return int(self._cursor.fetchone()[0])

    def commit(self):
        ''' commit changes
        '''
        self._conn.commit()

    def close(self):
        ''' close database
        '''
        self._conn.close()

        
