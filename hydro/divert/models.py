
from django.db import models


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
    pod = models.CharField(max_length=100)
    podType = models.CharField(max_length=12)
    podRate = models.IntegerField()
    units = models.CharField(max_length=12)
    podStorage = models.IntegerField()
    owner = models.CharField(max_length=100)
    faceValueAF = models.IntegerField()
    maxDiversionFlow = models.IntegerField()
    unitsFlow = models.CharField(max_length=12)
    status = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.pod}:  {self.latitude}, {self.longitude}, {self.owner}, {self.status}"
