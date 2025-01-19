
import logging
import requests
import sys
from ExecOrder import ExecOrder

logger = logging.getLogger(__name__)

def process_exec_order(exec_object):
    exec_order = ExecOrder(
                    exec_object["document_number"],
                    exec_object["pdf_url"],
                    exec_object["publication_date"],
                    exec_object["title"]
                )
    exec_order.save()
    return exec_order

def main(date):
    url = "https://federalregister.gov/api/v1/documents.json"
    params = {
        "conditions[presidential_document_type][]": "executive_order",
        "conditions[publication_date][gte]": date
    }

    results = requests.get(url=url, params=params)

    try:
        if results.json()["count"]:
            for result in results.json()["results"]:
                exec_order = process_exec_order(result)
    except:
        logging.info("error parsing fedregister result")

if __name__=="__main__":
    logging.basicConfig(
        filename='logs/full_log.log',
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info('Hourly fedreg script started')
    try:
        date = sys.argv[1]
        logging.info("Date requested: " + date)
        main(date)
    except:
        logging.info("Argument not provided")
    logging.info('Fedreg API run completed')