from pyparsing import *
# integer_types = Group(Optional("U") + Optional(Word("BL")) + "INT" + Word(nums) + "()")
# greet = "class" + Word( alphas ) + "(BaseMessage):" + (Word(alphas) + "=" + integer_types) * (1, None)
# hello = """class Message(BaseMessage):
    # type = ULINT8()
    # length = ULINT8()
    # payload = Payload()
    # """
# print hello, "->", greet.searchString( hello )

message = """name = Cell IOMMU Page table entry
field[0:1] = Page protection
field[2] = Coherence required
field[3:4] = Storage ordering
field[5:51] = RPN
field[52:63] = IOID
"""

class Message(object):
    def __init__(self, name):
        self.name = name
        self.width = 0
        self.fields = []

    def add_field(self, field):
        self.fields.append(field)
        self.width += field.width

class Field(object):
    def __init__(self, name, width):
        self.name = name
        self.width = width

def parse_string(string):
    messages = []

    def name_def_matched(s, loc, toks):
        messages.append(Message(toks.message_name))

    def field_def_matched(s, loc, toks):
        if toks.field_end:
            width = int(toks.field_end) - int(toks.field_start) + 1
        else:
            width = 1
        messages[-1].add_field(Field(toks.field_name, width))

    name_def = Literal("name") + "=" + restOfLine("message_name")
    name_def.setParseAction(name_def_matched)
    field_def = Literal("field") + Literal("[") + Word(nums)("field_start") + Optional(Literal(":") + Word(nums)("field_end")) + "]" + "=" + restOfLine("field_name")
    field_def.setParseAction(field_def_matched)
    message_def = name_def + field_def * (1, None)

    message_def.parseString(string)

    return messages

if __name__ == "__main__":
    parse_string(message)