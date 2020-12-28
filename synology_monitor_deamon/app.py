from influxdb import InfluxDBClient
from datetime import datetime
import psutil
import pytz
import asyncio
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--loglevel', default='info', required=False)

args = parser.parse_args()

if(args.loglevel=='info'):
    loglevel = logging.INFO
elif(args.loglevel=='debug'):
    loglevel = logging.DEBUG

logging.basicConfig(level=loglevel)
logging.root = logging.getLogger(__file__)


client = InfluxDBClient(host='172.24.249.110', 
                        port=58086, 
                        username='synology', 
                        password='synology',
                        ssl=False, 
                        verify_ssl=False,
                        database='ds918')

def get_point():
    point = [{
        "measurement" : "cpu_load",
        "time": datetime.now(tz=pytz.UTC),
        "fields": {
            "value" : psutil.cpu_percent(interval=1)
        }
    },
    {
        "measurement" : "memory_usage",
        "time": datetime.now(tz=pytz.UTC),
        "fields": {
            "value" : psutil.cpu_percent(interval=1)
        } 
    }
    ]
    return point


async def get_network_speed(time_delay):
    while True:
        d0 = psutil.net_io_counters()
        await asyncio.sleep(time_delay)
        d1 = psutil.net_io_counters()
        rx_rate = (d1.bytes_recv-d0.bytes_recv)/1024/1024
        tx_rate = (d1.bytes_sent-d0.bytes_sent)/1024/1024
        point = [{
            "measurement" : "network",
            "time": datetime.now(tz=pytz.UTC),
            "fields": {
                "rx" : rx_rate,
                "tx" : tx_rate
            }
        }]
        logging.debug('rx rate: {}, tx rate: {}'.format(rx_rate,tx_rate))
        client.write_points(point)

async def get_cpu_info(time_delay):
    while True:
        await asyncio.sleep(time_delay)
        cpu_usage = psutil.cpu_percent()
        cpu_temp = psutil.sensors_temperatures()['coretemp'][0].current
        point = [{
            "measurement" : "cpu",
            "time": datetime.now(tz=pytz.UTC),
            "fields": {
                "cpu_usage" : cpu_usage,
                "cpu_temp" : cpu_temp
            }
        }]
        logging.debug('cpu usage: {}, cpu temp: {}'.format(cpu_usage,cpu_temp))
        client.write_points(point)


async def get_memory_info(time_delay):
    while True:
        await asyncio.sleep(time_delay)
        used = psutil.virtual_memory().used/1024/1024
        used_percent = psutil.virtual_memory().percent
        point = [{
            "measurement" : "memory",
            "time": datetime.now(tz=pytz.UTC),
            "fields": {
                "used" : used,
                "used_percent" : used_percent
            }
        }]
        logging.debug('memory used: {}, used percent: {}'.format(used,used_percent))
        client.write_points(point)

async def get_disk_info(time_delay):
    while True:
        await asyncio.sleep(time_delay)
        total = psutil.disk_usage('/').total/1024/1204/1024
        used = psutil.disk_usage('/').used/1024/1204/1024
        free = psutil.disk_usage('/').free/1024/1204/1024
        percent = psutil.disk_usage('/').percent
        point = [{
            "measurement" : "disk",
            "time": datetime.now(tz=pytz.UTC),
            "fields": {
                "total" : total,
                "used" : used,
                "free" : free,
                "percent" : percent
            }
        }]
        logging.debug('disk total: {}, used: {}, free: {}, percent: {}'.format(
            total,used,free,percent))
        client.write_points(point)

async def gather_measurements():

    # create task (thread) for each function 
    task1 = asyncio.create_task(get_network_speed(1))
    task2 = asyncio.create_task(get_cpu_info(1))
    task3 = asyncio.create_task(get_memory_info(1))  
    task4 = asyncio.create_task(get_disk_info(1))  

    await task1
    await task2
    await task3
    await task4

# run the main function
asyncio.run(gather_measurements())

