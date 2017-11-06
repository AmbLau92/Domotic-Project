##Other functions for the project

from time import localtime, strftime

def get_current_time():
    """Give current time in mariaDB DateTime format"""
    current_time = strftime("%Y:%m:%d %H:%M:%S", localtime())
    return current_time


def format_value(sensor_value, sensor_loc):
    """Return loc_value dict in format {location_device: value_device}, value being temperature or humidity"""
    loc_value = {v: sensor_value.get(k, k) for k, v in sensor_loc.items()}
    return loc_value
