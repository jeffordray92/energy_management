from rest_framework import serializers

from django.contrib.auth.models import User, Group

from energy_tracker.models import TrackerEntry, Device


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['name', 'number', 'description']

class EntrySerializer(serializers.ModelSerializer):
    device = DeviceSerializer(many=False)

    class Meta:
        model = TrackerEntry
        fields = ['created_at', 'voltage', 'current', 'power', 'energy', 'power_factor', 'device']


class NewEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackerEntry
        fields = ['voltage', 'current', 'power', 'energy', 'power_factor', 'device']
