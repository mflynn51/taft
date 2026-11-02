
from django.db import models
from shapely.geometry import Polygon


'''
class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userdata")
    name = models.CharField(max_length=50, blank=True, null=True)

    def ___str___ (self):
        return f" {self.user.username}"
'''
        
class GeoPoint(models.Model):
    #id = models.CharField(max_length=10, primary_key=True)
    
    #applicationId = models.CharField(max_length=100)
    #applicationId = models.ForeignKey(WaterRight, on_delete=models.CASCADE, related_name="locations")
    
    latitude = models.FloatField()
    longitude = models.FloatField()
    pod = models.CharField(max_length=12)
    podType = models.CharField(max_length=12)
    podRate = models.IntegerField()
    units = models.CharField(max_length=12)
    podStorage = models.IntegerField()
    owner = models.CharField(max_length=12)
    faceValueAF = models.IntegerField()
    maxDiversionFlow = models.IntegerField()
    unitsFlow = models.CharField(max_length=12)
    status = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.pod}:  {self.latitude}, {self.longitude}, {self.owner}, {self.status}"


class ProductionRecord(models.Model):
    pool = models.CharField(max_length=50)
    year = models.IntegerField()
    variety = models.CharField(max_length=50)
    parcel = models.CharField(max_length=20)
    apn = models.CharField(max_length=20, blank=True)
    ranch = models.CharField(max_length=255)
    ranch_code = models.CharField(max_length=50)
    pack_start = models.DateField(null=True, blank=True)
    pack_end = models.DateField(null=True, blank=True)
    grower = models.CharField(max_length=100)
    block = models.CharField(max_length=100, blank=True)

    bins = models.FloatField(null=True, blank=True, verbose_name="24 WASHINGTON")
    juice = models.FloatField(null=True, blank=True, verbose_name="JUICE")
    culls = models.FloatField(null=True, blank=True, verbose_name="CULLS")

    sunkist_36 = models.FloatField(null=True, blank=True, verbose_name="SUNKIST 36")
    sunkist_40 = models.FloatField(null=True, blank=True, verbose_name="SUNKIST 40")
    sunkist_48 = models.FloatField(null=True, blank=True, verbose_name="SUNKIST 48")
    sunkist_56 = models.FloatField(null=True, blank=True, verbose_name="SUNKIST 56")
    sunkist_72 = models.FloatField(null=True, blank=True, verbose_name="SUNKIST 72")
    sunkist_88 = models.FloatField(null=True, blank=True, verbose_name="SUNKIST 88")
    sunkist_113 = models.FloatField(null=True, blank=True, verbose_name="SUNKIST 113")
    sunkist_138 = models.FloatField(null=True, blank=True, verbose_name="SUNKIST 138")
    sunkist_163 = models.FloatField(null=True, blank=True, verbose_name="SUNKIST 163")
    sunkist_180 = models.FloatField(null=True, blank=True, verbose_name="SUNKIST 180")

    choice_36 = models.FloatField(null=True, blank=True, verbose_name="CHOICE 36")
    choice_40 = models.FloatField(null=True, blank=True, verbose_name="CHOICE 40")
    choice_48 = models.FloatField(null=True, blank=True, verbose_name="CHOICE 48")
    choice_56 = models.FloatField(null=True, blank=True, verbose_name="CHOICE 56")
    choice_72 = models.FloatField(null=True, blank=True, verbose_name="CHOICE 72")
    choice_88 = models.FloatField(null=True, blank=True, verbose_name="CHOICE 88")
    choice_113 = models.FloatField(null=True, blank=True, verbose_name="CHOICE 113")
    choice_138 = models.FloatField(null=True, blank=True, verbose_name="CHOICE 138")
    choice_163 = models.FloatField(null=True, blank=True, verbose_name="CHOICE 163")
    choice_180 = models.FloatField(null=True, blank=True, verbose_name="CHOICE 180")

    sk_exp_brix_36 = models.FloatField(null=True, blank=True, verbose_name="SK EXP BRIX 36")
    sk_exp_brix_40 = models.FloatField(null=True, blank=True, verbose_name="SK EXP BRIX 40")
    sk_exp_brix_48 = models.FloatField(null=True, blank=True, verbose_name="SK EXP BRIX 48")
    sk_exp_brix_56 = models.FloatField(null=True, blank=True, verbose_name="SK EXP BRIX 56")
    sk_exp_brix_72 = models.FloatField(null=True, blank=True, verbose_name="SK EXP BRIX 72")
    sk_exp_brix_88 = models.FloatField(null=True, blank=True, verbose_name="SK EXP BRIX 88")
    sk_exp_brix_113 = models.FloatField(null=True, blank=True, verbose_name="SK EXP BRIX 113")
    sk_exp_brix_138 = models.FloatField(null=True, blank=True, verbose_name="SK EXP BRIX 138")
    sk_exp_brix_163 = models.FloatField(null=True, blank=True, verbose_name="SK EXP BRIX 163")
    sk_exp_brix_180 = models.FloatField(null=True, blank=True, verbose_name="SK EXP BRIX 180")

    sk_export_36 = models.FloatField(null=True, blank=True, verbose_name="SK EXPORT 36")
    sk_export_40 = models.FloatField(null=True, blank=True, verbose_name="SK EXPORT 40")
    sk_export_48 = models.FloatField(null=True, blank=True, verbose_name="SK EXPORT 48")
    sk_export_56 = models.FloatField(null=True, blank=True, verbose_name="SK EXPORT 56")
    sk_export_72 = models.FloatField(null=True, blank=True, verbose_name="SK EXPORT 72")
    sk_export_88 = models.FloatField(null=True, blank=True, verbose_name="SK EXPORT 88")
    sk_export_113 = models.FloatField(null=True, blank=True, verbose_name="SK EXPORT 113")
    sk_export_138 = models.FloatField(null=True, blank=True, verbose_name="SK EXPORT 138")
    sk_export_163 = models.FloatField(null=True, blank=True, verbose_name="SK EXPORT 163")
    sk_export_180 = models.FloatField(null=True, blank=True, verbose_name="SK EXPORT 180")

    sk_exp_hp_36 = models.FloatField(null=True, blank=True, verbose_name="SK EXP HP 36")
    sk_exp_hp_40 = models.FloatField(null=True, blank=True, verbose_name="SK EXP HP 40")
    sk_exp_hp_48 = models.FloatField(null=True, blank=True, verbose_name="SK EXP HP 48")
    sk_exp_hp_56 = models.FloatField(null=True, blank=True, verbose_name="SK EXP HP 56")
    sk_exp_hp_72 = models.FloatField(null=True, blank=True, verbose_name="SK EXP HP 72")
    sk_exp_hp_88 = models.FloatField(null=True, blank=True, verbose_name="SK EXP HP 88")
    sk_exp_hp_113 = models.FloatField(null=True, blank=True, verbose_name="SK EXP HP 113")
    sk_exp_hp_138 = models.FloatField(null=True, blank=True, verbose_name="SK EXP HP 138")
    sk_exp_hp_163 = models.FloatField(null=True, blank=True, verbose_name="SK EXP HP 163")
    sk_exp_hp_180 = models.FloatField(null=True, blank=True, verbose_name="SK EXP HP 180")

    ch_exp_hp_36 = models.FloatField(null=True, blank=True, verbose_name="CH EXP HP 36")
    ch_exp_hp_40 = models.FloatField(null=True, blank=True, verbose_name="CH EXP HP 40")
    ch_exp_hp_48 = models.FloatField(null=True, blank=True, verbose_name="CH EXP HP 48")
    ch_exp_hp_56 = models.FloatField(null=True, blank=True, verbose_name="CH EXP HP 56")
    ch_exp_hp_72 = models.FloatField(null=True, blank=True, verbose_name="CH EXP HP 72")
    ch_exp_hp_88 = models.FloatField(null=True, blank=True, verbose_name="CH EXP HP 88")
    ch_exp_hp_113 = models.FloatField(null=True, blank=True, verbose_name="CH EXP HP 113")
    ch_exp_hp_138 = models.FloatField(null=True, blank=True, verbose_name="CH EXP HP 138")
    ch_exp_hp_163 = models.FloatField(null=True, blank=True, verbose_name="CH EXP HP 163")
    ch_exp_hp_180 = models.FloatField(null=True, blank=True, verbose_name="CH EXP HP 180")

    sk_exp_po_ba_36 = models.FloatField(null=True, blank=True, verbose_name="SK EXP PO/BA 36")
    sk_exp_po_ba_40 = models.FloatField(null=True, blank=True, verbose_name="SK EXP PO/BA 40")
    sk_exp_po_ba_48 = models.FloatField(null=True, blank=True, verbose_name="SK EXP PO/BA 48")
    sk_exp_po_ba_56 = models.FloatField(null=True, blank=True, verbose_name="SK EXP PO/BA 56")
    sk_exp_po_ba_72 = models.FloatField(null=True, blank=True, verbose_name="SK EXP PO/BA 72")
    sk_exp_po_ba_88 = models.FloatField(null=True, blank=True, verbose_name="SK EXP PO/BA 88")
    sk_exp_po_ba_113 = models.FloatField(null=True, blank=True, verbose_name="SK EXP PO/BA 113")
    sk_exp_po_ba_138 = models.FloatField(null=True, blank=True, verbose_name="SK EXP PO/BA 138")
    sk_exp_po_ba_163 = models.FloatField(null=True, blank=True, verbose_name="SK EXP PO/BA 163")
    sk_exp_po_ba_180 = models.FloatField(null=True, blank=True, verbose_name="SK EXP PO/BA 180")

    def __str__(self):
        return f"{self.pool} ({self.year}) - {self.grower}, {self.ranch}"


class TreeBlock(models.Model):
    name = models.CharField(max_length=100)
    apn = models.CharField(max_length=20, blank=True)
    variety = models.CharField(max_length=100)
    bud = models.CharField(max_length=100, blank=True)
    rootstock = models.CharField(max_length=100, blank=True)
    year_planted = models.IntegerField()

    lat1 = models.FloatField()
    lon1 = models.FloatField()
    lat2 = models.FloatField()
    lon2 = models.FloatField()
    lat3 = models.FloatField()
    lon3 = models.FloatField()
    lat4 = models.FloatField()
    lon4 = models.FloatField()
    lat5 = models.FloatField(null=True, blank=True)
    lon5 = models.FloatField(null=True, blank=True)
    lat6 = models.FloatField(null=True, blank=True)
    lon6 = models.FloatField(null=True, blank=True)

    @property
    def coordinates(self):
        points = [
            (self.lon1, self.lat1),
            (self.lon2, self.lat2),
            (self.lon3, self.lat3),
            (self.lon4, self.lat4),
        ]
        if self.lat5 is not None and self.lon5 is not None:
            points.append((self.lon5, self.lat5))
        if self.lat6 is not None and self.lon6 is not None:
            points.append((self.lon6, self.lat6))
        return points

    @property
    def polygon(self):
        return Polygon(self.coordinates)

    def __str__(self):
        return f"{self.name} ({self.variety}, {self.year_planted})"
