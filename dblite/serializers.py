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

# -----------------------------------------------------------------
# CompressedJStrSerializer class
# -----------------------------------------------------------------

class CompressedStrSerializer(object):
    ''' CompressedStrSerializer 
    '''

    @staticmethod
    def dumps(v):
        ''' dumps value 
        '''
        if v is None:
            return None
        return zlib.compress(v)

    @staticmethod
    def loads(v):
        ''' loads value  
        '''
        if v is None:
            return None
        return zlib.decompress(v)

