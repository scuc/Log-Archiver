import json
import logging
import logging.config
import os
from datetime import date, datetime
from time import localtime, strftime

import yaml

import cleanup as cleanup
import config as cfg
import zip_logs as ziplogs

logger = logging.getLogger(__name__)

config = cfg.get_config()


def set_logger():
    """
    Setup logging configuration
    """
    path = "/Users/admin/Scripts/Log_Archiver/logging.yaml"

    with open(path, "rt") as f:
        config = yaml.safe_load(f.read())

        # get the file name from the handlers, append the date to the filename.
        for i in config["handlers"].keys():
            if "filename" in config["handlers"][i]:
                log_filename = config["handlers"][i]["filename"]
                base, extension = os.path.splitext(log_filename)
                today = datetime.today()
                log_filename = "{}_{}{}".format(
                    base, today.strftime("%Y%m%d"), extension
                )
                config["handlers"][i]["filename"] = log_filename
            else:
                continue

        logger = logging.config.dictConfig(config)

    return logger


def main():
    """
    Script will run on the 1st of the month at 00:00:00AM, for any subdirectories named "_logs" given inthe config.yaml
    it will create a ZIP archive of the daily logs from the previous month.
    """
    date_start = str(strftime("%A, %d. %B %Y %I:%M%p", localtime()))

    start_msg = f"\n\
    ==================================================================================\n\
                 Log Archiver - Start - {date_start} \n\
    ==================================================================================\n\
   "

    logger.info(start_msg)

    date = datetime.today()
    # year = date.year
    # month = date.month
    # day = date.day

    if not date.day == 1:
        cleanup.daily_cleanup(date)
    elif date.day == 1 and date.month == 1:
        date.year = date.year - 1
        cleanup.daily_cleanup(date)
    else:
        cleanup.daily_cleanup(date)

    complete_msg()


def complete_msg():

    date_end = str(strftime("%A, %d. %B %Y %I:%M%p", localtime()))

    complete_msg = f"\n\
    ================================================================================\n\
                 Log Archiver - Complete - {date_end} \n\
    ================================================================================\n\
    "

    logger.info(complete_msg)

    return


if __name__ == "__main__":
    set_logger()
    main()
