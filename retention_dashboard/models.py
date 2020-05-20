from django.db import models
from django.db.models import Q


class Week(models.Model):
    QUARTER_CHOICES = ((1, 'Winter'),
                       (2, 'Spring'),
                       (3, 'Summer'),
                       (4, 'Autumn'))
    number = models.IntegerField()
    quarter = models.PositiveSmallIntegerField(
        default=1, choices=QUARTER_CHOICES)
    year = models.IntegerField()

    def json_data(self):
        display_string = "{} {}: Week {}".format(self.get_quarter_display(),
                                                 self.year,
                                                 self.number)
        return {"value": self.id,
                "text": display_string}


class DataPoint(models.Model):
    TYPE_CHOICES = ((1, "Premajor"), (2, "EOP"), (3, "International"))
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
    upload = models.ForeignKey("Upload", on_delete=models.CASCADE)
    advisor = models.ForeignKey("Advisor", on_delete=models.PROTECT, null=True)

    @staticmethod
    def get_data_by_type_week(type, week):
        type_int = [item for item in
                    DataPoint.TYPE_CHOICES
                    if type in item][0][0]
        data = DataPoint.objects.filter(type=type_int, week=week)
        return data

    @staticmethod
    def filter_by_ranges(data_queryset, ranges, field):
        LOW_MIN = -5
        AVG_MIN = -3
        HIGH_MIN = 3
        HIGH_MAX = 5

        field_lt = field + "__lt"
        field_gt = field + "__gt"
        field_lte = field + "__lte"
        field_gte = field + "__gte"
        queries = []
        if "low" in ranges:
            queries.append(Q(**{field_lte: AVG_MIN,
                                field_gte: LOW_MIN}))
        if "avg" in ranges:
            queries.append(Q(**{field_lt: HIGH_MIN,
                                field_gt: AVG_MIN}))
        if "high" in ranges:
            queries.append(Q(**{field_lte: HIGH_MAX,
                                field_gte: HIGH_MIN}))
        query = queries.pop()
        for item in queries:
            query |= item
        return data_queryset.filter(query)

    @staticmethod
    def filter_by_text(data_queryset, text):
        data_queryset = \
            data_queryset.filter(Q(student_name__icontains=text)
                                 | Q(student_number__icontains=text)
                                 | Q(netid__icontains=text))

        return data_queryset

    @staticmethod
    def filter_by_premajor(data_queryset, is_premajor):
        return data_queryset.filter(premajor=is_premajor)

    def json_data(self):
        return {"student_name": self.student_name,
                "student_number": self.student_number,
                "netid": self.netid,
                "priority_score": self.priority_score,
                "activity_score": self.activity_score,
                "assignment_score": self.assignment_score,
                "grade_score": self.grade_score,
                "is_premajor": self.premajor
                }


class Upload(models.Model):
    file = models.TextField()
    type = models.PositiveSmallIntegerField(choices=DataPoint.TYPE_CHOICES)
    uploaded_by = models.CharField(max_length=12)
    created_on = models.DateTimeField(auto_now_add=True)
    week = models.ForeignKey("Week", on_delete=models.PROTECT)

    class Meta:
        unique_together = ('type', 'week',)


class Advisor(models.Model):
    advisor_name = models.TextField()
    advisor_netid = models.CharField(max_length=12)
    advisor_type = models.PositiveSmallIntegerField(
        choices=DataPoint.TYPE_CHOICES)

    @staticmethod
    def get_all_advisors():
        eop = Advisor.objects.filter(advisor_type=2).\
            values('advisor_name', 'advisor_netid')
        prem = Advisor.objects.filter(advisor_type=1).\
            values('advisor_name', 'advisor_netid')
        inter = Advisor.objects.filter(advisor_type=3).\
            values('advisor_name', 'advisor_netid')
        return {"EOP": list(eop),
                "Premajor": list(prem),
                "International": list(inter)}
