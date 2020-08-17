from django.db import models


class PiiData(models.Model):
    cc_number = models.CharField(max_length=200)
    cc_exp = models.CharField(max_length=200)
    cc_cvv = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


    #def __str__(self):
       #return self.pub_date.__str__() + " | cc_number: " + self.cc_number + "; cc_exp: " + self.cc_exp + "; cc_cvv: " + self.cc_cvv