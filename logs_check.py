
import logging
import os
import re 

from datetime import datetime, timedelta
from pathlib import Path

import config as cfg

logger = logging.getLogger(__name__)

config = cfg.get_config()
logpath_list = config['paths']['logs_path_list']


def check_logpaths(logpath_list):
    log_paths_list = []
    for path in logpath_list: 
        if not os.path.isdir(path):
            log.info(f"_log dir does not exist at path: {path}")
        else: 
            log_paths_list.append(path)
    
    return log_paths_list


def get_logs(logpath, date):
    """
    Check the given log folder paths and create a list of all the log files in each. 
    Only list the log files with a datestamp that contains the previous month.
    Pass the list of log files to the 'zip_logs' function and create a zip archive. 
    """

    logcheck_msg = f"Checking logs in:  {logpath}"
    logger.info(logcheck_msg)

    logfile_list = []
    yesterday = date - timedelta(1)
    log_files = os.listdir(logpath)

    for x in log_files:

        if (
            '.log' in x 
            and not '.zip' in x
            ): 
            print(f"LOG = {x}")
            log_date = re.split(r'_|\W+',x)[1]
            log_datetime = datetime(
                                    int(log_date[:4]),
                                    int(log_date[4:6]),
                                    int(log_date[6:8]),
                                    )

            if ( 
                '.log' in x 
                and log_datetime <= yesterday
                ): 
                logfile_list.append(x)
            else:
                continue
        else:
            continue


    # logfile_list = sorted(
    #                     [
    #                     os.path.join(logpath,x) for x in os.listdir(logpath) 
    #                     if '.log' in x
    #                     and len(x) >= 17
    #                     and log_datetime <= yesterday
    #                     ]
    #                 )

    logslist_msg = f"Log files found: {logfile_list} "

    return logfile_list 
    
        

if __name__ == '__main__':
    cehck_logsg