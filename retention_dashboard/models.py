from django.db import models


class Week(models.Model):
    QUARTER_CHOICES = ((1, 'Winter'),
                       (2, 'Spring'),
                       (3, 'Summer'),
                       (4, 'Autumn'))
    number = models.IntegerField()
    quarter = models.PositiveSmallIntegerField(
        default=1, choices=QUARTER_CHOICES)
    year = models.IntegerField()


class DataPoint(models.Model):
    TYPE_CHOICES = ((1, "OMAD"), (2, "EOP"), (3, "International"))
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    week = models.ForeignKey("Week", on_delete=models.PROTECT)
    student_name = models.TextField()
    student_number = models.IntegerField()
    netid = models.CharField(max_length=12)
    premajor = models.BooleanField()
    priority_score = models.FloatField()
    activity_score = models.FloatField()
    assignment_score = models.FloatField()
    grade_score = models.FloatField()


class Upload(models.Model):
    file = models.TextField()
    type = models.PositiveSmallIntegerField(choices=DataPoint.TYPE_CHOICES)
    uploaded_by = models.CharField(max_length=12)
    created_on = models.DateTimeField(auto_now_add=True)
    week = models.ForeignKey("Week", on_delete=models.PROTECT)
