import json
import logging

logger = logging.getLogger(__name__)

class ExecOrder:
    def __init__(self, doc_number, pdf, pub_date, title):
        self.document_number = doc_number
        self.pdf_url = pdf
        self.publication_date = pub_date
        self.title = title
        self.summary = None
    
    def __str__(self):
        return "Executive Order #" + self.document_number + ": " + self.title

    def save(self):
        filename = "order_objects/" + self.document_number + ".json"
        try:
            with open(filename, "x") as file:
                json.dump(vars(self), file, indent=4)
            logging.info("Writing " + str(self))
            with open("logs/write_log.txt", "a") as log:
                log.write(str(self)+"\n")
        except:
            logging.info("Order exists: " + str(self))
        return