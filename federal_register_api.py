
import json
import logging
import os
import requests
import sys
from ExecOrder import ExecOrder

logger = logging.getLogger(__name__)

def process_exec_order(exec_object, api_key=None):
    exec_order = ExecOrder(
                    exec_object["document_number"],
                    exec_object["pdf_url"],
                    exec_object["publication_date"],
                    exec_object["title"]
                )
    exec_order.save(api_key)
    return exec_order

def audit(api_key=None):
    for root, dirs, files in os.walk("./order_objects"):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as f:
                    json_object = json.loads(f.read())
                    order = object.__new__(ExecOrder)
                    order.__dict__ = json_object
                    order.save(api_key)
            except:
                logging.info("Audit failed for: " + file_path)
    

def main(date, api_key=None):
    url = "https://federalregister.gov/api/v1/documents.json"
    params = {
        "conditions[presidential_document_type][]": "executive_order",
        "conditions[publication_date][gte]": date
    }

    results = requests.get(url=url, params=params)

    try:
        if results.json()["count"]:
            for result in results.json()["results"]:
                exec_order = process_exec_order(result, api_key)
    except:
        logging.info("error parsing fedregister result")
    
    audit(api_key)

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