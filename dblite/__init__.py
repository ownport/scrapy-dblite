#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   simple library for stroring python dictionaries in sqlite database
#
__author__ = 'Andrey Usov <https://github.com/ownport/scrapy-dblite>'
__version__ = '0.2.1'

import os
import inspect
import sqlite3

from dblite.sql import WhereBuilder
from urlparse import urlparse


# the list of supported backends
SUPPORTED_BACKENDS = ['sqlite',]

# how many items will be returned by one SQL request. 
# Used in Storage()._get_all()
ITEMS_PER_REQUEST = 1000

class DuplicateItem(Exception):
    pass


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
        self._fields = dict()
        #self._fieldnames = None

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
        self._conn.row_factory = self._dict_factory

        # sqlite cursor
        self._cursor = self._conn.cursor()
        # autocommit data after put()
        self._autocommit = autocommit
        # commit counter increased every time after put without commit()
        self._commit_counter = 0 

        self._create_table(self._table)

    @staticmethod
    def _dict_factory(cursor, row):
        ''' factory for sqlite3 to return results as dict
        '''
        d = {}
        for idx, col in enumerate(cursor.description):
            if col[0] == 'rowid':
                d['_id'] = row[idx]
            else:
                d[col[0]] = row[idx]
        return d

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
        if not self._fields:
            if self._item_class is not None:
                for m in inspect.getmembers(self._item_class):
                    if m[0] == 'fields' and isinstance(m[1], dict):
                        self._fields = m[1]
                if not self._fields:
                    raise RuntimeError('Unknown item type, no fields: %s' % self._item_class)
            else:
                raise RuntimeError('Item class is not defined, %s' % self._item_class)
        return self._fields.keys()

    def _create_table(self, table_name):
        ''' create sqlite's table for storing simple dictionaries
        '''
        if self.fieldnames:
            sql_fields = []
            for field in self._fields:
                if field != '_id':
                    if 'dblite' in self._fields[field]:
                        sql_fields.append(' '.join([field, self._fields[field]['dblite']]))
                    else:
                        sql_fields.append(field)
            sql_fields = ','.join(sql_fields)
            SQL = 'CREATE TABLE IF NOT EXISTS %s (%s);' % (table_name, sql_fields)
            try:
                self._cursor.execute(SQL)
            except sqlite3.OperationalError, err:
                raise RuntimeError('Create table error, %s, SQL: %s' % (err, SQL))

    def get(self, criteria=None):
        ''' returns items selected by criteria
        
        If the criteria is not defined, get() returns all items.
        '''
        if criteria is None:
            return self._get_all()
        else:
            return self._get_with_criteria(criteria)

    def _get_all(self):
        ''' return all items
        '''
        rowid = 0
        while True:
            SQL_SELECT_MANY = 'SELECT rowid, * FROM %s WHERE rowid > ? LIMIT ?;' % self._table
            self._cursor.execute(SQL_SELECT_MANY, (rowid, ITEMS_PER_REQUEST))
            items = self._cursor.fetchall()
            if len(items) == 0:
                break
            for item in items:
                rowid = item['_id']
                yield self._item_class(item)

    def _get_with_criteria(self, criteria):
        ''' returns items selected by criteria
        ''' 
        SQL = "SELECT rowid,* FROM %s" % self._table
        WHERE = WhereBuilder().parse(criteria)
        if WHERE:
            SQL = ' '.join((SQL, 'WHERE', WHERE, ';'))
        else:
            SQL = ''.join((SQL, ';'))

        self._cursor.execute(SQL)
        for item in self._cursor.fetchall():
            yield self._item_class(item)


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
        if isinstance(item, self._item_class):
            self._put_one(item)
        elif isinstance(item, (list, tuple)):
            self._put_many(item)
        else:
            raise RuntimeError('Unknown item(s) type, %s' % type(item))

    def _put_one(self, item):
        ''' store one item in database
        '''
        values = [v for k, v in item.items() if k != '_id']

        # check if Item is new => update it
        if '_id' in item:
            fieldnames = ','.join(['%s=?' % f for f in item if f != '_id'])
            values.append(item['_id'])
            SQL = 'UPDATE %s SET %s WHERE rowid=?;' % (self._table, fieldnames)
        # new Item
        else:
            fieldnames = ','.join([f for f in item if f != '_id'])
            fieldnames_template = ','.join(['?' for f in item if f != '_id'])
            SQL = 'INSERT INTO %s (%s) VALUES (%s);' % (self._table, fieldnames, fieldnames_template)
        try:
            self._cursor.execute(SQL, values)
        except sqlite3.OperationalError, err:
            raise RuntimeError('Item put() error, %s, SQL: %s, values: %s' % (err, SQL, values) )
        except sqlite3.IntegrityError:
            raise DuplicateItem('Duplicate item, %s' % item)
        self._do_autocommit()        

    def _put_many(self, items):
        ''' store items in sqlite database
        '''
        for item in items:
            if not isinstance(item, self._item_class):
                raise RuntimeError('Items mismatch for %s and %s' % (self._item_class, type(item)))
            self.put(item)

    def delete(self, criteria=None, _all=False):
        ''' delete dictionary(ies) in sqlite database
        
        _all = True - delete all items
        '''
        if isinstance(criteria, self._item_class):
            criteria = {'_id': criteria['_id']}

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
        SQL = 'SELECT count(*) as count FROM %s;' % self._table
        self._cursor.execute(SQL)
        return int(self._cursor.fetchone()['count'])

    def commit(self):
        ''' commit changes
        '''
        self._conn.commit()

    def close(self):
        ''' close database
        '''
        self._conn.close()

        
