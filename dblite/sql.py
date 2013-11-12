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


class WhereBuilder(object):
    ''' SQL WHERE Builder
    '''
    def __init__(self):
        '''__init__
        '''
        self._sql = ''

    def parse(self, params):
        ''' parse parameters and return SQL 
        
        params is dictionary
        '''
        if not isinstance(params, dict):
            return ''

        if len(params) == 0:
            return ''        
        
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
        sql = ' AND '.join(selectors).strip()  
        modifiers_sql = ' '.join(modifiers).strip()
        if modifiers_sql:
            sql = ' '.join([sql, modifiers_sql]).strip()
        return sql
                
    def _logical(self, operator, params):
        ''' 
        $and:   joins query clauses with a logical AND returns all items 
                that match the conditions of both clauses
        $or:    joins query clauses with a logical OR returns all items 
                that match the conditions of either clause.
        '''

        if isinstance(params, dict):
            result = ["(%s)" % self.parse(dict([(k, v),])) for k,v in params.items()]
        elif isinstance(params, (list, tuple)):
            result = ["(%s)" % self.parse(v) for v in params]
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

            
