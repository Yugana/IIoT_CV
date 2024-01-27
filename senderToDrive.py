import yadisk
import os

y = yadisk.YaDisk(token="")
print(y.check_token()) # Проверьте токен

def upload_files_to_yandex_disk():
    local_directory = 'ResultLogs'
    remote_directory = 'IIOT/'

    for filename in os.listdir(local_directory):
        local_file = os.path.join(local_directory, filename)
        remote_file = os.path.join(remote_directory, filename)


        if not y.exists(remote_file): # проверяем, существует ли файл на диске
            y.upload(local_file, remote_file) # загружаем файл на диск

upload_files_to_yandex_disk()