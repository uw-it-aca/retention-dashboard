# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from django.db.models import Q, F


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
    def term_to_quarter_number(cls, term):
        term = term.lower()
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
                             f"term={term}")

    @classmethod
    def sis_term_to_quarter_number(cls, sis_term_id):
        term = None
        try:
            term = sis_term_id.split("-")[1].lower()
        except IndexError:
            raise ValueError(f"Unable to determine term for "
                             f"sis_term_id={sis_term_id}")
        try:
            return Week.term_to_quarter_number(term)
        except ValueError:
            raise ValueError(f"Unable to determine quarter number for "
                             f"sis_term_id={sis_term_id}")


class UploadTypes():
    premajor = 1
    eop = 2
    international = 3
    iss = 4
    tacoma = 5
    athletic = 6


class Sport(models.Model):
    sport_code = models.IntegerField()

    @property
    def sport_desc(self):
        descs = {
            1: "BASEBALL-MEN",
            2: "SOFTBALL-WOMEN",
            3: "BASKETBALL-MEN",
            4: "BASKETBALL-WMN",
            5: "CREW-MENV",
            6: "CREW-WOMENV",
            7: "FOOTBALL-MEN",
            8: "FTBL-WOMEN",
            9: "GOLF-MEN",
            10: "GOLF-WOMEN",
            11: "GYMN-MEN",
            12: "GYMN-WOMEN",
            13: "SOCR-MEN",
            14: "SOCR-WOMEN",
            15: "SWIM-MEN",
            16: "SWIM-WOMEN",
            17: "TENS-MEN",
            18: "TENS-WOMEN",
            19: "TRACK-MEN",
            20: "TRACK-WOMEN",
            22: "VLYB-WOMEN",
            23: "CROSS COUNTRY-M",
            24: "CROSS COUNTRY-W",
            25: "TRACK-INDOOR M",
            26: "TRACK-INDOOR W",
            27: "CREWN-MEN",
            28: "CREWN-WOMEN",
            29: "NONPARTICIPANTS",
            35: "NO ATH STATUS",
            40: "PERM INJURY FBL",
            41: "WIDE RECEIV FBL",
            42: "OFFENSE LNE FBL",
            43: "TEND KICKER FBL",
            44: "QUARTERBACK FBL",
            45: "RUNING BACK FBL",
            46: "DEFENS LINE FBL",
            47: "LINEBACKERS FBL",
            48: "DEFENS BACK FBL",
            49: "CORNER BACK FBL",
            51: "INACTIVE BASEBL",
            52: "INACTIVE SOFTBL",
            53: "INACTIVE BASKET M",
            54: "INACTIVE BASKET W",
            55: "INACTIVE CREWV M",
            56: "INACTIVE CREWV W",
            57: "INACTIVE FTBALL",
            59: "INACTIVE GOLF M",
            60: "INACTIVE GOLF W",
            62: "INACTIVE GYMN",
            63: "INACTIVE SOC",
            64: "INACT SOCCER W",
            65: "INACTIVE SWIM M",
            66: "INACTIVE SWIM W",
            67: "INACTIVE TENNIS M",
            68: "INACTIVE TENNIS W",
            69: "INACTIVE TRACK M",
            70: "INACTIVE TRACK W",
            72: "INACTIVE VOLBL",
            73: "INACTIVE CCNTRY M",
            74: "INACTIVE CCNTRY W",
            75: "INACT TR IND M",
            76: "INACT TR IND W",
            77: "INACTIVE CREMN M",
            78: "INACTIVE CREWN W",
            96: "REC W A AID",
            97: "REC NO A AID",
            98: "N REC W ATH AID",
            99: "N REC NO A AID",
            30: "SAND VOLLEYBL-W",
            80: "INACT SAND VLB"
        }
        return descs[self.sport_code]

    @classmethod
    def get_sport_by_type(cls, datapoint_type, week):
        dps = DataPoint.objects.filter(type=datapoint_type) \
            .filter(week=week) \
            .annotate(sport_code=F('sports__sport_code')) \
            .order_by('sport_code') \
            .filter(~Q(sport_code=None))
        sports = []
        for dp in dps:
            for sport in dp.sports.all():
                if (sport.sport_code not in
                        [sport["sport_code"] for sport in sports]):
                    sports.append(
                        {'sport_code': sport.sport_code,
                         'sport_desc': sport.sport_desc})
        return sorted(sports, key=lambda x: x["sport_desc"])

    @classmethod
    def get_all_sports(cls, week_number, quarter, year):
        week = Week.objects.filter(
            number=week_number,
            quarter=Week.term_to_quarter_number(quarter),
            year=year).get()
        prem = cls.get_sport_by_type(1, week)
        eop = cls.get_sport_by_type(2, week)
        inter = cls.get_sport_by_type(3, week)
        iss = cls.get_sport_by_type(4, week)
        tacoma = cls.get_sport_by_type(5, week)
        athletic = cls.get_sport_by_type(6, week)
        return {"Premajor": list(prem),
                "EOP": list(eop),
                "International": list(inter),
                "ISS": list(iss),
                "Tacoma": list(tacoma),
                "Athletics": list(athletic)}


class DataPoint(models.Model):
    TYPE_CHOICES = ((UploadTypes.premajor, "Premajor"),
                    (UploadTypes.eop, "EOP"),
                    (UploadTypes.international, "International"),
                    (UploadTypes.iss, "ISS"),
                    (UploadTypes.tacoma, "Tacoma"),
                    (UploadTypes.athletic, "Athletics"))
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    week = models.ForeignKey("Week", on_delete=models.PROTECT)
    student_name = models.TextField()
    student_number = models.IntegerField()
    netid = models.CharField(max_length=12)
    campus_code = models.CharField(max_length=2, null=True)
    class_code = models.CharField(max_length=2, null=True)
    premajor = models.BooleanField()
    eop = models.BooleanField(default=False)
    iss = models.BooleanField(default=False)
    international = models.BooleanField(default=False)
    is_stem = models.BooleanField(default=False)
    is_freshman = models.BooleanField(default=False)
    priority_score = models.FloatField(null=True)
    activity_score = models.FloatField(null=True)
    assignment_score = models.FloatField(null=True)
    grade_score = models.FloatField(null=True)
    signin_score = models.FloatField(default=0.0)
    upload = models.ForeignKey("Upload", on_delete=models.CASCADE)
    advisor = models.ForeignKey("Advisor", on_delete=models.PROTECT, null=True)
    sports = models.ManyToManyField("Sport")
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
        types = [item for item in DataPoint.TYPE_CHOICES
                 if type in item]
        if types:
            type_int = [item for item in
                        DataPoint.TYPE_CHOICES
                        if type in item][0][0]
            data = DataPoint.objects.filter(
                type=type_int,
                week=week).prefetch_related('advisor')
            return data
        else:
            return []

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
    def filter_by_class_standing(data_queryset, class_standing_filter):
        return data_queryset.filter(class_code=class_standing_filter)

    @staticmethod
    def filter_by_sports(data_queryset, sport_code_filter):
        return data_queryset.filter(sports__sport_code=sport_code_filter)

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

    def get_class_desc(self):
        class_codes_map = {
            0: "Pending",
            1: "Freshman",
            2: "Sophomore",
            3: "Junior",
            4: "Senior",
            5: "5th-Year",
            6: "Non-Matriculated",
            8: "Graduate",
            11: "1st Year Professional",
            12: "2nd Year Professional",
            13: "3rd Year Professional",
            14: "4th Year Professional",
        }
        if self.class_code is not None:
            return class_codes_map.get(int(self.class_code))

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
                "is_eop": self.eop,
                "is_iss": self.iss,
                "is_international": self.international,
                "is_freshman": self.is_freshman,
                "is_stem": self.is_stem,
                "is_athlete": self.sports.exists(),
                "summer_term_string": self.get_summer_string(),
                "class_desc": self.get_class_desc(),
                "campus_code": self.campus_code
                }
        if self.advisor is not None:
            resp["advisor_name"] = self.advisor.advisor_name
            resp["advisor_netid"] = self.advisor.advisor_netid

        return resp

    @classmethod
    def get_class_standing_by_type(cls, datapoint_type, week):
        dps = DataPoint.objects.filter(type=datapoint_type) \
            .filter(week=week) \
            .order_by("class_code")
        class_standings = {}
        for dp in dps:
            if dp.class_code:
                class_standings[dp.class_code] = \
                    {"class_code": int(dp.class_code),
                     "class_desc": dp.get_class_desc()}
        return sorted(class_standings.values(),
                      key=lambda i: i['class_code'])

    @classmethod
    def get_all_class_standings(cls, week_number, quarter, year):
        week = Week.objects.filter(
            number=week_number,
            quarter=Week.term_to_quarter_number(quarter),
            year=year).get()
        prem = cls.get_class_standing_by_type(1, week)
        eop = cls.get_class_standing_by_type(2, week)
        inter = cls.get_class_standing_by_type(3, week)
        iss = cls.get_class_standing_by_type(4, week)
        tacoma = cls.get_class_standing_by_type(5, week)
        athletic = cls.get_class_standing_by_type(6, week)
        return {"Premajor": list(prem),
                "EOP": list(eop),
                "International": list(inter),
                "ISS": list(iss),
                "Tacoma": list(tacoma),
                "Athletics": list(athletic)}


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
        athletic = cls.get_advisor_by_type(6)
        return {"Premajor": list(prem),
                "EOP": list(eop),
                "International": list(inter),
                "ISS": list(iss),
                "Tacoma": list(tacoma),
                "Athletics": list(athletic)}
