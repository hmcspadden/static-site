import os
import shutil
import logging
logger = logging.getLogger(__name__)

def copy_static(source_directory: str, target_directory: str) -> None:
    if not os.path.exists(source_directory):
        raise Exception("Source directory not found")

    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)
    split_path = target_directory.split("/")
    path_so_far = ""
    for i in range(len(split_path) - 1):
        path_so_far += split_path[i] + "/"
        if not os.path.exists(path_so_far):
            os.mkdir(path_so_far)


    directory = os.listdir(source_directory)
    for item in directory:
        if not os.path.isfile(source_directory + str(item)):
            copy_static(f"{source_directory}{str(item)}/", f"{target_directory}{str(item)}/")
        else:
            logger.debug(shutil.copy(source_directory + str(item), target_directory + str(item)))