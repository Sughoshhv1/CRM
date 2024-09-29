from django.db import models
from authuser.models import *
from ticket.models import *

# Create your models here.
class Lead(models.Model):
    lead_date = models.DateField()
    tk_name=models.CharField(max_length=200)
    ticket=models.ForeignKey(Ticket,on_delete=models.CASCADE)
    tech=models.ForeignKey(AuthUser,on_delete=models.CASCADE)
    

