
import requests
import json

class ExecOrder:
    def __init__(self, doc_number, pdf, pub_date, title):
        self.document_number = doc_number
        self.pdf_url = pdf
        self.publication_date = pub_date
        self.title = title
    
    def __str__(self):
        return "Executive Order #" + self.document_number + ": " + self.title

    def save(self):
        filename = "order_objects/" + self.document_number + ".json"
        with open(filename, "w+") as file:
            json.dump(vars(self), file, indent=4)

def process_exec_order(exec_object):
    exec_order = ExecOrder(
                    exec_object["document_number"],
                    exec_object["pdf_url"],
                    exec_object["publication_date"],
                    exec_object["title"]
                )
    exec_order.save()
    return exec_order

def main():
    url = "https://federalregister.gov/api/v1/documents.json"
    params = {
        "conditions[presidential_document_type][]": "executive_order",
        "conditions[publication_date][gte]": "2025-01-14"
    }

    results = requests.get(url=url, params=params)

    try:
        if results.json()["count"]:
            for result in results.json()["results"]:
                exec_order = process_exec_order(result)
                print(exec_order)
    except:
        print("error parsing fedregister result")

if __name__=="__main__":
    main()