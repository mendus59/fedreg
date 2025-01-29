
import json
import logging
import os
import requests
import sys
from PresidentialDocument import PresidentialDocument

logger = logging.getLogger(__name__)

def process_exec_object(exec_object, api_key=None):
    exec_object = PresidentialDocument(
                    exec_object["document_number"],
                    exec_object["pdf_url"],
                    exec_object["publication_date"],
                    exec_object["title"],
                    exec_object["object_type"]
                )
    exec_object.save(api_key)
    return exec_object

def audit(object_type, api_key=None):
    for root, dirs, files in os.walk("./json_objects/" + object_type +"_objects"):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as f:
                    json_object = json.loads(f.read())
                    order = object.__new__(PresidentialDocument)
                    order.__dict__ = json_object
                    order.save(api_key)
            except:
                logging.info("Audit failed for: " + file_path)
    

def process_objects(date, object_type, api_key=None):
    url = "https://federalregister.gov/api/v1/documents.json"
    params = {
        "conditions[presidential_document_type][]": object_type,
        "conditions[publication_date][gte]": date
    }

    results = requests.get(url=url, params=params)

    try:
        if results.json()["count"]:
            for result in results.json()["results"]:
                result["object_type"] = object_type
                exec_order = process_exec_object(result, api_key)
    except:
        logging.info("error parsing fedregister result")


def main(date, api_key=None):
    document_types = [
        "executive_order", "determination", "memorandum", 
        "notice", "proclamation", "presidential_order", "other"
    ]
    for obj_type in document_types:
        process_objects(date, obj_type, api_key)
        audit(obj_type, api_key)
    

if __name__=="__main__":
    logging.basicConfig(
        filename='logs/full_log.txt',
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info('Hourly fedreg script started')
    try:
        date = sys.argv[1]
        api_key = sys.argv[2]
        logging.info("Date requested: " + date)
        main(date, api_key)
    except:
        logging.info("Argument not provided")
    logging.info('Fedreg API run completed')