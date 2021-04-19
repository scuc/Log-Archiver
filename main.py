import datetime
import json
import logging
import logging.config
import os
import yaml

from time import localtime, strftime


import config as cfg

logger = logging.getLogger(__name__)

config = cfg.get_config()
script_root = config['paths']['script_root']


def set_logger():
    """
    Setup logging configuration
    """
    path = os.path.join(script_root, 'logging.yaml')

    with open(path, 'rt') as f:
        config = yaml.safe_load(f.read())

    # get the file name from the handlers, append the date to the filename. 
        for i in (config["handlers"].keys()):
            if 'filename' in config['handlers'][i]:
                log_filename = config["handlers"][i]["filename"]
                base, extension = os.path.splitext(log_filename)
                today = datetime.datetime.today()
                log_filename = "{}_{}{}".format(base,
                                                today.strftime("%Y%m%d"),
                                                extension)
                config["handlers"][i]["filename"] = log_filename
            else:
                print("+++++++++++++++ ERROR STARTING LOG FILE ++++++++++++++++")

        logger = logging.config.dictConfig(config)

    return logger


def main(): 
    """
    Script will run on the 1st of the month at 00:00:00AM, walk all the directories in a given
    source path, for any subdirectories named "_logs" it will create a ZIP archive of the daily logs
    from the previous month. 
    """

    date_start = str(strftime('%A, %d. %B %Y %I:%M%p', localtime()))

    start_msg = f"\n\
    ==================================================================================\n\
                 - Start - {date_start} \n\
    ==================================================================================\n\
   "

    logger.info(start_msg)



    
def complete_msg(media_summary):

    date_end = str(strftime('%A, %d. %B %Y %I:%M%p', localtime()))


    complete_msg = f"\n\
    ================================================================================\n\
                 - Complete - {date_end} \n\
    ================================================================================\n\
    "

    logger.info(complete_msg)

    return


if __name__ == '__main__':
    set_logger()
    main()