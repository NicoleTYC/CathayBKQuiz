import logging
import pathlib
import datetime
import os

dir_path = project_path = str(pathlib.Path(__file__).parent.absolute()) + r"\logs"

serial = "{:%Y-%m-%d-%H%M%S}".format(datetime.datetime.now())
filename = serial + '.log'

def create_logger(log_name = 'Log' , log_folder = '' ):

    logging.captureWarnings(True)  
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    my_logger = logging.getLogger(log_name)  
    my_logger.setLevel(logging.INFO)

    if not os.path.exists(dir_path + log_folder):
        os.makedirs(dir_path + log_folder)
    fileHandler = logging.FileHandler(dir_path + log_folder + '/' + filename, 'w', 'utf-8')
    fileHandler.setFormatter(formatter)
    my_logger.addHandler(fileHandler)
    

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.INFO)
    consoleHandler.setFormatter(formatter)
    my_logger.addHandler(consoleHandler)
    if len(my_logger.handlers) > 1: 
        my_logger.handlers.pop()

    return my_logger