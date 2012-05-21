import requests

def main():
    r = requests.post("http://127.0.0.1:5000/protocol", data={"message":"""name = Cell IOMMU Page table entry
    field[0:7] = Page
    field[8:15] = Cache
    """, "api_version":"1"})
    print r.text

