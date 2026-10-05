import os
import shutil
import logging
logger = logging.getLogger(__name__)

def copy_static(source_directory: str, target_directory: str) -> None:
    if not os.path.exists(source_directory):
        raise Exception("Source directory not found")

    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)
    os.mkdir(target_directory)


    directory = os.listdir(source_directory)
    for item in directory:
        if not os.path.isfile(source_directory + str(item)):
            copy_static(f"{source_directory}{str(item)}/", f"{target_directory}{str(item)}/")
        else:
            logger.debug(shutil.copy(source_directory + str(item), target_directory + str(item)))