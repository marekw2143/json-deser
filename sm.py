from pdb import set_trace

OBJ_CODE = False # flag indicating whether good class oriented code will be used or fast but rather difficult to maintain one

STRING_NODE = 0
DICT_NODE = 1

class DoesNotMatch(Exception):
    """
    Raised when given string doesn't isn't matched by given node
    """

class InvalidFormat(Exception):
    pass

class ValuesStorage(object):
    """
    Stroring values in fast fashion
    """

class Supervisor(object):
    """
    Manages creating ParseTree and generating deserialized objects from string
    """

    def __init__(self):
        """
        """

    def parse_string(self, string):
        """
        Returns deserialized object
        """

    def generate_parse_tree(self, string):
        """
        Generates parse tree from given string
        """
        for pos, char in enumerate(string):
            for cls in (DictNode, ListNode, StringNode):
                if char == cls.start_char:
                    return cls.create_from_string(string, pos)
                
class BaseNode(object):
    """
    Parent of all objects that can be in tree
    """

    def matches(self, string, starting_pos, value_container):
        """ 
        Parses given string against beeing current node representation
        For each variable value in string is added to value container
        Raises DoesNotMatch when string doesn't match this Node
        """
        raise NotImplementedError

    @classmethod
    def create_from_string(cls, string, string_pos):
        """
        Creates instance of node on the basis of given string
        Returns BaseNode subclass, position on string where BaseNode subclass representation stops
        """
        raise NotImplementedError

    def create_cached_object(self):
        """
        Creates python object representign given node with values ready to be filled
        """
        raise NotImplementedError

    def fill_cached_object(self, cached_obj):
        #for value in self.values_mapping:
        #    cached_obj[value.key] = value.value
        raise NotImplementedError

    def get_node_type(self):
        """
        Returns string code of node
        """
        return self.node_type

    def __eq__(self, other):
        raise NotImplementedError

class NodeContainer(BaseNode):
    """
    Contains child nodes
    """

class StringNode (BaseNode):
    start_char = '"'
    def get_node_type(self):return 'String'
    def __init__(self, val):
        self.value = val
        self.node_type = STRING_NODE

        self.start_pos, self.end_pos = None, None
        self.string = None

    def create_cached_object(self):
        return '#' * 100

    def fill_cached_object(self, obj):
        obj[:] = self.string[self.start_pos: self.end_pos]

    @classmethod
    def find_string(cls, string, pos):
        """
        Returns quoted string value, and pos of last " character
        """
        if string[pos] != '"': raise InvalidFormat
        index = string.index('"', pos + 1)
        #self.starting_pos = pos
        #self.end_pos = index
        return string[pos+1:index], index
        
    @classmethod
    def _find_string(cls, string, pos):
        """
        Returns quoted string value, and pos of last " character
        string - searched string
        pos - starting position of search
        """
        idx = pos + 1
        while 1:
            if string[idx] == '"':
                index = idx
                break
            idx += 1
        return string[pos+1:index], index

    @classmethod
    def find_string_and_compare(cls, string, pos, matched):
        """
        Checks whether @matched is equal to the text defined in string between @pos and next " character
        if is equal - returns position of last " character
        otherwise - raises Exception
        """
        idx = pos + 1
        while 1:
            if string[idx] == '"':
                index = idx
                break
            idx += 1
        if string[pos+1:index] == matched: return index
        raise Exception("sth went wrong")


    @classmethod
    def create_from_string(cls, string, pos):
        try:
            val = ''
            if string[pos] != cls.start_char: raise InvalidFormat
            pos += 1
            while 1:
                char = string[pos]
                if char == cls.start_char: return cls(val), pos
                val+= char
                pos += 1
            raise InvalidFormat
        except:
            raise InvalidFormat

    def matches(self, string, pos=0):
        if string[pos] != '"': raise InvalidFormat
        idx = pos + 1
        while 1:
            if string[idx] == '"':
                index = idx
                break
            idx += 1
        if string[pos+1:index] == self.value: return True, index
        return False, -1

class ContainerStringNode(StringNode):
    """
    Saves data about stored value during match, provides method to extract value
    """
    def matches(self, string, pos = 0):
        idx = pos + 1
        while 1:
            if string[idx] == '"':
                index = idx
                break
            idx += 1
        self.cache = (pos, idx)
        return True, index

    def create_obj(self, string):
        return string[self.cache[0] + 1:self.cache[1]]
        





class DictNode (NodeContainer):
    """
    Dictionary in parse tree
    """

    def get_node_type(self):
        return 'Dict'

    start_char = '{'
    end_char = '}'
    key_value_separator = ':'
    key_value_start = StringNode.start_char
    pair_separator = ','

    def get_next_string_end(self, string, pos):
        """ returns pos of next string end"""
        idx = pos + 1
        while 1:
            if string[idx] == '"': return idx
            idx += 1

    
    def create_cached_object(self):
        pass
        

    def __init__(self, children, cached_pattern):
        self.children = children # list - order of existance is important
        self.node_type = DICT_NODE
        # ("key", value) where value is instance of BaseNode

        self._values = [None] * 100 
        self._values_index = 0#-1 

        self.cached_pattern = cached_pattern
        self.cached_objects = [dict(self.cached_pattern)] * 1000 * 1000 # make 100 copies of cache

        self.string_positions = [None] * 1000 * 1000
        self.string_positions_index = 0

    def matches(self, string, pos):
        string_positions_index = 0
        string_positions = self.string_positions
        fstr = StringNode.find_string
        if string[pos] != self.start_char: raise InvalidFormat
        pos += 1
        iteration = 0
        length = len(self.children)
        while 1:#for key, value in self.children:
            # FIRST - check key
            key, value = self.children[iteration]
            if OBJ_CODE:
                mkey, pos = fstr(string, pos)
                if mkey != key.value: return False, -1
            else:
                index = None
                idx = pos + 1
                while 1:
                    if string[idx] == '"':
                       index = idx
                       break
                    idx += 1
                if string[pos+1:idx] != key.value: return False, -1
                pos = index

            pos += 1

            if string[pos] != self.key_value_separator: raise InvalidFormat
            pos += 1

            # SECOND - check value
            if value.node_type == STRING_NODE:
                start_pos = pos
                # find position of end of value string (last " ) - save its position in pos
                if OBJ_CODE:
                    matches, pos = value.matches(string, pos) # check if value matches (it caches value)
                    if not matches: return False, -1
                else:
                    idx = pos + 1
                    while 1:
                        if string[idx] == '"':	
                            pos = idx
                            break
                        idx += 1

                string_positions[string_positions_index] = (start_pos, pos)
                string_positions_index += 1 

            elif value.node_type == DICT_NODE:
                matches, pos = value.matches(string, pos)
                if not matches: return False, -1
            else: raise NotImplementedError
            pos += 1
            if iteration < length - 1:
                if string[pos] != self.pair_separator: raise InvalidFormat
                pos +=1 
            iteration += 1
            if iteration == length: break
        if string[pos] != self.end_char: raise InvalidFormat
        return True, pos

    def __get_cache_inst(self):
        return self.cached_pattern

    def create_obj(self, string):
        ret = self.__get_cache_inst()
        if OBJ_CODE:
            for key, value in self.children:
                ret[key.value] = value.create_obj(string)
        else:
            index = 0
            child = self.children
            for key, value in child:
                if value.node_type == DICT_NODE:
                    ret[key.value] = value.create_obj(string)
                else:
                    start_pos, end_pos = self.string_positions[index]
                    ret[key.value] = string[start_pos : end_pos]
        return ret

    @classmethod
    def create_from_string(cls, string, pos):
        children = []
        if string[pos] != cls.start_char: raise InvalidFormat
        pos += 1
        while 1:
            char = string[pos]
            if char == cls.key_value_start:# get key-value pair
                key, value, pos = cls.__get_key_value(string, pos)
                pos += 1
                children.append((key, value))
                if string[pos] != cls.pair_separator: # else - was separator - get nex key --> continue :)
                    if cls.__check_end(string, pos): 
                        patt = cls.__create_cached_pattern(children)
                        return cls(children, patt), pos
            else: raise DoesNotMatch
            pos += 1

    @classmethod
    def __create_cached_pattern(cls, children):
        ret = {}
        mapping = { STRING_NODE: "#" * 100,
                    DictNode: {}}
        for key, value in children:
            ret[key.value] = mapping[key.node_type]
        return ret

    @classmethod
    def __get_key_value(cls, string, pos):
        """
        Returns tuple containint key, value, finished_position
        pos started definition at given pos
        """
        key, pos = cls.__get_key(string, pos)
        pos += 1
        if string[pos] != cls.key_value_separator: raise InvalidFormat
        pos += 1
        if string[pos] == StringNode.start_char:
            value, pos = ContainerStringNode.create_from_string(string, pos)
            return key, value, pos
        elif string[pos] == DictNode.start_char:
            value, pos = DictNode.create_from_string(string, pos)
            return key, value, pos
        

    @classmethod
    def __get_key(cls, string, pos):
        if string[pos] == StringNode.start_char: 
            return StringNode.create_from_string(string, pos)

    @classmethod
    def __check_end(cls, string, pos):
        """
        Checks whether it's end of dictionary definition
        """
        if string[pos] != cls.end_char: raise InvalidFormat
        return True

class ListNode (NodeContainer):
    """
    List in parse tree
    """
    start_char = '['


