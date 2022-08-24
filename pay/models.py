from django.db import models
from user.models import Region,User
from staff.models import Employe
from autoslug import AutoSlugField
import random
import string 
#import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image,ImageDraw



'''

def random_string_generator(request):
    return ''.join(random.choices(string.ascii_letters , k=20))

def random_string_generator_professionnel(request):
    return ''.join(random.choices(string.ascii_letters , k=19))

ALIAS=(
	("SDE", "SDE"),
	("SENELEC","SENELEC"),
	("UCAD","UCAD",),
	("peage","peage"),
	("nouveau","nouveau")
	)


#Model pour les petits business
class BusinessModel(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	active=models.BooleanField(default=True)
	nom=models.CharField(max_length=255)
	description_business=models.TextField()
	contact=models.CharField(max_length=255)
	slug=AutoSlugField(populate_from=random_string_generator,unique=True)
	adress=models.ForeignKey(Region,on_delete=models.PROTECT)
	logo=models.ImageField(upload_to='static/media')
	document=models.FileField(upload_to='static/document')
	created=models.DateTimeField(auto_now_add=True)
	task_number=models.PositiveIntegerField(default=0)

#Qr code pour les business
class CodeGenerate(models.Model):
	business=models.OneToOneField(BusinessModel,on_delete=models.CASCADE)
	code=models.ImageField(upload_to='static/media',blank=True)

	def save(self,*args,**kwargs):
		img = qrcode.make(self.business.slug)
		qr_offset=Image.new('RGB',(310,310),'white')
		qr_offset.paste(img)
		file_name=self.business.nom+"-"+str(self.business.id)+"qr.png"
		stream=BytesIO()
		qr_offset.save(stream,'PNG')
		self.code.save(file_name,File(stream),save=False)
		qr_offset.close()
		super().save(*args,**kwargs)

#Transaction pour les petits business
class PayementBusiness(models.Model):
	nom_complet_client=models.CharField(max_length=255,null=True,blank=True)
	somme=models.DecimalField(max_digits=19, decimal_places=2)
	commission=models.DecimalField(max_digits=19, decimal_places=2,default=0)
	message=models.TextField()
	business=models.ForeignKey(BusinessModel,on_delete=models.PROTECT)
	created=models.DateTimeField(auto_now_add=True,blank=True,null=True)
	total=models.DecimalField(max_digits=19, decimal_places=2,default=0)
	relever=models.BooleanField(default=False)



#GaalguiPay 
class PayModel(models.Model):
	alias=models.CharField(max_length=100,choices=ALIAS,default="nouveau")
	adress=models.ForeignKey(Region,on_delete=models.CASCADE)
	active=models.BooleanField(default=False)
	logo=models.ImageField(upload_to='static/media',blank=True,null=True)

#Model pour les grandes entreprises
class Professionel(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	active=models.BooleanField(default=False)
	business_desription=models.TextField()
	nom=models.CharField(max_length=255)
	adress=models.ForeignKey(Region,on_delete=models.PROTECT)
	contact=models.CharField(max_length=255)
	logo=models.ImageField(upload_to='static/media')
	created=models.DateTimeField(auto_now_add=True)
	slug=AutoSlugField(populate_from=random_string_generator_professionnel,unique=True)
	document=models.FileField(upload_to='static/media')
	task_number=models.PositiveIntegerField(default=0)
	paymodel=models.ForeignKey(PayModel,on_delete=models.PROTECT,blank=True,null=True)
	


#Payement pour les grandes entreprises
class PayementProfessionnel(models.Model):
	message=models.TextField()
	nom_complet_client=models.CharField(max_length=255)
	montant=models.DecimalField( max_digits=19, decimal_places=2)
	created=models.DateTimeField(auto_now_add=True)
	employe=models.ForeignKey(Employe,on_delete=models.PROTECT,null=True,blank=True)
	professionnel=models.ForeignKey(Professionel,on_delete=models.PROTECT)
	relever=models.BooleanField(default=False)



#Qr code pour les professionnels
class CodeGenerateProfessionnel(models.Model):
	professionnel=models.OneToOneField(Professionel,on_delete=models.CASCADE)
	code=models.ImageField(upload_to='static/media',blank=True)
	
	def save(self,*args,**kwargs):
		img = qrcode.make(self.professionnel.slug)
		qr_offset=Image.new('RGB',(310,310),'white')
		qr_offset.paste(img)
		file_name=self.professionnel.nom+"-"+str(self.professionnel.id)+"qr.png"
		stream=BytesIO()
		qr_offset.save(stream,'PNG')
		self.code.save(file_name,File(stream),save=False)
		qr_offset.close()
		super().save(*args,**kwargs)


class PayementPeriodic(models.Model):
	professionnel=models.ForeignKey(Professionel,on_delete=models.PROTECT,blank=True,null=True)
	business=models.ForeignKey(BusinessModel,on_delete=models.PROTECT,blank=True,null=True)
	montant=models.DecimalField( max_digits=19, decimal_places=2)
	created=models.DateTimeField(auto_now_add=True)
	relever=models.BooleanField(default=False)


class SuspensionPayementPeriodic(models.Model):
	professionnel=models.ForeignKey(Professionel,on_delete=models.PROTECT,blank=True,null=True)
	business=models.ForeignKey(BusinessModel,on_delete=models.PROTECT,blank=True,null=True)
	montant=models.DecimalField( max_digits=19, decimal_places=2)
	created=models.DateTimeField(auto_now_add=True)
	relever=models.BooleanField(default=False)'''









 






	












