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
		self.fields = []
		
class Field(object):
	def __init__(self, name, start_bit, end_bit=None):
		self.name = name
		self.start_bit = start_bit
		if not end_bit:
			end_bit = start_bit
		self.end_bit = end_bit

def parse_string(string):
	messages = []
	
	def name_def_matched(s, loc, toks):
		messages.append(Message(toks.message_name))
		
	def field_def_matched(s, loc, toks):
		messages[-1].fields.append(Field(toks.field_name, toks.field_start, toks.field_end))
	
	name_def = Literal("name") + "=" + restOfLine("message_name")
	name_def.setParseAction(name_def_matched)
	field_def = Literal("field") + Literal("[") + Word(nums)("field_start") + Optional(Literal(":") + Word(nums)("field_end")) + "]" + "=" + restOfLine("field_name")
	field_def.setParseAction(field_def_matched)
	message_def = name_def + field_def * (1, None) 

	message_def.parseString(string)
	
	return messages

