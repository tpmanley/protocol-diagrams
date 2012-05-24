from pyparsing import *
# integer_types = Group(Optional("U") + Optional(Word("BL")) + "INT" + Word(nums) + "()")
# greet = "class" + Word( alphas ) + "(BaseMessage):" + (Word(alphas) + "=" + integer_types) * (1, None)
# hello = """class Message(BaseMessage):
    # type = ULINT8()
    # length = ULINT8()
    # payload = Payload()
    # """
# print hello, "->", greet.searchString( hello )

class Protocol(object):
    def __init__(self, endianness="little", row_width=16, field_resolution="bit", show_header=True):
        self.endianness = endianness
        self.row_width = row_width
        self.field_resolution = field_resolution
        self.show_header = show_header
        self.messages = []
        
class Message(object):
    def __init__(self, name):
        self.name = name
        self.fields = []

class Field(object):
    def __init__(self, name, width):
        self.name = name
        self.width = width

def parse_string(string):
    """Parses a string for a protocol definition.
    
    A protocol definition contains an optional protocol section, followed by one or
    more message sections.
    
    All the values in the protocol section are optional. The protocol section is defined
    using the following format::
    
        [protocol]
        endianness = little | big # optional, default = little
        row-width = <number of bits in a row> # optional, default = 16
        field-resolution = bit | byte # optional, default = bit
        show-header = true | false # optional, default = true
    
    Messages can be defined in the string using the following format::
    
        [message <id>] # <id> must be unique for each message in the protocol
        name = <message name> # optional
        <fields> # one or more fields are required
        
    Fields can be defined in the following ways::
    
        field[<start bit/byte>:<end bit/byte>] = <field name>
        field[<bit/byte>] = <field name>
    """
    p = Protocol()
    
    def protocol_def_matched(s, loc, toks):
        if toks.endianness:
            p.endianness = str(toks.endianness)
        if toks.row_width:
            p.row_width = int(toks.row_width)
        if toks.field_resolution:
            p.field_resolution = int(toks.field_resolution)
        if toks.show_header:
            p.show_header = bool(toks.show_header)

    def name_def_matched(s, loc, toks):
        p.messages.append(Message(toks.message_name))

    def field_def_matched(s, loc, toks):
        if toks.field_end:
            width = int(toks.field_end) - int(toks.field_start) + 1
        else:
            width = 1
        p.messages[-1].fields.append(Field(toks.field_name, width))

    field_def = Literal("field") + Literal("[") + Word(nums)("field_start") + \
                Optional(Literal(":") + Word(nums)("field_end")) + Literal("]") + \
                Literal("=") + restOfLine("field_name")
    field_def.setParseAction(field_def_matched)


    name_def = Literal("name") + "=" + restOfLine("message_name")
    name_def.setParseAction(name_def_matched)
    message_def = name_def + field_def * (1, None)

    message_def.parseString(string)

    return p

if __name__ == "__main__":
    parse_string("""name = Cell IOMMU Page table entry
field[0:1] = Page protection
field[2] = Coherence required
field[3:4] = Storage ordering
field[5:51] = RPN
field[52:63] = IOID
""")