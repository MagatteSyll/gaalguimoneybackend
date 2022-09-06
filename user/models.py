from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from datetime import datetime, timedelta
from autoslug import AutoSlugField
import random
import string 
from io import BytesIO
from django.core.files import File 
from PIL import Image,ImageDraw
import qrcode


def random_string_generator(request):
    return ''.join(random.choices(string.ascii_letters , k=20))

NATURE_TRANSACTION= (
    ("envoi direct", "envoi direct"),
    ("envoi via code", "envoi via code"), 
    ("depot", "depot"), 
    ("retrait", "retrait"),
    ("reception", "reception"),
    ("payement", "payement"),
    ("code","code"),
    ("retrait par code","retrait par code"),
    ("annulation commande","annulation commande"),
    ("activation compte","activation compte"),
    ("reception payement","reception payement")
    )



class Pays(models.Model):
	name=models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Region(models.Model):
	region=models.CharField(max_length=100)
	pays=models.ForeignKey(Pays,on_delete=models.CASCADE,)

class PointAcces(models.Model):

	adress=models.CharField(max_length=255)
	region=models.ForeignKey(Region,on_delete=models.CASCADE)

	def __str__(self):
		return self.adress
 
#Gestion utilisateur 
class UserManager(BaseUserManager):
	def create_user(self,nom,prenom,phone,password=None,is_staff=False,is_admin=False):
		if not phone:
			raise ValueError('phone obligatoire')
		if not password:
			raise ValueError('password obligatoire')
		if not nom:
			raise ValueError('entrez un nom')
		if not prenom:
			raise ValueError('entrez un prenom')
				
		self.phone=phone		
		user = self.model(phone=phone)	
		user.set_password(password)
		user.nom=nom
		user.prenom= prenom
		user.is_staff=is_staff
		user.is_admin=is_admin
		user.save(using=self._db)
		return user

	def create_superuser(self,nom,prenom,phone,password=None):
		user=self.create_user(
			phone=phone,
			password=password,
			nom=nom,
			prenom =prenom,
			is_staff=True,is_admin=True
			)
		return user

	def create_staff(self,nom,prenom,phone,password=None):
		user=self.create_user(
			phone=phone,
			password=password,
			nom=nom,
			prenom=prenom,
			is_staff=True,is_admin=False
			)
		return user	
#Utilisateur
class User(AbstractBaseUser):
	phone = PhoneNumberField(unique=True)
	active = models.BooleanField(default=True)
	prenom = models.CharField(max_length=100)
	nom =models.CharField(max_length=100)
	conform_phone=models.BooleanField(default=False)
	date_joined=models.DateTimeField(auto_now_add=True)
	solde=models.DecimalField(default=0, max_digits=19, decimal_places=2)
	professionnel=models.BooleanField(default=False)
	business=models.BooleanField(default=False)
	room=AutoSlugField(populate_from=random_string_generator,unique=True)
	group=AutoSlugField(populate_from=random_string_generator,unique=True)
	channel=AutoSlugField(populate_from=random_string_generator,unique=True)
	nature_document=models.CharField(max_length=255,default='pas de document')
	numero_document=models.CharField(max_length=255,default='0')
	document_verif=models.BooleanField(default=False)
	is_staff=models.BooleanField(default=False)
	is_admin=models.BooleanField(default=False)
	is_staff_simple=models.BooleanField(default=False)
	is_staff_bureau=models.BooleanField(default=False)
	is_staff_comptable=models.BooleanField(default=False)
	is_staff_manager=models.BooleanField(default=False)
	is_staff_techique=models.BooleanField(default=False)
	is_staff_manager_personnel=models.BooleanField(default=False)
	#point_acces=models.ForeignKey(PointAcces,on_delete=models.PROTECT,null=True,blank=True)

	
	REQUIRED_FIELDS= ['prenom','nom']
	USERNAME_FIELD ='phone'
	objects=UserManager()

	def get_prenom(self):
		return self.prenom
	def get_nom(self):
		return self.nom	

	def has_perm(self,perm,obj=None):
		return True

	def has_module_perms(self,app_label):
		return True
	def __str__(self):
		return str(self.phone)

class QrCodeClient(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	code=models.ImageField(upload_to='static/media',blank=True)
	def save(self,*args,**kwargs):
		img = qrcode.make(self.user.channel)
		qr_offset=Image.new('RGB',(310,310),'white')
		qr_offset.paste(img)
		file_name=self.user.nom+"-"+str(self.user.id)+"qr.png"
		stream=BytesIO()
		qr_offset.save(stream,'PNG')
		self.code.save(file_name,File(stream),save=False)
		qr_offset.close()
		super().save(*args,**kwargs)
  

class Employe(models.Model):
	user=models.OneToOneField(User,on_delete=models.PROTECT)
	point_acces=models.ForeignKey(PointAcces,on_delete=models.CASCADE)
	active=models.BooleanField(default=False)
	

#Envoi direct d un utilisateur a un autre
class Envoi(models.Model):
	envoyeur=models.ForeignKey(User,on_delete=models.PROTECT)
	phone_receveur=PhoneNumberField()
	somme=models.DecimalField( max_digits=19, decimal_places=2)
	created=models.DateTimeField(auto_now_add=True)
	commission=models.DecimalField(max_digits=19, decimal_places=2,default=0)
	relever=models.BooleanField(default=False)
	total=models.DecimalField(max_digits=19, decimal_places=2,default=0)


#Depot ,agence
class Depot(models.Model):
	depositaire=models.ForeignKey(User,on_delete=models.PROTECT)
	somme=models.DecimalField( max_digits=19, decimal_places=2)
	created=models.DateTimeField(auto_now_add=True)
	employe=models.ForeignKey(Employe,on_delete=models.CASCADE)
	relever=models.BooleanField(default=False)

	

#Retrait a partir d un  compte  
class Retrait(models.Model):
	beneficiaire=models.ForeignKey(User,on_delete=models.PROTECT)
	somme=models.DecimalField( max_digits=19, decimal_places=2)
	created=models.DateTimeField(auto_now_add=True)
	employe=models.ForeignKey(Employe,on_delete=models.CASCADE)
	relever=models.BooleanField(default=False)


#Retrait par code 
class RetraitCode(models.Model):
	beneficiaire=models.CharField(max_length=255)
	somme=models.DecimalField( max_digits=19, decimal_places=2)
	created=models.DateTimeField(auto_now_add=True)
	employe=models.ForeignKey(Employe,on_delete=models.CASCADE)
	relever=models.BooleanField(default=False)
	code=models.PositiveIntegerField()

	

#Envoi avec code 
class ViaCode(models.Model):
	code=models.PositiveIntegerField(unique=True)
	Nom_complet_du_receveur=models.CharField(max_length=255)
	Nom_complet_de_l_envoyeur=models.CharField(max_length=255,blank=True,null=True)
	client=models.ForeignKey(User,on_delete=models.PROTECT,blank=True,null=True)
	somme=models.DecimalField( max_digits=19, decimal_places=2)
	active=models.BooleanField(default=False)
	retirer=models.BooleanField(default=False)
	created=models.DateTimeField(auto_now_add=True)
	phone_beneficiaire=PhoneNumberField()
	commission=models.DecimalField(max_digits=19, decimal_places=2,default=0)
	employe=models.ForeignKey(Employe,blank=True,null=True,on_delete=models.CASCADE)
	relever=models.BooleanField(default=False)
	total=models.DecimalField(max_digits=19, decimal_places=2,default=0)


	

#Historiques transactions
class Messages(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	message=models.TextField()
	created=models.DateTimeField(auto_now_add=True)
	nature_transaction=models.CharField(max_length=100, choices=NATURE_TRANSACTION)
	montant=models.DecimalField( max_digits=19, decimal_places=2,default=0)
	commission=models.DecimalField( max_digits=19, decimal_places=2,default=0)
	beneficiaire=models.CharField(max_length=200,null=True,blank=True)
	code=models.PositiveIntegerField(null=True,blank=True)
	total=models.DecimalField( max_digits=19, decimal_places=2,default=0)
	donnateur=models.CharField(max_length=255,null=True,blank=True)
	logo=models.ImageField(upload_to='static/media',blank=True)
	should_notify=models.BooleanField(default=False)
	is_trans=models.BooleanField(default=True)
	lu=models.BooleanField(default=False)
	


class VerificationTransaction(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
	phone_destinataire=PhoneNumberField(blank=True,null=True)
	nom_complet_destinataire=models.CharField(max_length=255,null=True,blank=True)
	nom_complet_client=models.CharField(max_length=255,null=True,blank=True)
	created=models.DateTimeField(auto_now_add=True)
	somme=models.DecimalField(max_digits=19, decimal_places=2)
	commission=models.DecimalField( max_digits=19, decimal_places=2)
	nature_transaction=models.CharField(max_length=255, choices=NATURE_TRANSACTION,blank=True)
	employe=models.ForeignKey(Employe,null=True,blank=True,on_delete=models.CASCADE)
	reste=models.DecimalField(max_digits=19, decimal_places=2,default=0)
	commission_incluse=models.BooleanField(default=False)
	total=models.DecimalField(max_digits=19, decimal_places=2,default=0)
	code=models.PositiveIntegerField(default=0)

	def __str__(self):
		return (self.user.nom)



'''
class PhoneVerificationCode(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	code=models.PositiveIntegerField(unique=True)
	created=models.DateTimeField(auto_now_add=True)
	active=models.BooleanField(default=False)'''


class PayementGaalgui(models.Model):
	user=models.ForeignKey(User,on_delete=models.PROTECT)
	livraison=models.DecimalField(default=0, max_digits=19, decimal_places=2)
	commission=models.DecimalField(default=0, max_digits=19, decimal_places=2)
	total=models.DecimalField(default=0, max_digits=19, decimal_places=2)
	created=models.DateTimeField(auto_now_add=True)
	active=models.BooleanField(default=True)
	relever=models.BooleanField(default=False)
	annuler=models.BooleanField(default=False)
	prix=models.DecimalField(default=0, max_digits=19, decimal_places=2)
	nom=models.CharField(max_length=255,null=True,blank=True)


class AnnulationGaalguiShop(models.Model):
	payement=models.ForeignKey(PayementGaalgui,on_delete=models.CASCADE)
	relever=models.BooleanField(default=False)
	
class PhoneConfirmation(models.Model):
	phone=PhoneNumberField()
	code=models.PositiveIntegerField(unique=True) 
	active=models.BooleanField(default=False)
	created=models.DateTimeField(auto_now_add=True)







	



	






		



	
 
	


	


		
	
	
		

