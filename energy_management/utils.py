import csv
import datetime

from collections import OrderedDict

from energy_tracker.models import TrackerEntry, Device


def get_entries(room, frequency=None):
    current_time = datetime.datetime.now()
    devices = Device.objects.filter(room=room)

    if not frequency:
        display_data = TrackerEntry.objects.all()

    if frequency == "hourly":
        current_time = current_time - datetime.timedelta(hours=1)
        display_data = TrackerEntry.objects.filter(created_at__gte=current_time, device__in=devices)
    elif frequency == "daily":
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

    data = []

    data.append(list(OrderedDict.fromkeys([x.created_at.strftime("%D, %H:%M") for x in display_data.order_by('created_at')])))

    for device in devices:
        filtered_data = display_data.filter(device=device).order_by('created_at')
        data.append([x.power for x in filtered_data])

    return data


def override_entries(filename):
    try:
        with open(f'{filename}', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                #2019-11-18 8:38:56.067165+00:00
                created_at = datetime.datetime.strptime(
                    row['created_at'].replace("+00:00", "+08:00"), '%Y-%m-%d %H:%M:%S.%f%z')
                entry_id = int(row['entry_id'])
                device_name = row['device_name']
                voltage = float(row['voltage']) if row['voltage'] else 0
                current = float(row['current']) if row['current'] else 0
                power = float(row['power']) if row['power'] else 0
                energy = float(row['energy']) if row['energy'] else 0
                power_factor = float(row['power_factor']) if row['power_factor'] else 0

                device = Device.objects.get(name=device_name)

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
