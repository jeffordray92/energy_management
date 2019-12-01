import math
import datetime

from energy_tracker.models import Device, DayOfTheWeek, Timeframe, Delay

MINUTE_INTERVALS = 1


def convert_non_integer_to_zero(data):
    fields = ['voltage', 'current', 'power', 'energy', 'power_factor']
    for field in fields:
        try:
            val = float(data[field])
            if math.isnan(val):
                raise ValueError
        except ValueError:
            data[field] = 0.0
    return data


def get_change_status(device_name, day=None, hour=None, minute=None):
    try:
        device = Device.objects.get(name=device_name)
        messages = (
            "No status change",
            "Status changed: OFF to ON",
            "Status changed: ON to OFF"
        )
        change_status = check_change_status(device, day, hour, minute)
        if type(change_status) is dict:
            return change_status
        return {
            'success': True,
            'value': change_status,
            'message': messages[change_status]
        }
    except Exception as e:
        return {
            'success': False,
            'message': str(e)
        }

def get_devices_with_change(day=None, hour=None, minute=None):
    devices = Device.objects.all()
    responses = []
    messages = (
        "No status change",
        "Status changed: OFF to ON",
        "Status changed: ON to OFF"
    )
    for device in devices:
        change_status = check_change_status(device, day, hour, minute)
        if change_status and type(change_status) is int:
            responses.append({
                'device_name': device.name,
                'room': device.room.name if device.room else "",
                'value': change_status,
                'message': messages[change_status]
            })
    return responses

def check_change_status(device, day_of_the_week=None, hour=None, minute=None):
    """
    STATUSES
    0 - No change
    1 - Off to On
    2 - On to Off
    """
    try:
        days = ['Su', 'M', 'T', 'W', 'Th', 'F', 'S']
        delay = Delay.objects.filter(device=device).first()
        now = datetime.datetime.now()
        schedules = device.room.room_schedules.all()
        if not day_of_the_week:
            day_of_the_week = days[int(now.strftime("%w"))]
        day_of_the_week = DayOfTheWeek.objects.get(code=day_of_the_week)

        if hour is not None and minute is not None:
            now = now.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0
            )
        if delay:
            now = now - datetime.timedelta(
                seconds=(delay.delay_value*60)
            )
        current_time = now.time()
        previous_time = now - datetime.timedelta(
            seconds=(MINUTE_INTERVALS*60)
        )
        previous_time = previous_time.time()
        current_timeframe = Timeframe.objects.filter(
                start_time__lte=current_time,
                end_time__gte=current_time,
                days__id=day_of_the_week.id,
                schedules__room__devices=device
        )
        previous_timeframe = Timeframe.objects.filter(
                start_time__lte=previous_time,
                end_time__gte=previous_time,
                days__id=day_of_the_week.id
        )
        if current_timeframe and not previous_timeframe:
            return 1
        elif previous_timeframe and not current_timeframe:
            return 2
        else:
            return 0
    except Exception as e:
        return {
            'success': False,
            'message': str(e)
        }
