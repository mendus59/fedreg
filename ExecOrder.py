import json
import logging
from pathlib import Path
import requests

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

    def get_url(self):
        return "order_objects/" + self.document_number + ".json"

    def save(self, api_key=None):
        try:
            if not Path(self.get_url()).exists():
                self.summarize(api_key)
                
                with open("logs/write_log.txt", "a") as log:
                    log.write(str(self)+"\n")
                with open(self.get_url(), "x") as file:
                    json.dump(vars(self), file, indent=4)
                logging.info("Object has been created: " + str(self))
            else:
                with open(self.get_url(), "r+") as file:
                    data = file.read()
                    if not json.loads(data)["summary"]:
                        self.summarize(api_key)
                        file.seek(0)
                        file.truncate()
                        json.dump(vars(self), file, indent=4)
                        logging.info("Updated summary of " + str(self))

        except:
            logging.info("Error processing file: " + str(self))
        return

    def summarize(self, api_key=None):
        url = "https://api.apyhub.com/ai/summarize-documents/url"
        headers = {
            "apy-token": api_key,
            "Content-Type": "application/json"
        }
        data = {
            "url": self.pdf_url
        }
        try:
            results = requests.post(url=url, headers=headers, json=data)
            summary = results.json()["data"]["summary"]
            self.summary = summary
            logging.info("AI Summary call set for " + str(self))
        except:
            logging.info("AI Summary call failed")