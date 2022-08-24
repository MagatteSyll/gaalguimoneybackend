from django.db import models
from user.models import Employe,PointAcces
from autoslug import AutoSlugField
import random
import string 




def random_string_generator(request):
    return ''.join(random.choices(string.ascii_letters , k=20))

NATURE_ACTION_STAFF=(
   ("depot","depot"),
   ("retrait","retrait"),
   ("retrait code","retrait code"),
   ("envoi code","envoi code"),
   ("payement","payement"),
   ("activation","activation"),
   ('desactivation','desactivation'),
   ("reactivation","reactivation"),
   ("creation de compte business","creation de compte business"),
   ("creation de compte professionnel","creation de compte professionnel"),
   ("ajout de publicite","ajout de publicite"),
   ("nouveau membre staff","nouveau membre staff")

	)






class NotificationStaff(models.Model):
	employe=models.ForeignKey(Employe,on_delete=models.PROTECT)
	notification=models.TextField()
	created=models.DateTimeField(auto_now_add=True)

class NotificationAdmina(models.Model):
	employe=models.ForeignKey(Employe,on_delete=models.CASCADE)
	somme=models.DecimalField( max_digits=19, decimal_places=2)
	nature=models.CharField(max_length=255, choices=NATURE_ACTION_STAFF)
	created=models.DateTimeField(auto_now_add=True)
	client=models.CharField(max_length=255)


class ActionStaff(models.Model):
	employe=models.ForeignKey(Employe,on_delete=models.PROTECT,)
	action=models.TextField()
	created=models.DateTimeField(auto_now_add=True)
	nature=models.CharField(max_length=255, choices=NATURE_ACTION_STAFF,)
	montant_rentrant=models.DecimalField( max_digits=19, decimal_places=2,default=0)
	montant_entreprise=models.DecimalField( max_digits=19, decimal_places=2,default=0)


class TendancePub(models.Model):
	image=models.ImageField(upload_to='static/media')
	description=models.TextField()
	active=models.BooleanField(default=True)
