from drivers import ExchangeDriver, GoogleDriver, PrinterDriver
from syncer import Syncer

if __name__ == '__main__':
    driver = ExchangeDriver('<login>', '<password>', '<email>')
    google_driver = GoogleDriver()
    syncer = Syncer(driver, google_driver)
    syncer.process()
