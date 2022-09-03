from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import*
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import  permissions
from random import randint
from .models import User
from .notification import EnvoiDirectNotif,EnvoiViaCodeNotif ,PayementEgaalgui,CodePayementEGaalgui,notifpayement
from rest_framework import filters
#import requests
from decimal import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
#from .payement import foo
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from celery import shared_task
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from staff.models import*
from staff.serializer import*
from pay.models import*
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from fcm_django.models import FCMDevice
from django.http import JsonResponse
import vonage



 

client = vonage.Client(key="ba6aaf96", secret="kF38qLBVLFdlXFfG")
sms = vonage.Sms(client)
def SMSVerif(numero,code):
	responseData = sms.send_message(
		{
        "from": "GaalguiMoney",
        "to": numero,
        "text": "Le code de confirmation de votre numero est "+" "+ str(code)
        }
        )
	if responseData["messages"][0]["status"] == "0":
		print('message envoye')
	else:
		print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
class MyPaginationClass(PageNumberPagination):
    page_size = 15 
    page_size_query_param = 'page_size'

'''class ProdutVendu(generics.ListAPIView):
	pagination_class =MyPaginationClass
	serializer_class=CommandeSerializer
	
	def get_queryset(self, *args, **kwargs):
		user=self.request.user
		produits=Produit.objects.filter(vendeur=user,vendu=True,recycler=False,desactiver=False).order_by('-id')
		return produits
'''

#Payement periodique compte business
'''@shared_task
def payement(user_id,somme,name):
	user=User.objects.get(id=user_id)
	montantdelay=-2*somme
	admina=User.objects.get(phone='+79649642176')
	business=BusinessModel.objects.get(user=user)
	if user.solde<=montantdelay:
		business=BusinessModel.objects.get(user=user)
		task=PeriodicTask.objects.get(name=name)
		montant=abs(user.solde)
		SuspensionPayementPeriodic.objects.create(business=business,montant=montant,relever=False)
		admina.solde-=user.solde
		admina.save()
		task.delete()
		business.active=False
		business.save()
		user.business=False
		user.save()

		#Notification d annulation du compte professionnel
	else:
		
		user.solde-=somme
		user.save()
		admina.solde+=somme
		admina.save()
		PayementPeriodic.objects.create(business=business,montant=somme,relever=False)
		notifpayement(user,somme)

@shared_task
def payementprofessionnel(user_id,somme,name):
	user=User.objects.get(id=user_id)
	montantdelay=-2*somme
	admina=User.objects.get(phone='+79649642176')
	professionnel=Professionel.objects.get(user=user)
	if user.solde<=montantdelay:
		professionnel=Professionel.objects.get(user=user)
		pay=PayModel.objects.get(professionnel=professionnel)
		pay.active=False
		pay.save()
		task=PeriodicTask.objects.get(name=name)
		montant=abs(user.solde)
		SuspensionPayementPeriodic.objects.create(professionnel=professionnel,montant=montant,relever=False)
		admina.solde-=user.solde
		admina.save()
		task.delete()
		professionnel.active=False
		professionnel.save()
		user.professionnel=False
		user.save()
		#Notification d annulation du compte professionnel
	else:
		
		user.solde-=somme
		user.save()
		admina.solde+=somme
		admina.save()
		PayementPeriodic.objects.create(professionnel=professionnel,montant=somme,relever=False)
		notifpayement(user,somme)'''



def index(request):
	devices = FCMDevice.objects.filter(user__phone='+221772058140')
	#for device in devices:
	#device.send_message(Message(data={"titre": "Le titre","body":"le body"}))
	responseData = sms.send_message(
		{
        "from": "GaalguiMoney",
        "to": "79649642176",
        "text": "Le code de confirmation de votre numero est"
        }
        )
	if responseData["messages"][0]["status"] == "0":
		print('message envoye')
	else:
		print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
		
	
	return JsonResponse({'status':'OK'})
	

class MyTokenObtainPairView(TokenObtainPairView):
	serializer_class = MyTokenObtainPairSerializer

class MyTokenRefreshPairView(TokenRefreshView):
	serializer_class=MyTokenObtainPairSerializer 

#Verifiation du numero avant inscription
class ValidNumber(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		id=data['id']
		user=User.objects.get(id=id)
		code_id=data['code_id']
		code=int(data['code'])
		verif=PhoneVerificationCode.objects.get(id=code_id,active=True)
		if verif.code==code:
			user.active=True
			user.save()
			verif.active=False 
			verif.save()
			return Response({'succes':'registration'})

class GetCodeInscription(APIView):
	permission_classes=[permissions.AllowAny]
	def post(self,request):
		phone=request.data.get('phone')
		ifuser=User.objects.filter(phone=phone).count()
		phonecode=PhoneConfirmation.objects.filter(phone=phone).count()
		if ifuser==0 and phonecode<=3:
			code=randint(100000,999999)
			phonecode=PhoneConfirmation.objects.create(code=code,phone=phone,active=True)
			#SMSVerif(phone,code)
			return Response({'id':phonecode.id})

class ConfirmationCode(APIView):
	permission_classes=[permissions.AllowAny]
	def post(self,request):
		code=int(request.data.get('code'))
		id=request.data.get('id')
		phonecode=PhoneConfirmation.objects.get(id=id,active=True)
		if phonecode.code==code:
			phonecode.active=False
			phonecode.save()
			return Response({'success':'verification'})

class GetPhoneCode(APIView):
	permission_classes=[permissions.AllowAny]
	def post(self,request):
		id=request.data.get('id')
		phonecode=PhoneConfirmation.objects.get(id=id)
		serializer=PhoneConfirmationSerializer(phonecode)
		return Response(serializer.data)
		

class FinalisationRegistration(APIView):
	permission_classes=[permissions.AllowAny]
	def post(self,request):
		data=request.data
		serializer=UserSerializer(data=data)
		if serializer.is_valid():
			serializer.save(active=False,document_verif=False)
			return Response({'success':'registration'})


#Verification du numero de telephone en cas d oubli du mot de passe
class ResetVerification(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		phone=request.data['phone']
		client=User.objects.get(phone=phone,active=True,document_verif=True,is_staff=False)
		if client is not None:
			code=randint(100000,999999)
			verif=PhoneVerificationCode.objects.create(user=client,code=code,active=True)
			id=verif.id
			SMSVerif(phone,code)
			return Response({'id':id})

#Verification de l activite du code
class VerificationIdReset(APIView):
	permission_classes=[permissions.AllowAny]
	def post(self,request):
		id=request.data.get('id')
		verif=PhoneVerificationCode.objects.get(id=id)
		if verif.active==True:
			return Response(True)
		return Response(False)

#Verification du code
class CodeReset(APIView):
	permission_classes=[permissions.AllowAny]
	def post(self,request):
		id=request.data.get('id')
		code=int(request.data.get('code'))
		verif=PhoneVerificationCode.objects.get(id=id,active=True)
		if verif.code==code:
			return Response({'succes':'confirmation phone'})


#Changement du mot de passe
class ResetPassword(ModelViewSet):
	permission_classes = [permissions.AllowAny]
	queryset = User.objects.filter(active=True)
	serializer_class=UserSerializer
	@action(methods=["put"], detail=False, url_path='reseter')
	def modif_password(self,request,*args,**kwargs):
		data=request.data
		id=data['id']
		verif=PhoneVerificationCode.objects.get(id=id,active=True)
		if verif is not None:
			password=data['password']
			user=verif.user
			user.set_password(password)
			user.save()
			verif.active=False
			verif.save()
			return Response({'message':'donnee bien modifiee'})

	

class Authent(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request):
		if self.request.user.is_authenticated: 
			return Response(True)
		else:
			return Response(False)

#Identifier l utilisateur connecte
class GetUser(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request):
		if request.user.is_authenticated:
			serializer=UserSerializer(request.user)
			return Response(serializer.data)
		return Response(False)
		
#Verification de l existence du beneficiaire lors de l envoi
class VerificationCredentialsEnvoi(APIView):
	def post(self,request):
		envoyeur=request.user
		if envoyeur.active==True and envoyeur.document_verif==True:
			data=request.data
			phone_receveur=data['phone']
			getcontext().prec=10 
			somme=Decimal(data['somme'])
			if somme>0:
				frais=somme/Decimal(100)
				debit=somme+frais
				if phone_receveur!=envoyeur.phone:
					if envoyeur.solde>=debit:
						receveur=User.objects.get(phone=phone_receveur,active=True,document_verif=True)
						trans=VerificationTransaction.objects.create(user=envoyeur,somme=somme,
						commission=frais,phone_destinataire=phone_receveur,nature_transaction="envoi direct",total=debit)
						return Response({'id':trans.id,'nom':receveur.nom,'prenom':receveur.prenom})
						
							#if envoyeur.business==True or receveur.business==True or envoyeur.professionnel==True or receveur.professionnel==True:
'''else:
	trans=VerificationTransaction.objects.create(user=envoyeur,somme=somme,
		commission=frais,phone_destinataire=phone_receveur,nature_transaction="envoi direct",total=debit)
	return Response({'id':trans.id,'nom':receveur.nom,'prenom':receveur.prenom})'''

#Transaction 
class GetRansactionEnvoiDirect(APIView):
	def post(self,request):
		id=request.data.get('id')
		trans=VerificationTransaction.objects.get(id=id,nature_transaction="envoi direct",user=request.user)
		receveur=User.objects.get(phone=trans.phone_destinataire)
		userserial=UserSerializer(receveur)
		transserial=VerificationTransactionSerializer(trans)
		return Response({'receveur':userserial.data,'transaction':transserial.data})

		
#L envoi direct en lui meme			
class EnvoyerDirect(ModelViewSet):
	queryset =VerificationTransaction.objects.all()
	serializer_class=VerificationTransactionSerializer
	@action(methods=["put"], detail=False, url_path='envoyerdirectement')
	def envoi_direct(self,request,*args,**kwargs):
		envoyeur=request.user
		if envoyeur.active==True and envoyeur.document_verif==True:
			id=request.data.get('id')
			admina=User.objects.get(phone='+79649642176')
			employe=Employe.objects.get(user=admina,active=True)
			trans=VerificationTransaction.objects.get(id=id,nature_transaction="envoi direct",user=envoyeur)
			receveur=User.objects.get(phone=trans.phone_destinataire,active=True,document_verif=True)
			if envoyeur.solde>=trans.total:
				envoyeur.solde-=trans.total
				envoyeur.save()
				receveur.solde+=trans.somme
				receveur.save()
				admina.solde+=trans.commission
				admina.save()
				EnvoiDirectNotif(envoyeur,receveur,trans.somme,trans.commission,employe,trans.total)
				env=Envoi.objects.create(envoyeur=envoyeur,phone_receveur=receveur.phone,somme=trans.somme
					,commission=trans.commission,relever=False)
				trans.delete()
				return Response({'id':env.id,'nature':"envoi direct"})

	@action(methods=["put"], detail=False, url_path='annulationenvoi')
	def anunuler_direct(self,request,*args,**kwargs):
		id=request.data.get('id')
		trans=VerificationTransaction.objects.get(id=id,user=request.user)
		trans.delete()
		return Response({'success':'annulation'})

							

#Recu d envoi direct 
class RecuDirect(APIView):
	def post(self,request):
		data=request.data 
		id=data['id']
		envoi=Envoi.objects.get(id=id,envoyeur=request.user)
		receveur=User.objects.get(phone=envoi.phone_receveur)
		receveurserializer=UserSerializer(receveur)
		serializer=EnvoirSerializer(envoi)
		return Response({'envoi':serializer.data,'receveur':receveurserializer.data})



#Verification somme lors de l envoi par code
class VerificationSomme(APIView):
	def post(self,request):
		envoyeur=request.user
		data=request.data
		if envoyeur.active==True and envoyeur.document_verif==True:
			getcontext().prec=10
			somme=Decimal(data['somme'])
			if somme>0:
				frais=somme/Decimal(100)
				debit=somme+frais
				phone_receveur=data['phone']
				nom=data['nom']
				if envoyeur.solde>=debit:
					trans=VerificationTransaction.objects.create(user=envoyeur,somme=somme,
						commission=frais,phone_destinataire=phone_receveur,
						nature_transaction="envoi via code",
						nom_complet_destinataire=nom,total=debit)
					return Response({'id':trans.id,'nom':trans.nom_complet_destinataire})

class GetRansactionCode(APIView):
	def post(self,request):
		id=request.data.get('id')
		trans=VerificationTransaction.objects.get(id=id,nature_transaction="envoi via code",user=request.user)
		serializer=VerificationTransactionSerializer(trans)
		return Response(serializer.data)


#Envoi avec code directement a partir de son compte			
class EnvoiViaCodeDirect(ModelViewSet):
	queryset =VerificationTransaction.objects.all()
	serializer_class=VerificationTransactionSerializer

	@action(methods=["put"], detail=False, url_path='envoyerviacodedirectement')
	def envoi_code(self,request,*args,**kwargs):
		data=request.data
		client=request.user
		if client.active==True and client.document_verif==True:
			id=data['id']
			trans=VerificationTransaction.objects.get(id=id,nature_transaction="envoi via code",user=request.user)
			code=randint(100000000,999999999)
			admina=User.objects.get(phone='+79649642176')
			if client.solde>=trans.total:
				viacod=ViaCode.objects.create(code=code,
					Nom_complet_du_receveur=trans.nom_complet_destinataire ,client=client
					,somme=trans.somme,commission=trans.commission,active=True,retirer=False)
				client.solde-=trans.total
				client.save()
				admina.solde+=trans.commission
				admina.save()
				EnvoiViaCodeNotif(client,trans.somme,
					code,trans.commission,trans.nom_complet_destinataire,admina,trans.total)
				trans.delete()
				return Response({'id':viacod.id,'nature':"envoi via code"})

#Recu envoi par code
class RecuCode(APIView):
	def post(self,request):
		data=request.data
		id=data['id']
		envoicode=ViaCode.objects.get(id=id)
		if request.user==envoicode.client:
			serializer=ViaCodeSerializer(envoicode)
			return Response(serializer.data)

#un recu specifique
class RecuDonne(APIView):
	def post(self,request):
		data=request.data
		id=data['id']
		message=Messages.objects.get(id=id) 
		if request.user==message.user:
			serializer=MessageSerializer(message)
			return Response(serializer.data)
		
		
#les transactions de l utilisateur
class UserMessages(generics.ListAPIView):
	pagination_class =MyPaginationClass
	serializer_class=MessageSerializer

	def get_queryset(self, *args, **kwargs):
		user=self.request.user
		messages=Messages.objects.filter(user=user,is_trans=True).order_by('-id')
		return messages

#Les transactions qui necessitent une notification 
class UserNotif(generics.ListAPIView):
	pagination_class =MyPaginationClass
	serializer_class=MessageSerializer

	def get_queryset(self, *args, **kwargs):
		user=self.request.user
		messages=Messages.objects.filter(user=user,should_notify=True).order_by('-id')
		return messages

#Lecture des notifications
class UserNotifRead(APIView):
	def get(self,request):
		messages=Messages.objects.filter(user=request.user,should_notify=True,lu=False)
		for m in messages:
			m.lu=True
			m.save()
		return Response({'success':'read notif'})	

#Badge de la notification
class UserBadgeNotif(APIView):
	def get(self,request):
		numbernotif=Messages.objects.filter(user=request.user,should_notify=True,lu=False).count()
		return Response({'badge':numbernotif})

		

#filtration transaction
class RechercheMessage(generics.ListAPIView):
	permission_classes = [permissions.AllowAny]
	#queryset = Messages.objects.filter(user=request.user)
	serializer_class = MessageSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = search_fields = ['^message']

	def get_queryset(self):
		user = self.request.user
		return Messages.objects.filter(user=user)
	

#Verification en cas d achat sur gaalguishop
class VerificationPhonePourPayement(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		phone=data['phone']
		somme=Decimal(data['total'])
		client=User.objects.get(phone=phone,active=True,document_verif=True)
		if client is not None and client.solde>=somme:
			code=randint(10000,99999)
			verif=PhoneVerificationCode.objects.create(user=client,code=code,active=True)
			id=verif.id
			#CodePayementEGaalgui(client,code) 
			return Response({'id':id})


#Suppression de code en cas d annulation
class RemoveCode(ModelViewSet):
	permission_classes = [permissions.AllowAny]
	queryset = User.objects.filter(active=True)
	serializer_class=UserSerializer
	@action(methods=["put"], detail=False, url_path='coderemove')
	def remove_code(self,request,*args,**kwargs):
		id=self.request.data.get('id')
		verif=PhoneVerificationCode.objects.get(id=id)
		if verif is not None:
			verif.delete()
			return Response({'suppression':'success'})

#Payement gaalguishop		
class Payementgaalgui(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		code=int(request.data.get('code'))
		id=request.data.get('id')
		verif=PhoneVerificationCode.objects.get(id=id,active=True)
		if verif.code==code:
			phone=request.data.get('phone')
			user=User.objects.get(phone=phone,active=True,document_verif=True)
			getcontext().prec=10
			to=request.data.get('total')
			total=Decimal(to)
			co=request.data.get('commission')
			commission=Decimal(co) # Commission de la plateforme
			li=request.data.get('livraison')
			livraison=Decimal(li)
			if user.solde>=total:
				serializer=PayementGaalguiSerializer(data=data)
				if serializer.is_valid():
					user.solde-=total
					user.save()
					admina=User.objects.get(phone='+79649642176')
					admina.solde+=(livraison+commission)
					admina.save()
					serializer.save(user=user,active=False,total=total,commission=commission,
						livraison=livraison,relever=False)
					pay_id=serializer.data['id']
					pay=PayementGaalgui.objects.get(id=pay_id)
					pay.active=True
					pay.save()
					verif.active=False
					verif.save()
					#NotificationPayement(user,)
					return Response({'payement':'payement succes'})
				return Response(serializer.errors)


#Annulation d une commande GaalguiShop Refaire
class AnnulationCommandeGaalgui(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		phone=data['phone']
		getcontext().prec=10
		montant=Decimal(data['montant'])
		nom=data['nom']
		livraison=Decimal(data['livraison'])
		commission=Decimal(data['commission'])
		client=User.objects.get(phone=phone)
		client.solde+=montant
		client.save()
		admina=User.objects.get(phone='+79649642176')
		admina.solde-=(livraison+commission)
		admina.save()
		AnnulationGaalguiShop.objects.create()
		#AnnulationCommandeGaalguiShopNotif(client,somme,nom)
		return Response({'message':'Annulation a succes'})


#Les dernieres transactions 
class LastMessages(APIView):
	def get(self,request): 
		messages=Messages.objects.filter(user=request.user,is_trans=True).order_by('-id')[:5]
		serializer=MessageSerializer(messages,many=True)
		return Response(serializer.data) 


class GetPub(APIView):
	permission_classes=[permissions.AllowAny]
	def get(self,request):
		pub=TendancePub.objects.filter(active=True).order_by('-id')
		serializer=TendancePubSerializer(pub,many=True)
		return Response(serializer.data)

class GetCodeQr(APIView):
	def post(self,request):
		slug=request.data.get('slug')
		pro=Professionel.objects.get(slug=slug)
		if pro is not None:
			return Response({'id':pro.id})


class GetProfessionnel(APIView):
	def post(self,request):
		id=request.data.get('id')
		pro=Professionel.objects.get(id=id)
		serializer=ProfessionnelSerializer(pro)
		return Response(serializer.data)


class PayementQrCode(APIView):
	def post(self,request):
		data=request.data
		id=data['id']
		pro=Business.objects.get(id=id)
		receveur=pro.user
		user=request.user
		if receveur.active==True and receveur.document_verif==True and user.active==True and user.document_verif==True:
			getcontext().prec=10
			somme=Decimal(data['somme'])
			objet=data['objet']
			payeur=data['payeur']
			commission=0
			total=somme+commission
			if user.solde >= total:
				user.solde-=total
				user.save()
				receveur.solde+=somme
				receveur.save()
				beneficiaire=pro.nom
				pay=Payement.objects.create(user=user,somme=somme,commission=commission,objet=objet,
				business=pro)
				#admina=User.objects.get(phone="+79649642176")
				#admina.solde+=commission
				#admina.save()
				#NotificationAdmina.objects.create(user=admina,somme=commission,nature="payement qrcode")
				qrpayementNotif(user,receveur,somme,commission,payeur,total,beneficiaire)
				return Response({'id':pay.id})


class RecuPayement(APIView):
	def post(self,request):
		id=request.data.get('id')
		pay=Payement.objects.get(id=id)
		if request.user==pay.user:
			serializer=PayementSerializer(pay)
			return Response(serializer.data)


class LierSonCompteGaalguiShop(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		phone=request.data.get('phone')
		user=User.objects.get(phone=phone,active=True,conform_phone=True)
		if user is not None:
			return Response({'success':'user verif'})
		





		
		


		
	
		
	
		







		


	
		



	
		

		



	
		



	
		



		

		

		

