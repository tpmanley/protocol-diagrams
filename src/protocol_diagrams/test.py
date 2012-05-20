import requests

r = requests.post("http://127.0.0.1:5000/protocol", data={"message":"""name = Cell IOMMU Page table entry
field[0:1] = Page protection
field[2] = Coherence required
field[3:4] = Storage ordering
field[5:51] = RPN
field[52:63] = IOID
""", "api_version":"1"})
print r.text

