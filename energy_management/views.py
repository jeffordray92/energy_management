import json

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from energy_tracker.models import Room
from energy_management.utils import get_entries

class DashboardView(View):
    template_name = 'Dashboard.html'

    def get(self, request, *args, **kwargs):
        roomname = request.GET.get('room')
        frequency = request.GET.get('freq')

        if not roomname: roomname="T101"
        if not frequency: frequency="hourly"

        room = Room.objects.get(name=roomname)
        entries = get_entries(room, frequency)
        display_data = entries

        data = json.dumps(display_data)
        return render(request, self.template_name, {
            'data': data,
            'room': roomname,
            'freq': frequency
        })
