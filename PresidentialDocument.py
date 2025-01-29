import json
import logging
from pathlib import Path
import requests

logger = logging.getLogger(__name__)

class PresidentialDocument:
    def __init__(self, doc_number, pdf, pub_date, title, doc_type):
        self.document_number = doc_number
        self.pdf_url = pdf
        self.publication_date = pub_date
        self.title = title
        self.summary = None
        self.doc_type = doc_type
    
    def __str__(self):
        return "Document #" + self.document_number + ": " + self.title

    def get_url(self):
        return "json_objects/" + self.doc_type + "_objects/" + self.document_number + ".json"

    def save(self, api_key=None):
        try:
            if not Path(self.get_url()).exists():
                self.summarize(api_key)
                
                with open("logs/" + self.doc_type + "_log.txt", "a") as log:
                    log_url = "./json_objects/" + self.doc_type + "_objects/" + self.document_number + ".json\n"
                    log.write(log_url)
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
        url = "https://kagi.com/api/v0/summarize"
        headers = {'Authorization': f'Bot '+ api_key}
        params = {
            "url": self.pdf_url,
            "summary_type": "summary",
            "engine": "cecil"
        }
        try:
            results = requests.post(url=url, headers=headers, params=params)
            summary = results.json()["data"]["output"]
            self.summary = summary
            logging.info("AI Summary call set for " + str(self))
        except:
            logging.info("AI Summary call failed")