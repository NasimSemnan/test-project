import time
import winsound
from datetime import datetime, timedelta

count = int(input("count of beep: "))


def pashooo():
    now = datetime.now()
    wakeup_time = input("vared kon time mesl HH:MM:  ")
    wakeup_date_time = datetime.strptime(wakeup_time, "%H:%M").time()
    wakeup = datetime.combine(now.date(), wakeup_date_time)
    tim_bidar_bash = wakeup - now
    if tim_bidar_bash.total_seconds() < 0:
        wakeup += timedelta(days=1)
        tim_bidar_bash = wakeup - now

    print(f"bidar bash:{tim_bidar_bash}")
    time.sleep(tim_bidar_bash.total_seconds())
    print("bidarshoooo")


def start_beep(count):
    for i in range(0, count):
        winsound.Beep(2500, 1000)
        print("wakeUp")


pashooo()

start_beep(count)
