from extracttasks import extract_files_from_imap4, extract_files_from_ftp
import config
import schedule
import time
import threading


def run_extract_bank_statements_task():
    extract_files_from_imap4(
        imap_server=config.IMAP_SERVER,
        login=config.MAIL_LOGIN,
        password=config.MAIL_PASSWORD,
        load_data_dir=config.ACCOUNT_STATEMENT_DIR
    )


def run_extract_blocklist_task():
    extract_files_from_ftp(
        hostname=config.HOST,
        port=config.PORT,
        username=config.USER,
        password=config.PASS,
        dir_input=config.INPUT_DIR_BLOCK_LISTS,
        dir_output=config.BLOCK_LISTS_DAILY_REPORTS
    )


def run_extract_daily_report_task():
    extract_files_from_ftp(
        hostname=config.HOST,
        port=config.PORT,
        username=config.USER,
        password=config.PASS,
        dir_input=config.INPUT_DIR_TAG_DAILY_REPORTS,
        dir_output=config.TAG_DAILY_REPORTS,
    )


def run_thread_process(job):
    run_thread = threading.Thread(target=job)
    run_thread.start()


# schedule.every().day.at('13:02').do(run_extract_bank_statements_task)
# schedule.every().day.at('13:03').do(run_extract_blocklist_task)
schedule.every().day.at('13:21').do(run_extract_daily_report_task)

while True:
    schedule.run_pending()
