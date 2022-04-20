import logging
import os
import re
import zipfile
from datetime import datetime
from pathlib import Path
from time import localtime, strftime

import config as cfg

logger = logging.getLogger(__name__)

config = cfg.get_config()
logpath_list = config["paths"]["logs_path_list"]


def zip_log(logpath, log, date):
    """
    Compress the list of log files into a zip archive, then delete the logs that were archived.
    """

    os.chdir(logpath)

    compression = zipfile.ZIP_DEFLATED
    log_filename = os.path.basename(log)
    logfile_date = re.split(r"_|\W+", log_filename)

    if not int(logfile_date[1]) == ValueError:
        logfile_year = logfile_date[1][:4]
        logefile_month = logfile_date[1][4:6]
        zip_filename = f"{logfile_year}-{logefile_month}_logs.zip"

        filename_msg = f"zip filename: {zip_filename}"
        logger.info(filename_msg)

    else:
        log.error(f"ValueError for the date on: {log_filename}")
        return ValueError

    try:
        zippath = Path(logpath, zip_filename)

        with zipfile.ZipFile(zippath, mode="a", compression=compression) as zipObj:

            zipObj.write(Path(log))
            zipObj.close()

            print("")
            print(f"{log_filename} WAS WRITTEN TO THE ZIP {zip_filename}")
            print("")

            archive = zipfile.ZipFile(zippath, mode="r")
            print("***********  NOW TESTINGZ ZIP *************")
            test_result = archive.testzip()

            if test_result == None:
                zip_sucess_msg = f"{zip_filename} test sucessful."
                logger.info(zip_sucess_msg)
                archive_namelist_msg = f"Archived log: {log_filename}"
                logger.info(archive_namelist_msg)
                delete_logs(logpath, log)
                return
            else:
                zip_fail_msg = f"Failed to zip {log_filename} in archive: {zip_filename}. \n test results: {test_result}"
                logger.info(zip_fail_msg)
                return

    except zipfile.BadZipfile as error:
        logger.error(error)
        return


def delete_logs(logpath, log):
    """
    Delete all log files in the given list of logs.
    """

    logpath = Path(log)
    logpath.unlink()
    print(f"LOG DELETED: {log}")

    return


if __name__ == "__main__":
    get_logs()
