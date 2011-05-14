import unittest
from pdb import set_trace
from sm import DictNode, InvalidFormat, ContainerStringNode
from sm import StringNode, DoesNotMatch, InvalidFormat

class DictNodeTestCase(unittest.TestCase):
    def setUp(sefl):
        pass

    def test_create_from_string_good(self):
        string='{"color":"red"}'
        node, pos = DictNode.create_from_string(string, 0)
        key1, value1 = node.children[0]
        self.assertEquals(key1.value, 'color')
        self.assertEquals(key1.get_node_type(), 'String')
        self.assertEquals(value1.value, 'red')
        self.assertEquals(value1.get_node_type(), 'String')

    def test_create_from_string_recursive_dict(self):
        string='{"colors":{"front":"red","back":"blue"}}'
        node, pos = DictNode.create_from_string(string, 0)
        key1, value1 = node.children[0]
        
        self.assertEquals(key1.value, 'colors')
        self.assertEquals(key1.get_node_type(), 'String')
        self.assertEquals(value1.get_node_type(), 'Dict')

        key11, value11 = value1.children[0]

        self.assertEquals(key11.value, 'front')
        self.assertEquals(key11.get_node_type(), 'String')
        self.assertEquals(value11.value, 'red')
        self.assertEquals(value11.get_node_type(), 'String')

        key12, value12 = value1.children[1]
        self.assertEquals(key12.value, 'back')
        self.assertEquals(key12.get_node_type(), 'String')
        self.assertEquals(value12.value, 'blue')
        self.assertEquals(value12.get_node_type(), 'String')

    def test_matches(self):
        string='{"front":"red","back":"blue"}'
        node, _ = DictNode.create_from_string(string, 0)

        self.assertEquals(node.matches(string, 0), (True,len(string) - 1 ))

        # values are matched by default
        self.assertEquals(node.matches('{"front":"green","back":"blue"}', 0), (True,len('{"front":"green","back":"blue"}') -1) ) 

        self.assertEquals(node.matches('{"front":"red","left":"blue"}', 0), (False, -1)) # values are matched by default
        self.assertEquals(node.matches('{"front":"green","right":"blue"}', 0), (False, -1)) # values are matched by default
        self.assertRaises(InvalidFormat, node.matches, '"front":"red","back":"blue"}', 0)

    def test_matches_recursive_dict(self):
        string='{"colors":{"front":"red","back":"green"}}'
        node, _ = DictNode.create_from_string(string, 0)

        self.assertEquals(node.matches(string, 0), (True, len(string) - 1))
        self.assertEquals(node.matches('{"colors":{"front":"white","back":"green"}}', 0), (True, len('{"colors":{"front":"white","back":"green"}}') - 1))
        self.assertEquals(node.matches('{"names":{"front":"red","back":"green"}}', 0), (False, -1))

    def test_create_obj(sefl):
        string='{"colors":{"front":"red","back":"green"}}'
        node, _ = DictNode.create_from_string(string, 0)
        node.matches('{"colors":{"front":"red","back":"green"}}', 0)
        obj = node.create_obj(string)
    


class StringNodeTestCase(unittest.TestCase):
    def setUp(self):
        self.string = '"some string"'
        self.node, _ = StringNode.create_from_string(self.string, 0)

    def test_create_from_string_good(self):
        string = '"some string here"'
        node, pos = StringNode.create_from_string(string, 0)
        self.assertEqual(node.value, "some string here")
        self.assertEqual(pos, len(string) - 1)

        string = '   "hey"'
        node, pos = StringNode.create_from_string(string, 3)
        self.assertEqual(node.value, "hey")
        self.assertEqual(pos, 7)


    def test_create_from_string_does_not_match(self):
        for string in ('"', "'"):
            self.assertRaises(InvalidFormat, StringNode.create_from_string, '"', 0)

    def test_matches_ok(self):
        self.assertTrue(self.node.matches(self.string)[0])
    
    def test_matches_raises_InvalidFormat(self):
        self.assertRaises(InvalidFormat, self.node.matches, 'some string')

    def test_matches_does_not_match(self):
        self.assertEqual((False, -1), self.node.matches('"another string"'))

    def test_find_string(self):
        string = '"test"   '
        value, index = StringNode.find_string(string, 0)
        self.assertEqual(value, "test")
        self.assertEqual(5, index)

class ContainerStringNodeTest(unittest.TestCase):
    def setUp(self):
        self.node, _ = ContainerStringNode.create_from_string('"some not important text"', 0)
        self.text = '"some text here"'
        self.text_length =len(self.text)

    def test_matches(self):
        matches, pos = self.node.matches(self.text, 0)
        self.assertEqual((matches, pos), (True, self.text_length - 1))
    
    def test_create_obj(self):
        matches, pos = self.node.matches(' "one two three"', 1)
        value = self.node.create_obj(' "one two three"')
        self.assertEqual(value, "one two three")


if __name__=="__main__":
    unittest.main()
