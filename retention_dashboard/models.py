# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

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
                "year": self.year,
                "quarter": self.get_quarter_display(),
                "number": self.number,
                "text": display_string}

    @classmethod
    def sis_term_to_quarter_number(cls, sis_term_id):
        term = None
        try:
            term = sis_term_id.split("-")[1].lower()
        except IndexError:
            pass
        if term == "winter":
            return 1
        elif term == "spring":
            return 2
        elif term == "summer":
            return 3
        elif term == "autumn":
            return 4
        else:
            raise ValueError(f"Unable to determine quarter number for "
                             f"sis_term_id={sis_term_id}")


class UploadTypes():
    premajor = 1
    eop = 2
    international = 3
    iss = 4
    tacoma = 5


class DataPoint(models.Model):
    TYPE_CHOICES = ((UploadTypes.premajor, "Premajor"),
                    (UploadTypes.eop, "EOP"),
                    (UploadTypes.international, "International"),
                    (UploadTypes.iss, "ISS"),
                    (UploadTypes.tacoma, "Tacoma"))
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    week = models.ForeignKey("Week", on_delete=models.PROTECT)
    student_name = models.TextField()
    student_number = models.IntegerField()
    netid = models.CharField(max_length=12)
    premajor = models.BooleanField()
    is_stem = models.BooleanField(default=False)
    is_freshman = models.BooleanField(default=False)
    priority_score = models.FloatField(null=True)
    activity_score = models.FloatField(null=True)
    assignment_score = models.FloatField(null=True)
    grade_score = models.FloatField(null=True)
    signin_score = models.FloatField(default=0.0)
    upload = models.ForeignKey("Upload", on_delete=models.CASCADE)
    advisor = models.ForeignKey("Advisor", on_delete=models.PROTECT, null=True)
    has_a_term = models.BooleanField(default=False)
    has_b_term = models.BooleanField(default=False)
    has_full_term = models.BooleanField(default=False)

    def get_first_last_name(self):
        try:
            parts = self.student_name.split(",", 1)
            return parts[1], parts[0]
        except IndexError:
            try:
                parts = self.student_name.split(" ", 1)
                return parts[1], parts[0]
            except IndexError:
                return "", self.student_name

    @staticmethod
    def get_data_type_by_text(type_str):
        try:
            return [t for t in list(DataPoint.TYPE_CHOICES)
                    if t[1] == type_str][0][0]
        except IndexError:
            raise ValueError("Unkown type {}".format(type_str))

    @staticmethod
    def get_data_by_type_week(type, week):
        type_int = [item for item in
                    DataPoint.TYPE_CHOICES
                    if type in item][0][0]
        data = DataPoint.objects.filter(type=type_int,
                                        week=week).prefetch_related('advisor')
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
    def filter_by_summer(data_queryset, summer_terms):
        queries = []
        if "a" in summer_terms:
            queries.append(Q(has_a_term=True))
        if "b" in summer_terms:
            queries.append(Q(has_b_term=True))
        if "full" in summer_terms:
            queries.append(Q(has_full_term=True))

        query = queries.pop()
        for item in queries:
            query &= item
        return data_queryset.filter(query)

    @staticmethod
    def filter_by_premajor(data_queryset, is_premajor):
        return data_queryset.filter(premajor=is_premajor)

    @staticmethod
    def filter_by_freshman(data_queryset, is_freshman):
        return data_queryset.filter(is_freshman=is_freshman)

    @staticmethod
    def filter_by_stem(data_queryset, is_stem):
        return data_queryset.filter(is_stem=is_stem)

    @staticmethod
    def filter_by_advisor(data_queryset, advisor_netid, advisor_type):
        advisor_type_id = DataPoint.get_data_type_by_text(advisor_type)
        return (data_queryset
                .filter(advisor__advisor_netid=advisor_netid)
                .filter(advisor__advisor_type=advisor_type_id))

    def get_summer_string(self):
        term_list = []
        if self.has_a_term:
            term_list.append("A")
        if self.has_b_term:
            term_list.append("B")
        if self.has_full_term:
            term_list.append("Full")
        return ', '.join(map(str, term_list))

    def json_data(self):
        first, last = self.get_first_last_name()
        resp = {"student_first_name": first,
                "student_last_name": last,
                "student_number": self.student_number,
                "netid": self.netid,
                "priority_score": self.priority_score,
                "activity_score": self.activity_score,
                "assignment_score": self.assignment_score,
                "grade_score": self.grade_score,
                "signin_score": self.signin_score,
                "is_premajor": self.premajor,
                "is_freshman": self.is_freshman,
                "is_stem": self.is_stem,
                "summer_term_string": self.get_summer_string()
                }
        if self.advisor is not None:
            resp["advisor_name"] = self.advisor.advisor_name
            resp["advisor_netid"] = self.advisor.advisor_netid

        return resp


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

    class Meta:
        unique_together = ('advisor_netid', 'advisor_type')

    @classmethod
    def get_advisor_by_type(cls, advisor_type):
        return Advisor.objects.filter(advisor_type=advisor_type) \
            .order_by('advisor_name') \
            .filter(~Q(advisor_name="")) \
            .values('advisor_name', 'advisor_netid')

    @classmethod
    def get_all_advisors(cls):
        prem = cls.get_advisor_by_type(1)
        eop = cls.get_advisor_by_type(2)
        inter = cls.get_advisor_by_type(3)
        iss = cls.get_advisor_by_type(4)
        tacoma = cls.get_advisor_by_type(5)
        return {"Premajor": list(prem),
                "EOP": list(eop),
                "International": list(inter),
                "ISS": list(iss),
                "Tacoma": list(tacoma)}
