# SQL builder
#
# idea was taken from http://docs.mongodb.org/manual/reference/operator/nav-query/
import re

RE_LIKE = re.compile(r'^/(?P<RE_LIKE>.+)/$')
RE_REGEXP = re.compile(r'^r/(?P<RE_REGEXP>.+)/$')

'''
SUPPORTED_OPERATORS = (
    # comparison
    '$gt', '$gte', '$in', '$lt', '$lte', '$ne', '$nin',
)
'''

# logical
LOGICAL_OPERATORS = ( '$or', '$and', )

# Query modifiers
QUERY_MODIFIERS = ( '$orderby', )


class SQLBuilder(object):
    ''' SQLBuilder
    '''
    def __init__(self, table, params):
        '''__init__
        table   -
        params  - is dictionary
        '''
        self._table = table
        self._selectors = ''
        self._modifiers = ''

        self._selectors, self._modifiers = self._parse(params)

    def select(self, fields=['rowid', '*'], offset=None, limit=None):
        ''' return SELECT SQL
        '''
        # base SQL
        SQL = 'SELECT %s FROM %s' % (','.join(fields), self._table)
        
        # selectors
        if self._selectors:
            SQL = ' '.join([SQL, 'WHERE', self._selectors]).strip()
        
        # modifiers
        if self._modifiers:
            SQL = ' '.join([SQL, self._modifiers])

        # limit
        if limit is not None and isinstance(limit, int):
            SQL = ' '.join((SQL, 'LIMIT %s' % limit))

        # offset
        if (limit is not None) and (offset is not None) and isinstance(offset, int):
            SQL = ' '.join((SQL, 'OFFSET %s' % offset))

        return ''.join((SQL, ';'))

    def delete(self):
        ''' return DELETE SQL
        '''
        SQL = 'DELETE FROM %s' % self._table
        if self._selectors:
            SQL = ' '.join([SQL, 'WHERE', self._selectors]).strip()
        
        return SQL

    def _parse(self, params):
        ''' parse parameters and return SQL 
        '''
        if not isinstance(params, dict):
            return None, None

        if len(params) == 0:
            return None, None

        selectors = list()
        modifiers = list()
        
        for k in params.keys():

            if k in LOGICAL_OPERATORS:
                selectors.append(self._logical(k, params[k]))

            elif k in QUERY_MODIFIERS:
                modifiers.append(self._modifier(k, params[k]))

            else:
                if k == '_id':
                    selectors.append("rowid%s" % (self._value_wrapper(params[k])))
                else:
                    selectors.append("%s%s" % (k, self._value_wrapper(params[k])))

        _selectors = ' AND '.join(selectors).strip()
        _modifiers = ' '.join(modifiers).strip()
        return _selectors, _modifiers 
                
    def _logical(self, operator, params):
        ''' 
        $and:   joins query clauses with a logical AND returns all items 
                that match the conditions of both clauses
        $or:    joins query clauses with a logical OR returns all items 
                that match the conditions of either clause.
        '''

        result = list()
        if isinstance(params, dict):
            for k,v in params.items():
                selectors, modifiers = self._parse(dict([(k, v),]))
                result.append("(%s)" % selectors) 
        elif isinstance(params, (list, tuple)):
            for v in params:
                selectors, modifiers = self._parse(v)
                result.append("(%s)" % selectors)
        else:
            raise RuntimeError('Unknow parameter type, %s:%s' % (type(params), params))

        if operator == '$and':
            return ' AND '.join(result)
        elif operator == '$or':
            return ' OR '.join(result)
        else:
            raise RuntimeError('Unknown operator, %s' % operator)        

    def _modifier(self, operator, params):
        ''' 
        $orderby:   sorts the results of a query in ascending (1) or descending (-1) order.
        '''

        if operator == '$orderby':
            order_types = {-1: 'DESC', 1: 'ASC'}
            if not isinstance(params, dict):
                raise RuntimeError('Incorrect parameter type, %s' % params) 
            return 'ORDER BY %s' % ','.join(["%s %s" % (p, order_types[params[p]]) for p in params])
        else:
            raise RuntimeError('Unknown operator, %s' % operator)        
    
    def _value_wrapper(self, value):
        ''' wrapper for values 
        '''
        if isinstance(value, (int, float,)):
            return '=%s' % value
        elif isinstance(value, (str, unicode)):
            value = value.strip()
            # LIKE
            if RE_LIKE.match(value):
                return ' LIKE %s' % repr(RE_LIKE.match(value).group('RE_LIKE'))
            # REGEXP
            elif RE_REGEXP.match(value):
                return ' REGEXP %s' % repr(RE_REGEXP.search(value).group('RE_REGEXP'))
            else:            
                return '=%s' % repr(value)
        elif value is None:
            return ' ISNULL'

            
