# SQL builder
#
# idea was taken from http://docs.mongodb.org/manual/reference/operator/nav-query/

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
        
        result = ''
        
        for k in params.keys():
            
            if k in LOGICAL_OPERATORS:
                result = ' '.join((result, self._logical(k, params[k])))
            else:
                if k == '_id':
                    result = ' '.join((result, "rowid=%s" % (self._value_wrapper(params[k]) )))
                else:
                    result = ' '.join((result, "%s=%s" % (k, self._value_wrapper(params[k]) )))
            
        return result.strip()
                
    def _logical(self, operator, params):
        ''' 
        $and:   joins query clauses with a logical AND returns all items 
                that match the conditions of both clauses
        $or:    joins query clauses with a logical OR returns all items 
                that match the conditions of either clause.
        '''
        if not isinstance(params, dict):
            raise RuntimeError('Parameters should be defined via python dictionary, params: %s' % params)

        result = ["(%s)" % self.parse(dict([(k, v),])) for k,v in params.items()]

        if operator == '$and':
            return ' AND '.join(result)
        elif operator == '$or':
            return ' OR '.join(result)
        else:
            raise RuntimeError('Unknown operator, %s' % operator)        
    
    def _value_wrapper(self, value):
        ''' wrapper for values 
        '''
        if isinstance(value, (int, float, )):
            return value
        elif isinstance(value, (str, unicode)):
            return '"%s"' % value

            
