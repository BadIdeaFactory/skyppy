from datetime import datetime

class inaLogger:
    @staticmethod
    def write_to_log(content):
        try:
            with open("log.txt", "a") as logfile:
                logfile.write(f"{str(datetime.now().isoformat())}; {str(content)} \n")
        except:
            pass