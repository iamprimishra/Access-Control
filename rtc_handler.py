from mraa_helper import MRAA_Helper
from datetime import datetime,timedelta

class RTC_Handler:

    _REG_SECONDS = 0x00
    _REG_MINUTES = 0x01
    _REG_HOURS = 0x02
    _REG_DAY = 0x03
    _REG_DATE = 0x04
    _REG_MONTH = 0x05
    _REG_YEAR = 0x06
    _REG_CONTROL = 0x07

    def __init__(self,twi,address):
        self.mraa_i2c = MRAA_Helper()
        self.twi=twi
        self.address=address
        self.i2c = self.mraa_i2c.i2c_init(twi=self.twi,address=self.address)


    def bcd_to_int(self,bcd):
        """Decode a 2x4bit BCD to a integer.
        """
        out = 0
        for d in (bcd >> 4, bcd):
            for p in (1, 2, 4 ,8):
                if d & 1:
                    out += p
                d >>= 1
            out *= 10
        return int(out / 10)


    def int_to_bcd(self,n):
        """Encode a one or two digits number to the BCD.
        """
        bcd = 0
        for i in (n // 10, n % 10):
            for p in (8, 4, 2, 1):
                if i >= p:
                    bcd += 1
                    i -= p
                bcd <<= 1
        return int(bcd >> 1)

    def _read_seconds(self):
        return self.bcd_to_int(self.mraa_i2c.read_i2c_data(self._REG_SECONDS))


    def _read_minutes(self):
        return self.bcd_to_int(self.mraa_i2c.read_i2c_data(self._REG_MINUTES))


    def _read_hours(self):
        d = self.mraa_i2c.read_i2c_data(self._REG_HOURS)
        if not ((d & 0x40) >> 7):
            return self.bcd_to_int(d & 0x3F)
        else:
            h = self.bcd_to_int(d & 0x1F)
            if d & 0x20:
                h += 11  # Convert 12h to 24h
            elif h == 12:
                h = 0
            return h


    def _read_day(self):
        return self.bcd_to_int(self.mraa_i2c.read_i2c_data(self._REG_DAY))


    def _read_date(self):
        return self.bcd_to_int(self.mraa_i2c.read_i2c_data(self._REG_DATE))


    def _read_month(self):
        return self.bcd_to_int(self.mraa_i2c.read_i2c_data(self._REG_MONTH))


    def _read_year(self):
        # print(self.mraa_i2c.read_i2c_data(self._REG_YEAR))
        return self.bcd_to_int(self.mraa_i2c.read_i2c_data(self._REG_YEAR))


    def read_all(self):
        """Return a tuple such as (year, month, date, day, hours, minutes,
        seconds).
        """
        return (self._read_year(), self._read_month(), self._read_date(),
                self._read_day(), self._read_hours(), self._read_minutes(),
                self._read_seconds())


    def read_str(self):
        """Return a string such as 'YY-DD-MMTHH-MM-SS'.
        """
        return '%02d-%02d-%02dT%02d:%02d:%02d' % (self._read_year(),
                self._read_month(), self._read_date(), self._read_hours(),
                self._read_minutes(), self._read_seconds())


    def read_datetime(self, century=21, tzinfo=None):
        """Return the datetime.datetime object.
        """
        # print(self._read_year(),self._read_month(), self._read_date(), self._read_hours(),self._read_minutes(), self._read_seconds())
        return datetime((century - 1) * 100 + self._read_year(),
                self._read_month(), self._read_date(), self._read_hours(),
                self._read_minutes(), self._read_seconds(), 0, tzinfo=tzinfo)


    def write_all(self, seconds=None, minutes=None, hours=None, day=None,
            date=None, month=None, year=None, save_as_24h=True):
        """Direct write un-none value.
        Range: seconds [0,59], minutes [0,59], hours [0,23],
               day [0,7], date [1-31], month [1-12], year [0-99].
        """

        # print(seconds,minutes,hours,day,date,month,year)
        if seconds is not None:
            if seconds < 0 or seconds > 59:
                raise ValueError('Seconds is out of range [0,59].')
            self.mraa_i2c.write_i2c_data(self._REG_SECONDS, self.int_to_bcd(seconds))

        if minutes is not None:
            if minutes < 0 or minutes > 59:
                raise ValueError('Minutes is out of range [0,59].')
            self.mraa_i2c.write_i2c_data(self._REG_MINUTES, self.int_to_bcd(minutes))

        if hours is not None:
            if hours < 0 or hours > 23:
                raise ValueError('Hours is out of range [0,23].')
            if save_as_24h:
                self.mraa_i2c.write_i2c_data(self._REG_HOURS, self.int_to_bcd(hours) & 0xbf)
            else:
                if hours == 0:
                    h = self.int_to_bcd(12) | 0x32
                elif hours <= 12:
                    h = self.int_to_bcd(hours)
                else:
                    h = self.int_to_bcd(hours - 12) | 0x32
                self.mraa_i2c.write_i2c_data(self._REG_HOURS, h)

        if year is not None:
            if year < 0 or year > 99:
                raise ValueError('Years is out of range [0,99].')
            self.mraa_i2c.write_i2c_data(self._REG_YEAR, self.int_to_bcd(year))

        if month is not None:
            if month < 1 or month > 12:
                raise ValueError('Month is out of range [1,12].')
            self.mraa_i2c.write_i2c_data(self._REG_MONTH, self.int_to_bcd(month))

        if date is not None:
            if date < 1 or date > 31:
                raise ValueError('Date is out of range [1,31].')
            self.mraa_i2c.write_i2c_data(self._REG_DATE, self.int_to_bcd(date))

        if day is not None:
            if day < 1 or day > 7:
                raise ValueError('Day is out of range [1,7].')
            self.mraa_i2c.write_i2c_data(self._REG_DAY, self.int_to_bcd(day))


    def write_datetime(self, dt):
        """Write from a datetime.datetime object.
        """
        # print(dt)
        self.write_all(dt.second, dt.minute, dt.hour,
                dt.isoweekday(), dt.day, dt.month, dt.year % 100)


    def write_now(self):
        """Equal to DS1307.write_datetime(datetime.datetime.now()).
        """
        self.write_datetime(datetime.now()+timedelta(hours=5, minutes=30))


def main():

    ds = RTC_Handler(1, 0x68)
    ds.write_now()
    print(ds.read_datetime())
    # ds.write_now()


def rtc_init():
    ds = RTC_Handler(1,0x68)
    ds.write_now()
    print("RTC Time : {}".format(ds.read_datetime()))


if __name__ == '__main__':
    main()
