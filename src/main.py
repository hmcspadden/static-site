from copy_static import copy_static
from generate_page import *
import logging
import sys
logger = logging.getLogger(__name__)
basepath = sys.argv[1]

def main():
    logging.basicConfig(filename='static.log', level=logging.DEBUG)
    logger.info("Logging Started")
    copy_static("./static/", f"{basepath}docs/")
    generate_pages_recursive(f"./content/", "./template.html", f"{basepath}docs/")
    logger.info("Logging Finished")

main()