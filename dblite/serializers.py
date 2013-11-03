import json
import zlib

import cPickle as pickle

# -----------------------------------------------------------------
# cPickleSerializer class
# -----------------------------------------------------------------

class cPickleSerializer(object):
    ''' cPickleSerializer 
    '''

    @staticmethod
    def dumps(v):
        ''' dumps value 
        '''
        return pickle.dumps(v)

    @staticmethod
    def loads(v):
        ''' loads value  
        '''
        return pickle.loads(v)

# -----------------------------------------------------------------
# CompressedPickleSerializer class
# -----------------------------------------------------------------

class CompressedPickleSerializer(object):
    ''' CompressedPickleSerializer 
    '''

    @staticmethod
    def dumps(v):
        ''' dumps value 
        '''
        return zlib.compress(pickle.dumps(v))

    @staticmethod
    def loads(v):
        ''' loads value  
        '''
        return pickle.loads(zlib.decompress(v))

# -----------------------------------------------------------------
# CompressedJsonSerializer class
# -----------------------------------------------------------------

class CompressedJsonSerializer(object):
    ''' CompressedJsonSerializer 
    '''

    @staticmethod
    def dumps(v):
        ''' dumps value 
        '''
        return zlib.compress(json.dumps(v))

    @staticmethod
    def loads(v):
        ''' loads value  
        '''
        return json.loads(zlib.decompress(v))


