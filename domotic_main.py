##Main script: get data from sensors, format and populate the different DBs

from apscheduler.schedulers.blocking import BlockingScheduler
from config_DB import *
from temperature_grab import *
from humidity_grab import *
from func_others import *
from mariadb_storage import *


def populate_DB():
    current_time = get_current_time()
    #Pb with cuurentime 2h avant...
    tempsensor_loc = {'28-0000032404c5': 1, '28-000001d1b573': 2, '28-0516a50fa1ff': 3}
    humsensor_loc = {'dht22': 1}

    sensor_temp = grab_sensors_temp()
    sensor_hum =  grab_sensors_hum()

    tempvalues = format_value(sensor_temp, tempsensor_loc)
    humvalues = format_value(sensor_hum, humsensor_loc)

    insert_tempvalues(user, host, password, database, current_time, tempvalues)
    insert_humvalues(user, host, password, database, current_time, humvalues)


#populate_DB()
scheduler = BlockingScheduler()
scheduler.add_job(populate_DB, 'interval', minutes = 1)
scheduler.start()
