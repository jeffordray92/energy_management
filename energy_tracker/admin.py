from django.contrib import admin

from rangefilter.filter import DateRangeFilter

from energy_tracker.models import (
    TrackerEntry,
    Device,
    DayOfTheWeek,
    Room,
    Schedule,
    Timeframe,
    OverrideDay,
    Delay,
    CalibrationValue,
    ScheduleChange,
    ScheduleChangePairings
)

def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


class EntryAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'device', 'voltage', 'current', 'power', 'energy', 'power_factor']
    list_filter = [('created_at', DateRangeFilter), ('created_at', custom_titled_filter('Date Saved - Range')), 'device']
    change_list_template = "custom_list.html"


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'room', 'description']


class DeviceInline(admin.TabularInline):
    model = Device
    classes = ['collapse']
    extra = 0


class RoomAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [DeviceInline,]


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['name', 'room', 'date_time', 'notes']


class TimeframeAdmin(admin.ModelAdmin):
    filter_horizontal = ['days']


class DayAdmin(admin.ModelAdmin):
    list_display = ['code', 'description']


class OverrideAdmin(admin.ModelAdmin):
    list_display = ['date', 'description', 'override_type']

class DelayAdmin(admin.ModelAdmin):
    list_display = ['device', 'delay_value']

class CalibrationAdmin(admin.ModelAdmin):
    list_display = ['device', 'field', 'value']


class ScheduleChangePairInline(admin.TabularInline):
    model = ScheduleChangePairings
    extra = 0


class ScheduleChangeAdmin(admin.ModelAdmin):
    list_display = ['name', 'date']
    inlines = [ScheduleChangePairInline,]


admin.site.register(TrackerEntry, EntryAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Timeframe, TimeframeAdmin)
admin.site.register(DayOfTheWeek, DayAdmin)
admin.site.register(OverrideDay, OverrideAdmin)
admin.site.register(Delay, DelayAdmin)
admin.site.register(ScheduleChange, ScheduleChangeAdmin)


admin.site.site_header = "Energy Management Admin"
admin.site.site_title = "Energy Management Admin Portal"
admin.site.index_title = "Welcome to Energy Management Admin Portal"
