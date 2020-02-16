import csv
import datetime

from collections import OrderedDict
from pytz import timezone

from energy_tracker.models import TrackerEntry, Device


def get_entries(room, frequency="hourly", start=None, end=None):

    current_time = datetime.datetime.now()
    current_time = current_time.astimezone(timezone('Asia/Manila'))

    # PLEASE DELETE AFTER!!!!
    # current_time = current_time.replace(day=10, month=12, year=2019)
    devices = Device.objects.filter(room=room).order_by('name')

    data = []

    if frequency == "hourly":
        # time1 = current_time - datetime.timedelta(hours=3)
        # time2 = current_time - datetime.timedelta(hours=4)
        # display_data = TrackerEntry.objects.filter(created_at__gte=time2, created_at__lt=time1, device__in=devices)
        current_time = current_time - datetime.timedelta(hours=1)
        display_data = TrackerEntry.objects.filter(created_at__gte=current_time, device__in=devices)
    elif frequency == "daily":
        # display_data = TrackerEntry.objects.filter(created_at__date=current_time.date())
        # current_time = current_time.astimezone(timezone('Asia/Manila'))
        current_time = current_time - datetime.timedelta(days=1)
        display_data = TrackerEntry.objects.filter(created_at__gte=current_time, device__in=devices)
    elif frequency == "weekly":
        current_time = current_time - datetime.timedelta(weeks=1)
        display_data = TrackerEntry.objects.filter(created_at__gte=current_time, device__in=devices)
    elif frequency == "monthly":
        current_time = current_time - datetime.timedelta(days=30)
        display_data = TrackerEntry.objects.filter(created_at__gte=current_time, device__in=devices)
    elif frequency == "yearly":
        current_time = current_time - datetime.timedelta(weeks=52)
        display_data = TrackerEntry.objects.filter(created_at__gte=current_time, device__in=devices)
    elif frequency == "range":
        if start:
            start_time = datetime.datetime.strptime(start, '%Y-%m-%d').replace(hour=0, minute=0)
        if end:
            end_time = datetime.datetime.strptime(end, '%Y-%m-%d').replace(hour=23, minute=59)
        else:
            end_time = current_time

        display_data = TrackerEntry.objects.filter(created_at__lte=end_time, device__in=devices)
        if start:
            display_data = display_data.filter(created_at__gte=start_time)


    data.append(format_time_entries(display_data))

    for device in devices:
        filtered_data = display_data.filter(device=device).order_by('created_at')
        new_data = [x.power for x in filtered_data]
        data.append(new_data)
        # print(device.name)
        # if device.name == "Aircon":
        #     print([(x.power, x.created_at.astimezone(timezone('Asia/Manila')).strftime("%D, %H:%M")) for x in filtered_data])
    return data


def format_entries_by_average(display_data, frequency, current_time):
    data = []

    if frequency == "hourly":
        data.append(list(OrderedDict.fromkeys([x.created_at.strftime("%D, %H:%M") for x in display_data.order_by('created_at')])))

        for device in devices:
            filtered_data = display_data.filter(device=device).order_by('created_at')
            data.append([x.power for x in filtered_data])


    if frequency == "daily":
        last_hour = current_time.hour + 1
        base_times = [current_time.replace(
            hour=hour, minute=0, second=0, microsecond=0
        ) for hour in range(0,last_hour)]
        data.append([x.strftime("%D, %H:%M") for x in base_times])
        for device in devices:
            filtered_data = display_data.filter(device=device)
            for time in base_times:
                filtered_data.filter(created_at__gte=time, created_at__lt=time).aggregate(Avg('price'))
            data.append([x.power for x in filtered_data])


def format_time_entries(display_data):
    formatted_time = list(OrderedDict.fromkeys([x.created_at.astimezone(timezone('Asia/Manila')).strftime("%D, %H:%M") for x in display_data.order_by('created_at')]))
    return formatted_time


def override_entries(filename):
    try:
        with open(f'{filename}', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                #2019-11-18 8:38:56.067165+00:00
                created_at = datetime.datetime.strptime(
                    row['created_at'].replace("+08:00", "+00:00"), '%Y-%m-%d %H:%M:%S.%f%z')
                created_at = created_at.astimezone(tz=timezone('Asia/Manila'))
                entry_id = int(row['entry_id'])
                device_name = row['device_name']
                voltage = float(row['voltage']) if row['voltage'] else 0
                current = float(row['current']) if row['current'] else 0
                power = float(row['power']) if row['power'] else 0
                energy = float(row['energy']) if row['energy'] else 0
                power_factor = float(row['power_factor']) if row['power_factor'] else 0

                device = Device.objects.get(name=device_name)

                # obj, created = TrackerEntry.objects.get_or_create(
                #     created_at=created_at,
                #     device=device
                # )
                # obj.voltage = voltage
                # obj.current = current
                # obj.power = power
                # obj.energy = energy
                # obj.power_factor = power_factor
                # obj.save()

                obj = TrackerEntry(
                    id=entry_id,
                    created_at=created_at,
                    voltage=voltage,
                    current=current,
                    power=power,
                    energy=energy,
                    power_factor=power_factor,
                    device=device
                )
                obj.save()
                obj.created_at = created_at
                obj.save()
                # print(row)
                line_count += 1 
                print(f"Processing Line # {line_count}", end="\r")
            print(f'Processed {line_count} lines.')
    except Exception as e:
        print(e)


def print_each(**kwargs):
    print(kwargs)
