import os
from datetime import datetime
from rtc_handler import rtc_init

def set_date_time():

    try:
        date_string = os.popen('wget -qSO- google.com 2>&1 | grep Date: | cut -c 14-33').read().strip()
        date_string = datetime.strptime(date_string,"%d %b %Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        os.system("date -s \"{}\"".format(date_string))
        print("System Date Time : {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        rtc_init()


    except Exception:
        raise Exception




if __name__ == "__main__":
    set_date_time()
