# SQL builder
#
# idea was taken from http://docs.mongodb.org/manual/reference/operator/nav-query/
import re

RE_LIKE = re.compile(r'^/(.+)/$')
RE_REGEXP = re.compile(r'^r/(.+)/$')

'''
SUPPORTED_OPERATORS = (
    # comparison
    '$gt', '$gte', '$in', '$lt', '$lte', '$ne', '$nin',
)
'''
# logical
LOGICAL_OPERATORS = ( '$or', '$and', )


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
        
        result = list()
        
        for k in params.keys():
            
            if k in LOGICAL_OPERATORS:
                result.append(self._logical(k, params[k]))
            else:
                if k == '_id':
                    result.append("rowid%s" % (self._value_wrapper(params[k])))
                else:
                    result.append("%s%s" % (k, self._value_wrapper(params[k])))
            
        return ' AND '.join(result).strip()
                
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
    
    def _value_wrapper(self, value):
        ''' wrapper for values 
        '''
        if isinstance(value, (int, float,)):
            return '=%s' % value
        elif isinstance(value, (str, unicode)):
            value = value.strip()
            # LIKE
            if RE_LIKE.match(value):
                return ' LIKE "%s"' % RE_LIKE.match(value).groups()
            # REGEXP
            elif RE_REGEXP.match(value):
                return ' REGEXP "%s"' % RE_REGEXP.search(value).groups()
            else:            
                return '="%s"' % value
        elif value is None:
            return ' ISNULL'

            
