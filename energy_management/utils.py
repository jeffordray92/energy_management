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
