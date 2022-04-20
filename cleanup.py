import logging
import os
from datetime import date, datetime, timedelta
from pathlib import Path
from time import localtime, strftime

import config as cfg
import logs_check as check
import zip_logs as ziplogs

logger = logging.getLogger(__name__)

config = cfg.get_config()
logpath_list = config["paths"]["logs_path_list"]


def daily_cleanup(date):

    for logpath in logpath_list:
        print(f"LOG PATH: {logpath}")
        logfile_list = check.get_logs(logpath, date)

        if logfile_list == []:
            continue
        else:
            for log in logfile_list:
                ziplogs.zip_log(logpath, log, date)


# def get_dir_name(year,month,day):

#     if not int(month) - 1 == 0:
#         dir_name = f"{}-{"
