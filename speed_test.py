import timeit
import re
from pdb import set_trace
from sm import DictNode
import cjson
import psyco
psyco.full ()


####################
# TEST PROPERTIES
####################
ITERATIONS = 1
REPEAT = 5 

####################
# IMPORT REGEX AND PARSED MESSAGE
###################
from test_msg import msg
from test_regex import msg_regex

####################
# CREATE TEST DATA
####################
try:
    regex = re.compile('^%s$' % msg_regex )
    if not regex.match(msg): raise Exception("improperly regex")
except: pass
node, _ = DictNode.create_from_string(msg, 0)
if not node.matches(msg, 0): raise Exception("DictNode doesn't matches message")

def test_cjson():
    ret = cjson.decode(msg)
    if not ret:
        raise Exception

def test_sm():
    m, _ = node.matches(msg, 0)
    if not m:
        raise Exception
    ret = node.create_obj(msg)

def test_regex():
    m = regex.match(msg)
    if not m:
        raise Exception

def fire_test (name, extra_imports = None, repeat = REPEAT, iterations = ITERATIONS, SHOW_VALUES = 3):
    ''' fires given test function '''
    imports = 'from __main__ import %s' % name
    if extra_imports: imports += ',' + ','.join(extra_imports)
    t = timeit.Timer('%s()' % name, imports)
    print '%s:\t%s'% (name, sorted(t.repeat (repeat, iterations))[:SHOW_VALUES])

def do_tests():
#    fire_test ('test_regex', ['msg', 'regex',])
    fire_test ('test_cjson', ['msg', 'cjson',])
    fire_test ('test_sm', ['msg', 'node', ])



do_tests ()
