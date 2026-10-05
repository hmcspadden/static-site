from copy_static import copy_static
from generate_page import *
import logging
logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(filename='static.log', level=logging.DEBUG)
    logger.info("Logging Started")
    copy_static("./static/", "./public/")
    generate_pages_recursive("./content/", "./template.html", "./public/")
    logger.info("Logging Finished")

main()