import datetime


class Logging():

    def now_time(self):
        return str(datetime.datetime.now())

    def __init__(self):
        now_time    = self.now_time().replace(':','-')
        self.file_name   = 'Logs/Log {}.txt'.format(now_time[0:18])

        with open(self.file_name, 'x') as log_file:
            log_file.write('[INFO][{}] Started Logging \n'.format(self.now_time()[0:18]))
            log_file.write('[INFO][{}] Log File Name: {} \n'.format(self.now_time()[0:18], self.file_name))
            
            print('[INFO][{}] Started Logging \n'.format(self.now_time()[0:18]))
            print('[INFO][{}] Log File Name: {} \n'.format(self.now_time()[0:18], self.file_name))

            log_file.close()

    def open_log(self):
        return open(self.file_name, 'a')

    def info(self, message):
        text        = '[INFO][{}] {} \n'.format(self.now_time()[0:18], message)
        log_file    = self.open_log()

        log_file.write(text)
        print(text, end='')

    def warning(self, message):
        text        = '[WARN][{}] {} \n'.format(self.now_time()[0:18], message)
        log_file    = self.open_log()

        log_file.write(text)
        print(text, end='')

    def error(self, message):
        text        = '[EROR][{}] {} \n'.format(self.now_time()[0:18], message)
        log_file    = self.open_log()

        log_file.write(text)
        print(text, end='')
