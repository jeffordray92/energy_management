from django.db import models


optional = {
    'blank': True,
    'null': True
}


class TrackerEntry(models.Model):

    voltage = models.FloatField()
    current = models.FloatField()
    power = models.FloatField()
    energy = models.FloatField()
    power_factor = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    device = models.ForeignKey(
        "energy_tracker.Device",
        on_delete=models.CASCADE,
        related_name="entries",
        **optional
    )

    def __str__(self):
        return str(self.created_at)

    class Meta:
        verbose_name = "Entry"
        verbose_name_plural = "Entries"


class Device(models.Model):

    name = models.CharField(max_length=50)
    number = models.CharField(max_length=10)
    room = models.ForeignKey(
        "energy_tracker.Room",
        on_delete=models.CASCADE,
        related_name="devices",
        **optional
    )
    description = models.TextField(**optional)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"


class Room(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"


class Schedule(models.Model):
    name = models.CharField(max_length=50)
    room = models.ForeignKey(
        "energy_tracker.Room",
        on_delete=models.CASCADE,
        related_name="room_schedules",
        **optional
    )
    notes = models.TextField(**optional)
    date_time = models.ForeignKey(
        "energy_tracker.Timeframe",
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name="Day and Time",
        **optional
    )

    def __str__(self):
        return "{} - {}".format(self.name, self.room.name)

    class Meta:
        verbose_name = "Room Schedule"
        verbose_name_plural = "Room Schedules"


class Timeframe(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = models.ManyToManyField(
        "energy_tracker.DayOfTheWeek",
        **optional)

    def __str__(self):
        days = "".join(str(day.code) for day in self.days.all())
        return "{} - {} {}".format(self.start_time, self.end_time, days)

    class Meta:
        verbose_name = "Time Frame"
        verbose_name_plural = "Time Frame"


class DayOfTheWeek(models.Model):
    code = models.CharField(max_length=2)
    description = models.CharField(max_length=9)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Day of the Week"
        verbose_name_plural = "Days of the Week"


class OverrideDay(models.Model):

    TYPE_CHOICES = [
        ("ON", "Always On"),
        ("OFF", "Always Off")
    ]

    date = models.DateField()
    description = models.CharField(max_length=200)
    override_type = models.CharField(
        max_length=3,
        choices=TYPE_CHOICES,
        default="OFF"
    )

    def __str__(self):
        return "{} ({})".format(self.date, self.description)

    class Meta:
        verbose_name = "Override Day"
        verbose_name_plural = "Override Days"


class Delay(models.Model):

    device = models.OneToOneField(
        "energy_tracker.Device",
        related_name="delay",
        on_delete=models.CASCADE
    )
    delay_value = models.IntegerField()

    def __str__(self):
        return self.device.name

    class Meta:
        verbose_name = "Delay"
        verbose_name_plural = "Delays"


class CalibrationValue(models.Model):

    CALIBRATION_FIELDS = [
        ("P", "Power"),
        ("V", "Voltage"),
        ("C", "Current")
    ]

    device = models.ForeignKey(
        "energy_tracker.Device",
        on_delete=models.CASCADE,
        related_name="calibration_values",
    )
    field = models.CharField(
        max_length=1,
        choices=CALIBRATION_FIELDS,
        default="P"
    )
    value = models.FloatField()

    def __str__(self):
        return "{} - {}".format(self.device.name, self.field)

    class Meta:
        verbose_name = "Calibration Value"
        verbose_name_plural = "Calibration Values"


class ScheduleChange(models.Model):

    name = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.date})"

    class Meta:
        verbose_name = "Schedule Change"
        verbose_name_plural = "Schedule Change List"


class ScheduleChangePairings(models.Model):

    schedule_date = models.ForeignKey(
        "energy_tracker.ScheduleChange",
        on_delete=models.CASCADE,
        related_name="schedule_date_pair",
    )
    schedule = models.ForeignKey(
        "energy_tracker.Timeframe",
        on_delete=models.CASCADE,
        related_name="schedule_pair",
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
