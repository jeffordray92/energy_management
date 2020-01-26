import csv
import datetime
import pytz

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from energy_tracker.models import Device, TrackerEntry
from energy_tracker.serializers import EntrySerializer, NewEntrySerializer
from energy_tracker.utils import (
    check_change_status,
    convert_non_integer_to_zero,
    get_change_status,
    get_devices_with_change
)

class TrackerListView(APIView):
    """
    List all tracker entries, or create a new tracker entry.
    """
    def get(self, request, format=None):
        entries = TrackerEntry.objects.all()
        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # data = request.data    for JSON
        data = convert_non_integer_to_zero(request.data.dict())
        device_name = data.get('device')
        try:
            device = Device.objects.get(name=device_name) if device_name else None
        except ObjectDoesNotExist:
            device = None
        if device:
            data['device'] = device.id
            serializer = NewEntrySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"errors": "Wrong device name"}, status=status.HTTP_400_BAD_REQUEST)


class AllStatusView(APIView):
    """
    List all devices with change in status for the current time
    """
    def get(self, request, format=None):
        return Response({"devices": get_devices_with_change()}, status=status.HTTP_200_OK)


class DeviceStatusView(APIView):
    """
    Return status change for a device for the current time
    """
    def get(self, request, device, format=None):
        change_status = get_change_status(device)
        if change_status['success']:
            return Response(change_status['value'], status=status.HTTP_200_OK)
        else:
            return Response(change_status, status=status.HTTP_400_BAD_REQUEST)


class AllStatusTimeView(APIView):
    """
    List all devices with change in status for a given time
    """
    def get(self, request, hour, minute, date, format=None):
        days = ['Su', 'M', 'T', 'W', 'Th', 'F', 'S']
        day = days[int(datetime.datetime.strptime(date, '%Y-%m-%d').strftime("%w"))]
        return Response({"devices": get_devices_with_change(day, hour, minute, date)}, status=status.HTTP_200_OK)


class DeviceStatusTimeView(APIView):
    """
    Return status change for a device for a given time
    """
    def get(self, request, device, hour, minute, date, format=None):
        days = ['Su', 'M', 'T', 'W', 'Th', 'F', 'S']
        day = days[int(datetime.datetime.strptime(date, '%Y-%m-%d').strftime("%w"))]
        change_status = get_change_status(device, day, hour, minute, date)
        if change_status['success']:
            return Response(change_status['value'], status=status.HTTP_200_OK)
        else:
            return Response(change_status, status=status.HTTP_400_BAD_REQUEST)

class TempView(APIView):

    def post(self, request, format=None):
        print(request.is_secure())
        return Response({"message": "TEST"}, status=status.HTTP_200_OK)


def export_csv_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    query = {k:v for (k,v) in request.GET.items()}
    queryset = TrackerEntry.objects.filter(**query).order_by('-id')
    entries = queryset.values(
        'id',
        'created_at',
        'device__name',
        'voltage',
        'current',
        'power',
        'energy',
        'power_factor'
    )
    filename = "export-{}.csv".format(datetime.datetime.now().date())
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    writer = csv.writer(response)
    writer.writerow(['created_at', 'entry_id', 'device_name', 'voltage', 'current', 'power', 'energy', 'power_factor'])
    for entry in entries:
        created_at = entry['created_at']
        writer.writerow([
            created_at.isoformat().replace("+00:00", "+08:00"),
            entry['id'],
            entry.get('device__name',""),
            entry['voltage'],
            entry['current'],
            entry['power'],
            entry['energy'],
            entry['power_factor'],
        ])

    return response
