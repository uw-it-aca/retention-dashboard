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


class DataPoint(models.Model):
    TYPE_CHOICES = ((1, "Premajor"), (2, "EOP"), (3, "International"))
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    week = models.ForeignKey("Week", on_delete=models.PROTECT)
    student_name = models.TextField()
    student_number = models.IntegerField()
    netid = models.CharField(max_length=12)
    premajor = models.BooleanField()
    is_stem = models.BooleanField(default=False)
    is_freshman = models.BooleanField(default=False)
    priority_score = models.FloatField()
    activity_score = models.FloatField()
    assignment_score = models.FloatField()
    grade_score = models.FloatField()
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
    def filter_by_advisor(data_queryset, advisor_netid):
        """
        Hard code this to EOP advisors for now, if we get other types add that
        filtering here
        """
        advisor = Advisor.objects.get(advisor_netid=advisor_netid,
                                      advisor_type=2)
        return data_queryset.filter(advisor=advisor)

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

    @staticmethod
    def get_all_advisors():
        eop = Advisor.objects.filter(advisor_type=2) \
            .order_by('advisor_name') \
            .filter(~Q(advisor_name="")) \
            .values('advisor_name', 'advisor_netid')
        prem = Advisor.objects.filter(advisor_type=1) \
            .filter(~Q(advisor_name="")) \
            .order_by('advisor_name') \
            .values('advisor_name', 'advisor_netid')
        inter = Advisor.objects.filter(advisor_type=3) \
            .order_by('advisor_name') \
            .filter(~Q(advisor_name="")) \
            .values('advisor_name', 'advisor_netid')
        return {"EOP": list(eop),
                "Premajor": list(prem),
                "International": list(inter)}
