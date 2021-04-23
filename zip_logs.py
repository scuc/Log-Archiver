
import logging
import os
import zipfile

from datetime import datetime
from pathlib import Path
from time import localtime, strftime

import config as cfg

logger = logging.getLogger(__name__)

config = cfg.get_config()
logs_list = config['paths']['logs_path_list']


def get_date(): 

    """
    get todays date and time, use the month value to build a list of log files.
    """

    today = datetime.today()
    year = today.strftime('%Y')
    month = today.strftime('%m')
    day = today.strftime('%d')

    return year, month, day


def log_checks():
    """
    Check the given log folder paths and create a list of all the log files in each. 
    Only list the log files with a datestamp that contains the previous month.
    Pass the list of log files to the 'zip_logs' function and create a zip archive. 
    """

    year, month, day = get_date()
    prev_month = int(month) - 1
    
    if len(str(prev_month)) != 2: 
        prev_month = "0"+ str(prev_month)

    for logpath in logs_list:
        log_files = sorted(
                            [
                            x for x in os.listdir(logpath) 
                            if x.endswith('.log')
                            if x[-8:-6] == str(prev_month)
                            ]
                        )

        zip_logs(logpath, log_files, prev_month)


def zip_logs(logpath, log_files, prev_month):
    """
    Compress the list of log files into a zip archive, then delete the logs that were archived.
    """
    os.chdir(logpath)

    compression = zipfile.ZIP_DEFLATED

    year, month, day = get_date()

    zip_filename = f"{year}-{prev_month}_logs.zip"

    with zipfile.ZipFile(zip_filename, 'w', compression=compression) as zipObj:

        for log in log_files:
            zipObj.write(log)

    try:
        archive = zipfile.ZipFile(zip_filename, 'r')
        test_result = archive.testzip()

        if test_result == None: 
            zip_sucess_msg = f"{zip_filename} test sucessful."
            logger.info(zip_sucess_msg)
            archive_namelist_msg = f"Archived logs: {archive.namelist()}"
            logger.info(archive_namelist_msg)
            delete_logs(logpath, log_files)
            return
        else: 
            zip_fail_msg = f"{zip_filename} test failed. \n test results: {test_result}"
            logger.info(zip_fail_msg)
            return 

    except zipfile.BadZipfile as e: 
        logger.error(e)


def delete_logs(logpath, log_files):
    """
    Delete all log files in the given list of logs.
    """
    for log in log_files: 
        logpath = Path(log)
        logpath.unlink()

    return 

if __name__ == '__main__':
    log_checks()
