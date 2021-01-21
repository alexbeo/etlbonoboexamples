import paramiko
import logging
import datetime
import os.path
import imaplib
import email
import os


def extract_files_from_imap4(
        imap_server: str,
        login: str,
        password: str,
        load_data_dir: str,
):
    print("- подключаемся к ", imap_server)
    mail = imaplib.IMAP4_SSL(imap_server)
    print("-- логинимся")
    mail.login(login, password)
    mail.list()
    print("-- подключаемся к inbox")
    mail.select("inbox")
    print("-- получаем UID последнего письма")
    result, data = mail.search(None, 'FROM', '"izvod-noreply@otpsrbija.rs"')
    print('-----', result, len(data[0]))

    for num in data[0].split():
        result, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        try:
            email_message = email.message_from_string(raw_email)
            print(raw_email)
        except TypeError:
            email_message = email.message_from_bytes(raw_email)

        print("--- нашли письмо от: ", email.header.make_header(email.header.decode_header(email_message['From'])))
        print(type(email.header.make_header(email.header.decode_header(email_message['From']))))
        for part in email_message.walk():
            print(part.get_content_type())
            if "application" in part.get_content_type():
                filename = part.get_filename()
                filename = str(email.header.make_header(email.header.decode_header(filename)))
                if not filename:
                    filename = "test.txt"
                print("---- нашли вложение ", filename)
                if filename.endswith('.XML'):
                    with open(os.path.join(load_data_dir, filename), 'wb') as fp:
                        fp.write(part.get_payload(decode=1))
                    print("-- удаляем письмо")
                    mail.store(num, '+FLAGS', '(\Deleted)')
                    # mail.expunge()

    mail.close()
    mail.logout()


def extract_files_from_ftp(
            hostname='',
            port=00000,
            username='',
            password='',
            dir_input='',
            dir_output=''
    ):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print('----подключаемся к ftp серверу')
            client.connect(hostname=hostname, username=username, password=password, port=port)
            sftp = client.open_sftp()
        except Exception:
            date_now = datetime.datetime.now()
            str_data_now = str(date_now) + f' Не удалось подключиться к серверу!'
            logging.error(str_data_now, exc_info=False)
        else:
            # read_files_from_dir(sftp, directory)
            ls_sftp = sftp.listdir(dir_input)
            if len(ls_sftp) > 0:
                print('------чтение данных с ftp сервера')
                for f in ls_sftp:
                    input_file_path = os.path.join(dir_input, f)
                    local_file_path = os.path.join(dir_output, f)
                    sftp.get(input_file_path, local_file_path)
                client.close()
            print('----закрыли соеденение с ftp сервером')

        return True
