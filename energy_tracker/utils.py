import math
import datetime

from energy_tracker.models import (
    Device,
    DayOfTheWeek,
    Timeframe,
    Delay,
    OverrideDay,
    ScheduleChange,
    ScheduleChangePairings
)

MINUTE_INTERVALS = 1
MINUTE_INTERVALS_PADDING = 3


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


def get_change_status(device_name, day=None, hour=None, minute=None, date=None):
    try:
        device = Device.objects.get(name=device_name)
        messages = (
            "No status change",
            "Status changed: OFF to ON",
            "Status changed: ON to OFF"
        )
        change_status = check_change_status(device, day, hour, minute, date)
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

def get_devices_with_change(day=None, hour=None, minute=None, date=None):
    devices = Device.objects.all()
    responses = []
    messages = (
        "No status change",
        "Status changed: OFF to ON",
        "Status changed: ON to OFF"
    )
    for device in devices:
        change_status = check_change_status(device, day, hour, minute, date)
        if change_status and type(change_status) is int:
            responses.append({
                'device_name': device.name,
                'room': device.room.name if device.room else "",
                'value': change_status,
                'message': messages[change_status]
            })
    return responses

def check_change_status(device, day_of_the_week=None, hour=None, minute=None, date=None):
    """
    STATUSES
    0 - No change
    1 - Off to On
    2 - On to Off
    """
    try:
        override = check_override(hour, minute)
        if override is not None:
            return override
        days = ['Su', 'M', 'T', 'W', 'Th', 'F', 'S']
        delay = Delay.objects.filter(device=device)
        if delay:
            delay = delay.first()
        else:
            delay = None
        schedules = device.room.room_schedules.all()
        if not day_of_the_week:
            now = datetime.datetime.now()
            day_of_the_week = days[int(now.strftime("%w"))]
        day_of_the_week = DayOfTheWeek.objects.get(code=day_of_the_week)


        now = datetime.datetime.now()
        if hour is not None and minute is not None:
            now = now.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0
            )

        if delay:
            delay_value = int(delay.delay_value)
            now = now - datetime.timedelta(
                seconds=(delay_value * 60)
            )
            current_timeframe, previous_timeframe, previous_timeframe_padding = get_all_timeframes(
                now, day_of_the_week, hour, minute, date, device
            )
            if not current_timeframe:
                if previous_timeframe or previous_timeframe_padding:
                    return 2

        now = datetime.datetime.now()
        if hour is not None and minute is not None:
            now = now.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0
            )
        current_timeframe, previous_timeframe, previous_timeframe_padding = get_all_timeframes(
            now, day_of_the_week, hour, minute, date, device
        )

        if current_timeframe:
            if (not previous_timeframe) or (not previous_timeframe_padding):
                return 1
        else:
            if ((previous_timeframe) or (previous_timeframe_padding)) and not delay:
                return 2
        return 0
    except Exception as e:
        return {
            'success': False,
            'message': str(e)
        }


def check_override(hour=None, minute=None):
    now = datetime.datetime.now()
    if hour is not None and minute is not None:
        now = now.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0
        )
    override = OverrideDay.objects.filter(date=now.date()).first()
    if override:
        if override.override_type == "ON":
            if now.time() == datetime.time(7, 40):
                return 1
            elif now.time() == datetime.time(22, 00):
                return 2
            else:
                return 0
        elif override.override_type == "OFF":
            return 0
    else:
        return None


def get_individual_timeframe(time, day, device, current_date):
    timeframe = Timeframe.objects.filter(
        start_time__lte=time,
        end_time__gt=time,
        days__id=day,
        schedules__room__devices=device
    )
    schedule_change = ScheduleChange.objects.filter(date=current_date)
    if schedule_change:
        schedule_change = schedule_change.first()
        changed_timeframe = ScheduleChangePairings.objects.filter(
            start_time__lte=time,
            end_time__gte=time,
            schedule__days__id=day,
            schedule__schedules__room__devices=device
        )
        if changed_timeframe:
            return changed_timeframe

        timeframe = timeframe.exclude(
            schedule_pair__schedule_date__date=current_date
        )
    return timeframe


def get_all_timeframes(now, day_of_the_week, hour, minute, date, device):
        current_time = now.time()
        current_date = datetime.datetime.strptime(date, '%Y-%m-%d').date() if date else now.date()

        # ct = Timeframe.objects.filter(
        #     start_time__lte=current_time,
        #     end_time__gte=current_time,
        #     days__id=day_of_the_week.id
        # )
        # ct = get_individual_timeframe(time, day, device, current_date)
        # print(ct)
        current_timeframe = get_individual_timeframe(
            time=current_time,
            day=day_of_the_week.id,
            device=device,
            current_date=current_date
        )

        previous_time = now - datetime.timedelta(
            seconds=(MINUTE_INTERVALS * 60)
        )
        previous_time = previous_time.time()
        previous_timeframe = get_individual_timeframe(
            time=previous_time,
            day=day_of_the_week.id,
            device=device,
            current_date=current_date
        )
        # next_time = now + datetime.timedelta(
        #     seconds=(MINUTE_INTERVALS * 60)
        # )
        # next_time = next_time.time()
        # next_timeframe = get_individual_timeframe(
        #     time=next_time,
        #     day=day_of_the_week.id,
        #     device=device,
        #     current_date=current_date
        # )
        previous_time_padding = now - datetime.timedelta(
            seconds=(MINUTE_INTERVALS * 60 * MINUTE_INTERVALS_PADDING)
        )
        previous_time_padding = previous_time_padding.time()
        previous_timeframe_padding = get_individual_timeframe(
            time=previous_time_padding,
            day=day_of_the_week.id,
            device=device,
            current_date=current_date
        )
        return current_timeframe, previous_timeframe, previous_timeframe_padding
