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