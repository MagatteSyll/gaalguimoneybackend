from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from user.serializer import*
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import  permissions
from random import randint
from datetime import datetime
from user.models import*
from .models import*
from user.notification import depotNotif,RetraitNotif,ActivationClientNotif,qrpayementNotif,notifactivationbusiness
from decimal import*
from .notif import*
#from user.payement import actionperiodique
from rest_framework.viewsets import ModelViewSet 
from rest_framework.decorators import action
from datetime import datetime, timedelta
from django.utils import timezone 
import time, threading
import json
from .serializer import* 
from pay.models import*
from user.serializer import*
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from pay.serializer import*
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from rest_framework.pagination import PageNumberPagination




class MyPaginationClass(PageNumberPagination):
    page_size = 15 
    page_size_query_param = 'page_size'
###1 Envoi via code
#Commission incluse
class CommissionEnvoiCodeInclus(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None:
			monaie=employe.point_acces.pays.monaie_associe
			#if monaie==
			data=request.data
			getcontext().prec=10
			somme=Decimal(data['somme'])
			if somme>0:
				commission=somme/Decimal(100)
				montant=somme-commission 
				commission_envoi=montant/Decimal(100)
				total=montant+commission_envoi
				reste=somme-total
				trans=VerificationTransaction.objects.create(
					nom_complet_destinataire=data['receveur'],nom_complet_client=data['envoyeur'],somme=montant,
					commission=commission_envoi,nature_transaction="envoi via code",
					phone_destinataire=data['phone'],commission_incluse=True,
					reste=reste,employe=employe)
				return Response({'id':trans.id,'nature':trans.nature_transaction})

#Commission non incluse
class CommissionEnvoiCodeNonIncluse(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None:
			data=request.data
			getcontext().prec=10
			somme=Decimal(data['somme'])
			if somme>0:
				commission=somme/Decimal(100)
				total=somme+commission
				trans=VerificationTransaction.objects.create(
					nom_complet_destinataire=data['receveur'],nom_complet_client=data['envoyeur'],somme=somme,
					commission=commission,nature_transaction="envoi via code",
					phone_destinataire=data['phone'],employe=employe,total=total,commission_incluse=False)
				return Response({'id':trans.id,'nature':trans.nature_transaction})

#Recu envoi code
class RecuViaCode(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None:
			data=request.data
			id=data['id']
			viacode=ViaCode.objects.get(id=id,employe=employe)
			serializer=ViaCodeSerializer(viacode)
			return Response(serializer.data)


###Depot
#Verification des donnees du client lors du depot
class GetClientDepot(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None:
			phone=request.data.get('phone')
			client=User.objects.get(phone=phone,active=True,document_verif=True)
			if client is not None:
				getcontext().prec=10
				somme=Decimal(request.data.get('somme'))
				if somme>0:
					devise=employe.point_acces.region.pays.monaie_associe
					deviseclient=client.pays.monaie_associe
					if devise==deviseclient:
						trans=VerificationTransaction.objects.create(user=client,somme=somme,commission=0,
							nature_transaction="depot",employe=employe)
						return Response({'depot':trans.id,'nature':trans.nature_transaction})
					else:
						sommecfa=somme*devise.valeur_CFA
						sommeconverti=sommecfa/deviseclient.valeur_CFA
						trans=VerificationTransaction.objects.create(user=client,somme=sommeconverti,commission=0,
							nature_transaction="depot",employe=employe)
						return Response({'depot':trans.id,'nature':trans.nature_transaction})


#Recu Depot
class RecuDepot(APIView):
	permission_classes = [permissions.IsAdminUser] 
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None:
			data=request.data
			id=data['id']
			depot=Depot.objects.get(id=id,employe=employe)
			serializer=DepotSerializer(depot)
			return Response(serializer.data)

## 3 Retrait simple 
#Identification du client lors du retrait
class GetClientRetrait(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None:
			phone=request.data.get('phone')
			somme=Decimal(request.data.get('somme'))
			client=User.objects.get(phone=phone,active=True,document_verif=True)
			if somme>0 and client.solde>=somme:
				devise=employe.point_acces.region.pays.monaie_associe
				deviseclient=client.pays.monaie_associe
				if devise==deviseclient:
					trans=VerificationTransaction.objects.create(user=client,somme=somme,
						sommecoteclient=somme,
						commission=0,employe=employe,nature_transaction="retrait")
					return Response({'retrait':trans.id,'nature':trans.nature_transaction})
				else:
					sommecfa=somme*devise.valeur_CFA
					sommeconverti=sommecfa/deviseclient.valeur_CFA
					trans=VerificationTransaction.objects.create(user=client,somme=sommeconverti,
						sommecoteclient=somme,
						commission=0,employe=employe,nature_transaction="retrait")
					return Response({'retrait':trans.id,'nature':trans.nature_transaction})


#Recu Retrait
class RecuRetrait(APIView):
	permission_classes = [permissions.IsAdminUser] 
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None:
			data=request.data
			id=data['id']
			retrait=Retrait.objects.get(id=id,employe=employe)
			serializer=RetraitSerializer(retrait)
			return Response(serializer.data)

###4 Retrait avec code
#Verification code lors du retrait
class RetraitViaCode(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None:
			data=request.data
			code=int(data['code'])
			transfert=ViaCode.objects.get(code=code,active=True)
			if transfert is not None:
				trans=VerificationTransaction.objects.create(
					nom_complet_destinataire=transfert.Nom_complet_du_receveur,
					nom_complet_client=transfert.Nom_complet_de_l_envoyeur,somme=transfert.somme,
					commission=0,employe=employe,nature_transaction="retrait par code",code=transfert.code)
				return Response({'id':trans.id,'nature':trans.nature_transaction})


#Recu retrait avec code
class RecuRetraitCode(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		data=request.data
		id=data['id']
		viacode=ViaCode.objects.get(id=id,active=False)
		serializer=ViaCodeSerializer(viacode)
		return Response(serializer.data)

#GetTransaction donnee
class GetRansaction(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None:
			id=request.data.get('id')
			trans=VerificationTransaction.objects.get(id=id,employe=employe)
			serializer=VerificationTransactionSerializer(trans)
			return Response(serializer.data)


class LesTransactions(ModelViewSet):
	permission_classes = [permissions.IsAdminUser]
	queryset=VerificationTransaction.objects.all()
	serializer_class=VerificationTransactionSerializer
	@action(methods=["put"], detail=False, url_path='deposer')
	def depot(self,request,*args,**kwargs):
		id=request.data.get('id')
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None:
			trans=VerificationTransaction.objects.get(id=id,employe=employe)
			if trans is not None:
				user=trans.user
				if user.active==True and user.document_verif==True:
					getcontext().prec=10
					user.solde+=trans.somme 
					user.save()
					dep=Depot.objects.create(depositaire=user,somme=trans.somme,employe=employe,relever=False)
					action='Depot de ' +" "+ str(trans.sommecoteclient) +" "+ "sur le compte numero"+ " "+ str(user.id)
					ActionStaff.objects.create(action=action,employe=employe,nature="depot",montant_rentrant=trans.somme,
						montant_entreprise=0)
					depotNotif(user,trans.somme)
					depotStaffNotif(employe,user,trans.somme)
					trans.delete()
					return Response({'id':dep.id,'nature':"depot"})
	@action(methods=["put"], detail=False, url_path='retirer')
	def retirer(self,request,*args,**kwargs):
		id=request.data.get('id')
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None:
			trans=VerificationTransaction.objects.get(id=id,employe=employe)
			if trans is not None:
				user=trans.user
				if user.active==True and user.document_verif==True:
					getcontext().prec=10
					user.solde-=trans.somme
					user.save()
					retait=Retrait.objects.create(beneficiaire=user,somme=trans.somme,employe=employe,relever=False)
					action='Retrait de ' +" "+ str(trans.somme) +" "+ "sur le compte numero"+ " "+ str(user.id)
					ActionStaff.objects.create(action=action,employe=employe,nature="retrait",montant_rentrant=trans.somme,
						montant_entreprise=0)
					RetraitNotif(user,trans.somme)
					retraitStaffNotif(employe,user,trans.somme)
					trans.delete()
					return Response({'id':retait.id,'nature':"retrait"})

	@action(methods=["put"], detail=False, url_path='retirercode')
	def retirer_code(self,request,*args,**kwargs):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None:
			code=request.data.get('code')
			id=request.data.get('id')
			transfert=ViaCode.objects.get(code=code,active=True,retirer=False)
			trans=VerificationTransaction.objects.get(id=id,employe=employe)
			RetraitCode.objects.create(beneficiaire=trans.nom_complet_destinataire,somme=trans.somme,
				code=trans.code,employe=employe,relever=False)
			transfert.active=False
			trans.retirer=True
			transfert.save()
			action='Retrait par code de  ' +" "+ str(trans.somme) +" "+ "via code "+ " "+ str(trans.code)
			ActionStaff.objects.create(action=action,employe=employe,nature="retrait code",montant_rentrant=trans.somme,
				montant_entreprise=0)
			retraitcodeStaffNotif(employe,trans.nom_complet_destinataire,trans.somme,trans.code)
			trans.delete()
			return Response({"id":transfert.id,"nature":"retrait par code"})

	@action(methods=["put"], detail=False, url_path='envoyerviacode')
	def envoyercode(self,request,*args,**kwargs):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None:
			id=request.data.get('id')
			trans=VerificationTransaction.objects.get(id=id,employe=employe)
			if trans is not None:
				code=randint(100000000,999999999)
				vicode=ViaCode.objects.create(Nom_complet_du_receveur=trans.nom_complet_destinataire
					,Nom_complet_de_l_envoyeur=trans.nom_complet_client,somme=trans.somme,
					employe=employe,phone_beneficiaire=trans.phone_destinataire,commission=trans.commission,
					active=True,code=code,retirer=False)
				action='Envoi via code de  ' +" "+ str(trans.somme) +" "+ "code"+ " "+ str(code)
				getcontext().prec=10
				ActionStaff.objects.create(action=action,employe=employe,nature="envoi code",montant_rentrant=trans.somme,
					montant_entreprise=trans.commission)
				admina=User.objects.get(phone="+79649642176")
				#NotificationAdmina.objects.create(user=admina,somme=trans.commission,nature="envoi via code")
				admina.solde+=trans.commission
				admina.save()
				envoicodeStaffNotif(employe,trans.nom_complet_client,trans.somme,code)
				trans.delete()
				return Response({'id':vicode.id,'nature':"envoi via code"})
	
####Activation d un client 
class VerificationPourActivation(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		phone=request.data.get('phone')
		user=User.objects.get(phone=phone,active=True,document_verif=False)
		if user is not None:
			return Response({'polza':user.id,'prenom':user.prenom,'nom':user.nom})

class GetPolza(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		id=request.data.get('id')
		user=User.objects.get(id=id,active=True,document_verif=False)
		if user is not None:
			serializer=UserSerializer(user)
			return Response(serializer.data)

class ActivationDuClient(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None:
			pays=employe.point_acces.region.pays
			id=request.data.get('id')
			user=User.objects.get(id=id,active=True,document_verif=False)
			nature=request.data.get('nature')
			numero=request.data.get('numero')
			user.nature_document=nature
			user.numero_document=numero
			user.document_verif=True
			user.pays=pays
			user.save()
			action='Activation de l utilisateur numero '+ " "+ str(user.id)
			ActionStaff.objects.create(action=action,employe=employe,nature="activation",montant_rentrant=0,
				montant_entreprise=0)
			QrCodeClient.objects.create(user=user)
			ActivationClientNotif(user)
			activationStaffNotif(employe,user.prenom,user.nom)
			return Response({'success':'activation'})


class GetClientDesactivation(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and employe.user.is_staff_bureau==True:
			phone=request.data.get('phone')
			user=User.objects.get(phone=phone,active=True)
			if user is not None:
				return Response({'polza':user.id,'prenom':user.prenom,'nom':user.nom})

class ConfirmationDesactivation(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and employe.user.is_staff_bureau:
			id=request.data.get('id')
			user=User.objects.get(id=id,active=True)
			serializer=UserSerializer(user)
			return Response(serializer.data)


class DesactivationDuClient(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and employe.user.is_staff_bureau:
			id=request.data.get('id')
			user=User.objects.get(id=id,active=True)
			#user.active=False
			user.document_verif=False
			user.save()
			motif=request.data.get('motif')
			action="desactivation du compte numero"+" "+ str(user.id) +" "+ "pour motif"+ " "+ motif 
			employe=Employe.objects.get(user=request.user,active=True)
			ActionStaff.objects.create(action=action,employe=employe,nature='desactivation',montant_rentrant=0,
				montant_entreprise=0)
			desactivationStaffNotif(employe,user.prenom,user.nom)
			return Response({'success':'desactivation'})
 
class VerifyClientReactivation(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe.user.is_staff_bureau==True:
			phone=request.data.get('phone')
			user=User.objects.get(phone=phone,active=False)
			return Response({'polza':user.id,'prenom':user.prenom,'nom':user.nom})

class GetUserReactivation(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe.user.is_staff_bureau==True:
			id=request.data.get('id')
			user=User.objects.get(id=id,active=False)
			serializer=UserSerializer(user)
			return Response(serializer.data)
		

class ReactivationClient(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe.user.is_staff_bureau==True:
			id=request.data.get('id')
			motif=request.data.get('motif')
			user=User.objects.get(id=id,active=False)
			user.active=True
			user.save()
			ActionStaff.objects.create(action="Reactivation de l utilisateur numero" +" "+  str(user.id)+" "+" pour motif:"+" "+motif,
				employe=employe)
			reactivationCompteNotif(employe,user.prenom,user.nom)
			return Response({'success':'reactivation'})




class VerificationNouvelMembreStaf(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and  employe.user.is_staff_bureau and employe.user.is_staff_manager:
			phone=request.data.get('phone')
			user=User.objects.get(phone=phone,active=True,is_staff=False)
			if user is not None:
				return Response({'polza':user.id,'prenom':user.prenom,'nom':user.nom})

class GetClientNouvelMembreStaf(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and  employe.user.is_staff and employe.user.is_staff_manager:
			id=request.data.get('id')
			user=User.objects.get(id=id,active=True,is_staff=False)
			if user is not None:
				serializer=UserSerializer(user)
				return Response(serializer.data)

class ConfirmationStaff(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and  employe.user.is_staff and employe.user.is_staff_manager_personnel:
			id=request.data.get('id')
			user=User.objects.get(id=id,active=True,is_staff=False)
			point_id=request.data.get('point')
			status=request.data.get('status')
			point_acces=PointAcces.objects.get(id=point_id)
			Employe.objects.create(user=user,point_acces=point_acces,active=True)
			action="Ajout au staff simple de l utilisateur  "+" "+ str(user.id) 
			employe=Employe.objects.get(user=request.user,active=True)
			ActionStaff.objects.create(action=action,employe=employe,nature="nouveau membre staff",montant_rentrant=0,
			montant_entreprise=0)
			user.is_staff=True
			user.save()
			if status=='simple':
				user.is_staff_simple=True
				user.save()
			if status=='bureau':
				user.is_staff_bureau=True
				user.save()
			if status=='comptable':
				user.is_staff_comptable=True
				user.save()
			if status=='manager':
				user.is_staff_manager=True
				user.save()
			if status=='technique':
				user.is_staff_techique=True
				user.save()
			return Response({'success':'ajout staff'})




#Dernieres operations staff a corriger
class LastMessageStaf(APIView):
	def get(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		messages=NotificationStaff.objects.filter(employe=employe).order_by('-id')[:5]
		serializer=NotificationStaffSerializer(messages,many=True)
		return Response(serializer.data)

#Historique des transactions du personnel
class NotifStaff(generics.ListAPIView):
	permission_classes = [permissions.IsAdminUser]
	serializer_class = NotificationStaffSerializer
	pagination_class =MyPaginationClass
	def get_queryset(self):
		user = self.request.user
		employe=Employe.objects.get(user=user,active=True)
		notif=NotificationStaff.objects.filter(employe=employe).order_by('-id')
		return notif
		

#Les adresses de point d acces 
class Adressage(APIView):
	def get(self,request):
		adress=Region.objects.all()
		serializer=RegionSerializer(adress,many=True)
		return Response(serializer.data)
			

class AjoutNewPub(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and  employe.user.is_staff_bureau==True:
			data=request.data
			serializer=TendancePubSerializer(data=data)
			if serializer.is_valid():
				serializer.save(active=True)
				action="Ajout d une nouvelle publicite "
				employe=Employe.objects.get(user=request.user,active=True)
				ActionStaff.objects.create(action=action,employe=employe,nature="ajout de publicite")
				return Response({'success':'pub'})
			return Response(serializer.errors)

'''
class CreateBusiness(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and employe.user.is_staff_bureau:
			data=request.data
			serializer=BusinessModelSerializer(data=data)
			if serializer.is_valid():
				schedule, created = IntervalSchedule.objects.get_or_create(every=2, period=IntervalSchedule.MINUTES,)
				start=timezone.now()
				region_id=data['region']
				adress=Region.objects.get(id=region_id)
				phone=data['phone']
				user=User.objects.get(phone=phone,active=True,document_verif=True,)
				name= 'renouvellement du compte business de '+ " " + user.prenom + str(user.id) 
				somme=12000
				task=PeriodicTask.objects.create(interval=schedule, name=name,task='user.views.payement',
					args=json.dumps((user.id,somme,name)),start_time=start)
				serializer.save(user=user,adress=adress,task_number=task.id)
				user.business=True
				user.save()
				busi=BusinessModel.objects.get(id=serializer.data['id'])
				admina=User.objects.get(phone="+79649642176")
				admina.solde+=12000
				admina.save()
				action="Creation du compte professionnel"+" "+ busi.nom + " "+ "numero"+" "+ str(busi.id)
				employe=Employe.objects.get(user=request.user,active=True)
				ActionStaff.objects.create(action=action,employe=employe,nature="creation de compte business",montant_rentrant=12000,
					montant_entreprise=12000)
				nom=busi.slug
				code=CodeGenerate.objects.create(business=busi)
				comptebusineesStaffNotif(employe,busi.nom)
				notifactivationbusiness(user)
				return Response({'id':code.id,'nom':nom})
		#return Response(serializer.errors)


class GetQrCode(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):

		data=request.data
		id=data['id']
		code=CodeGenerate.objects.get(id=id)
		img=code.code.url
		#serializer=CodeGenerateSerializer
		return Response({'file':img})

class VerificationSuspensionBusiness(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and  employe.user.is_staff_bureau==True:
			phone=request.data.get('phone')
			user=User.objects.get(phone=phone)
			business=BusinessModel.objects.get(user=user)
			return Response({'id':business.id,'prenom':user.prenom,'nom':user.nom})

class GetBusinessUser(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and request.user.is_staff_bureau==True:
			id=request.data.get('id')
			business=BusinessModel.objects.get(id=id)
			serializer=BusinessModelSerializer(business)
			return Response(serializer.data)




class SuspensionBusiness(ModelViewSet):
	permission_classes = [permissions.IsAdminUser]
	queryset=BusinessModel.objects.all()
	serializer_class=BusinessModelSerializer

	@action(methods=["put"], detail=False, url_path='suspension')
	def suspendre(self,request,*args,**kwargs):
		employe=Employe.objects.get(user=request.user,active=True)
		if  employe is not None and employe.user.is_staff_bureau==True:
			id=request.data.get('id')
			business=BusinessModel.objects.get(id=id)
			task=PeriodicTask.objects.get(id=business.task_number)
			user=business.user
			user.business=False
			user.save()
			action="Suspension du compte business "+" "+ business.nom + " "+ "numero"+" "+ str(business.id)
			ActionStaff.objects.create(action=action,employe=employe)
			notifdesactivationbusiness(user)
			suspensionbusinessStaffNotif(employe,business.nom)
			task.delete()
			business.delete()
			return Response({'success':'suspension'})



class CreateProfesionnel(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and  employe.user.is_admin==True:
			data=request.data
			serializer=ProfessionnelSerializer(data=data)
			if serializer.is_valid():
				schedule, created = IntervalSchedule.objects.get_or_create(every=2, period=IntervalSchedule.MINUTES,)
				start=timezone.now()
				region_id=data['region']
				adress=Region.objects.get(id=region_id)
				phone=data['phone']
				user=User.objects.get(phone=phone,active=True,document_verif=True,)
				somme=30000
				name= 'renouvellement du compte professionnel de '+ " " + user.prenom + str(user.id) 
				task=PeriodicTask.objects.create(interval=schedule, name=name,task='user.views.payementprofessionnel',
					args=json.dumps((user.id,somme,name)),start_time=start)
				serializer.save(user=user,adress=adress,active=False,task_number=task.id)
				user.professionnel=True
				user.save()
				logo=data['logo']
				professionnel=Professionel.objects.get(id=serializer.data['id'])
				#pay=PayModel.objects.create(professionnel=professionnel,adress=adress,active=False)
				qr=CodeGenerateProfessionnel.objects.create(professionnel=professionnel)
				admina=User.objects.get(phone="+79649642176")
				admina.solde+=130000
				ActionStaff.objects.create(action=action,employe=employe,nature="creation de compte professionnel",montant_rentrant=130000,
					montant_entreprise=130000)
				creationcompteprofessionnelStaffNotif(employe,professionnel.nom)
				return Response({'id':qr.id,'alias':professionnel.nom})
			#return Response(serializer.errors)

class GetQrCodeProfessionnel(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and employe.user.is_admin:
			data=request.data
			id=data['id']
			code=CodeGenerateProfessionnel.objects.get(id=id)
			img=code.code.url
			return Response({'file':img})

class VerificationSuspensionProfessionnel(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and employe.user.is_admin==True:
			phone=request.data.get('phone')
			user=User.objects.get(phone=phone)
			professionnel=Professionel.objects.get(user=user)
			return Response({'id':professionnel.id,'alias':professionnel.nom})

class GetProfessionnelPay(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and  employe.user.is_admin==True:
			id=request.data.get('id')
			professionnel=Professionel.objects.get(id=id)
			serializer=ProfessionnelSerializer(professionnel)
			return Response(serializer.data)


class SuspensionProfesionnel(ModelViewSet):
	permission_classes = [permissions.IsAdminUser]
	queryset=Professionel.objects.all()
	serializer_class=ProfessionnelSerializer

	@action(methods=["put"], detail=False, url_path='suspension')
	def suspendre(self,request,*args,**kwargs):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and request.user.is_admin==True:
			id=request.data.get('id')
			professionnel=Professionel.objects.get(id=id)
			task=PeriodicTask.objects.get(id=professionnel.task_number)
			user=professionnel.user
			user.professionnel=False
			suspensioncompteprofessionnelStaffNotif(employe,professionnel.nom)
			user.save()
			task.delete()
			professionnel.delete()
			return Response({'success':'suspension professionnel'})
'''



#Obtenir les points qui sont dans la meme ville??
class GetPointAcces(APIView):
	permission_classes=[permissions.IsAdminUser]
	def get(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None:
			loc=PointAcces.objects.all()
			serializer=PointAccesSerializer(loc,many=True)
			return Response(serializer.data)

#Region selon le pays
class GetRegion(APIView):
	permission_classes=[permissions.IsAdminUser]
	def get(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None:
			loc=Region.objects.all()
			serializer=RegionSerializer(loc,many=True)
			return Response(serializer.data)

	
#A revoir
'''
class GetPublicPay(APIView):
	permission_classes=[permissions.IsAdminUser]
	def get(self,request):
		#filtre a travers la location
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None :
			pay=PayModel.objects.filter(active=True)
			serializer=PayModelSerializer(pay,many=True)
			return Response(serializer.data)
'''

###Comptabilite

class GetLesDepots(generics.ListAPIView):
	permission_classes=[permissions.IsAdminUser]
	serializer_class = DepotSerializer
	pagination_class =MyPaginationClass

	def get_queryset(self):
		user = self.request.user
		employe=Employe.objects.get(user=user,active=True)
		if employe.user.is_staff_comptable:
			lesdepots=Depot.objects.filter(relever=False).order_by('-id')
			return lesdepots

class ReleverDepot(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if  employe.user.is_staff_comptable:
			id=request.data.get('id')
			depot=Depot.objects.get(id=id)
			depot.relever=True
			depot.save()
			return Response({'success':'relever'})

class GetLesRetraits(generics.ListAPIView):
	permission_classes=[permissions.IsAdminUser]
	serializer_class = RetraitSerializer
	pagination_class =MyPaginationClass

	def get_queryset(self):
		user = self.request.user
		employe=Employe.objects.get(user=user,active=True)
		if employe.user.is_staff_comptable:
			lesretrait=Retrait.objects.filter(relever=False).order_by('-id')
			return lesretrait


class ReleverRetrait(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe.user.is_staff_comptable:
			id=request.data.get('id')
			retrait=Retrait.objects.get(id=id)
			retrait.relever=True
			retrait.save()
			return Response({'success':'relever'})

class GetLesRetraitCode(generics.ListAPIView):
	permission_classes=[permissions.IsAdminUser]
	serializer_class = RetraitCodeSerializer
	pagination_class =MyPaginationClass

	def get_queryset(self):
		user = self.request.user
		employe=Employe.objects.get(user=user,active=True)
		if employe.user.is_staff_comptable:
			lesretraitcode=RetraitCode.objects.filter(relever=False).order_by('-id')
			return lesretraitcode

class ReleveRetraitCode(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe.user.is_staff_comptable:
			id=request.data.get('id')
			retraitcode=RetraitCode.objects.get(id=id)
			retraitcode.relever=True
			retraitcode.save()
			return Response({'success':'relever'})


class GetEnvoiCode(generics.ListAPIView):
	permission_classes=[permissions.IsAdminUser]
	serializer_class = ViaCodeSerializer
	pagination_class =MyPaginationClass

	def get_queryset(self):
		user = self.request.user
		employe=Employe.objects.get(user=user,active=True)
		if employe.user.is_staff_comptable:
			lesenvoiscode=ViaCode.objects.filter(relever=False).order_by('-id')
			return lesenvoiscode
	

class ReleveEnvoiCode(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe.user.is_staff_comptable:
			id=request.data.get('id')
			envoicode=ViaCode.objects.get(id=id)
			envoicode.relever=True
			envoicode.save()
			return Response({'success':'relever'})

class GetLesEnvoi(generics.ListAPIView):
	permission_classes=[permissions.IsAdminUser]
	serializer_class = EnvoirSerializer
	pagination_class =MyPaginationClass

	def get_queryset(self):
		user = self.request.user
		employe=Employe.objects.get(user=user,active=True)
		if employe.user.is_staff_comptable:
			lesenvois=Envoi.objects.filter(relever=False).order_by('-id')
			return lesenvois
	


class ReleveEnvoi(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe.user.is_staff_comptable:
			id=request.data.get('id')
			envoi=Envoi.objects.get(id=id)
			envoi.relever=True
			envoi.save()
			return Response({'success':'relever'})

#Relever des payements professionnels
'''class GetLesPayements(APIView):
	permission_classes=[permissions.IsAdminUser]
	serializer_class = PayementProfessionnelSerializer
	pagination_class =MyPaginationClass

	def get_queryset(self):
		user = self.request.user
		employe=Employe.objects.get(user=user,active=True)
		if employe.user.is_staff_comptable:
			lespayements=PayementProfessionnel.objects.filter(relever=False).order_by('-id')
			return lespayements
	


class RelevePayement(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe.user.is_staff_comptable:
			id=request.data.get('id')
			payement=PayementProfessionnel.objects.get(id=id)
			payement.relever=True
			payement.save()
			return Response({'success':'relever'})'''


class GetLesPayementsGaalguiShop(generics.ListAPIView):
	permission_classes=[permissions.IsAdminUser]
	serializer_class = PayementGaalguiSerializer
	pagination_class =MyPaginationClass

	def get_queryset(self):
		user = self.request.user
		employe=Employe.objects.get(user=user,active=True)
		if employe.user.is_staff_comptable:
			lespayementsegaalgui=PayementGaalgui.objects.filter(relever=False).order_by('-id')
			return lespayementsegaalgui

class RelevePayementGaalguiShop(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe.user.is_staff_comptable:
			id=request.data.get('id')
			payementeshop=PayementGaalgui.objects.get(id=id)
			payementeshop.relever=True
			payementeshop.save()
			return Response({'success':'relever'})


class AnnulationGaalguiShop(generics.ListAPIView):
	permission_classes=[permissions.IsAdminUser]
	serializer_class = AnnulationGaalguiShopSerializer
	pagination_class =MyPaginationClass

	def get_queryset(self):
		user = self.request.user
		employe=Employe.objects.get(user=user,active=True)
		if employe.user.is_staff_comptable:
			lesannulationegaalgui=AnnulationGaalguiShop.objects.filter(relever=False).order_by('-id')
			return lesannulationegaalgui

class ReleveAnnulationGaalguiShop(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe.user.is_staff_comptable:
			id=request.data.get('id')
			annulationeshop=AnnulationGaalguiShop.objects.get(id=id)
			annulationeshop.relever=True
			annulationeshop.save()
			return Response({'success':'relever'})

#En rapport avec les comptes professionnels
'''
class GetPayementPeriodic(APIView):
	permission_classes=[permissions.IsAdminUser]
	def get(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and employe.user.is_staff_comptable:
			lesperiodic=PayementPeriodic.objects.filter(relever=False).order_by('-id')
			serializer=PayementPeriodicSerializer(lesperiodic,many=True)
			return Response(serializer.data)


class RelevePayementPeriodic(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and employe.user.is_staff_comptable:
			id=request.data.get('id')
			period=PayementPeriodic.objects.get(id=id)
			period.relever=True
			period.save()
			return Response({'success':'relever'})



class GetSuspensionPeriodic(APIView):
	permission_classes=[permissions.IsAdminUser]
	def get(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and employe.user.is_staff_comptable:
			lesperiodic=SuspensionPayementPeriodic.objects.filter(relever=False).order_by("-id")
			serializer=SuspensionPayementPeriodicSerializer(lesperiodic,many=True)
			return Response(serializer.data)


class ReleveSuspensionPayementPeriodic(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		employe=Employe.objects.get(user=request.user,active=True)
		if employe is not None and employe.user.is_staff_comptable:
			id=request.data.get('id')
			period=SuspensionPayementPeriodic.objects.get(id=id)
			period.relever=True
			period.save()
			return Response({'success':'relever'})'''

class VerificationDepotService(APIView):
	def post(self,request):
		user=request.user
		if user.business:
			service=Service.objects.get(user=user,active=True)
			phone=request.data.get('phone')
			client=User.objects.get(phone=phone,active=True,document_verif=True)
			if client is not None:
				getcontext().prec=10
				somme=Decimal(request.data.get('somme'))
				if somme>0 and somme<=1000000 and user.solde>=somme and client!=user:
					if user.pays.monaie_associe==client.pays.monaie_associe:
						trans=VerificationTransaction.objects.create(user=client,somme=somme,commission=0,
							nature_transaction="depot",service=service,sommecoteclient=somme)
						return Response({'depot':trans.id,'nature':trans.nature_transaction})
					else:
						sommecfa=somme*user.pays.monaie_associe.valeur_CFA
						sommeconverti=sommecfa/client.pays.monaie_associe.valeur_CFA
						trans=VerificationTransaction.objects.create(user=client,somme=somme,commission=0,
							nature_transaction="depot",service=service,sommecoteclient=sommeconverti)
						return Response({'depot':trans.id,'nature':trans.nature_transaction})






## 3 Retrait simple 
#Identification du client lors du retrait
class VerificatioRetraitService(APIView):
	def post(self,request):
		user=request.user
		if user.business:
			service=Service.objects.get(user=user,active=True)
			if service is not None:
				phone=request.data.get('phone')
				somme=Decimal(request.data.get('somme'))
				if somme>0 and somme<1000000:
					client=User.objects.get(phone=phone,active=True,document_verif=True)
					if client.solde>=somme:
						trans=VerificationTransaction.objects.create(user=client,somme=somme,
						commission=0,service=service,nature_transaction="retrait")
						return Response({'retrait':trans.id,'nature':trans.nature_transaction})

#Verification code lors du retrait
class VerificationRetraitViaCodeService(APIView):
	def post(self,request):
		user=request.user
		if user.business:
			service=Service.objects.get(user=user,active=True)
			if service is not None:
				data=request.data
				code=int(data['code'])
				transfert=ViaCode.objects.get(code=code,active=True)
				if transfert is not None:
					trans=VerificationTransaction.objects.create(
						nom_complet_destinataire=transfert.Nom_complet_du_receveur,
						nom_complet_client=transfert.Nom_complet_de_l_envoyeur,somme=transfert.somme,
						commission=0,employe=employe,nature_transaction="retrait par code",code=transfert.code)
					return Response({'id':trans.id,'nature':trans.nature_transaction})

class VerificationEnvoiCodeService(APIView):
	def post(self,request):
		user=request.user
		service=Service.objects.get(user=request.user,active=True)
		if service is not None:
			data=request.data
			getcontext().prec=10
			somme=Decimal(data['somme'])
			nature=data['nature']
			if somme>0:
				if nature=="inclus":
					commission=somme/Decimal(100)
					montant=somme-commission 
					commission_envoi=montant/Decimal(100)
					total=montant+commission_envoi
					reste=somme-total
					if user.solde>=total and total<=1000000:
						trans=VerificationTransaction.objects.create(
							nom_complet_destinataire=data['receveur'],nom_complet_client=data['envoyeur'],somme=montant,
							commission=commission_envoi,nature_transaction="envoi via code",
							phone_destinataire=data['phone'],commission_incluse=True,
							reste=reste,service=service)
						return Response({'id':trans.id,'nature':trans.nature_transaction})
				if nature=="non inclus":
					commission=somme/Decimal(100)
					total=commission+somme
					if user.solde>=total and total<=1000000:
						trans=VerificationTransaction.objects.create(
							nom_complet_destinataire=data['receveur'],nom_complet_client=data['envoyeur'],
							somme=somme,
							commission=commission,nature_transaction="envoi via code",
							phone_destinataire=data['phone'],commission_incluse=False,
							reste=0,service=service)
						return Response({'id':trans.id,'nature':trans.nature_transaction})


#Envoi direct via service
class VerificationEnvoiCompteServiceEnvoi(APIView):
	def post(self,request):
		user=request.user
		if user.business:
			service=Service.objects.get(user=user,active=True)
			if service is not None:
				data=request.data
				getcontext().prec=10
				somme=Decimal(data['somme'])
				phone=data['phone']
				client=User.objects.get(phone=phone,active=True,document_verif=True)
				if nature=="inclus":
					commission=somme/Decimal(100)
					montant=somme-commission 
					commission_envoi=montant/Decimal(100)
					total=montant+commission_envoi
					reste=somme-total
					if user.solde>=total and total<=1000000:
						trans=VerificationTransaction.objects.create(
							user=client,somme=montant,commission=commission_envoi,
							nature_transaction="envoi direct",reste=reste,service=service)
					return Response({'id':trans.id,'nature':trans.nature_transaction})
				if nature=="non inclus":
					commission=somme/Decimal(100)
					total=commission+somme
					if user.solde>=total and total<=1000000:
						trans=VerificationTransaction.objects.create(
							user=client,somme=montant,commission=commission_envoi,
							nature_transaction="envoi direct",reste=reste,service=service)
						return Response({'id':trans.id,'nature':trans.nature_transaction})




class GetTransactionService(APIView):
	def post(self,request):
		user=request.user
		if user.business:
			service=Service.objects.get(user=user,active=True)
			id=request.data.get('id')
			trans=VerificationTransaction.objects.get(id=id,service=service)
			serializer=VerificationTransactionSerializer(trans)
			return Response(serializer.data)


class LesTransactionsService(ModelViewSet):
	queryset=VerificationTransaction.objects.all()
	serializer_class=VerificationTransactionSerializer
	@action(methods=["put"], detail=False, url_path='depotservice')
	def depot(self,request,*args,**kwargs):
		id=request.data.get('id')
		user=request.user
		if user.business:
			service=Service.objects.get(user=user,active=True)
			if service is not None:
				trans=VerificationTransaction.objects.get(id=id,service=service)
				if trans is not None:
					client=trans.user
					if client.active==True and client.document_verif==True and client!=user:
						getcontext().prec=10
						client.solde+=trans.sommecoteclient
						client.save()
						user.solde-=trans.somme
						user.save()
						gain=trans.somme*(5/1000)
						total=gain+trans.somme
						#user.solde+=gain
						#user.save()
						TransactionService.objects.create(service=service,gain=gain,total=total,
							montant=trans.somme,nature="Depot",active=True,relever=False)
						dep=Depot.objects.create(depositaire=client,somme=trans.somme,service=service,
							relever=False)
						depotNotif(client,trans.somme)
						depotBusinessNotif(employe,user,trans.somme)
						trans.delete()
						return Response({'id':dep.id,'nature':"depot"})

	@action(methods=["put"], detail=False, url_path='retraitsimple')
	def retirer(self,request,*args,**kwargs):
		id=request.data.get('id')
		user=request.user
		if user.business:
			service=Service.objects.get(user=user,active=True)
			if service is not None:
				trans=VerificationTransaction.objects.get(id=id,service=service)
				if trans is not None:
					client=trans.user
					if client.active==True and client.document_verif==True and client!=user:
						getcontext().prec=10
						client.solde+=trans.somme
						client.save()
						gain=trans.somme*(5/1000)
						total=gain+trans.somme
						user.solde+=gain
						user.save()
						TransactionService.objects.create(service=service,gain=gain,total=total,
							montant=trans.somme,nature="retrait",active=True,relever=False)
						retait=Retrait.objects.create(beneficiaire=client,somme=trans.somme,
						service=service,relever=False)
						RetraitNotif(client,trans.somme)
						retraitBusinessNotif(service,client,trans.somme)
						trans.delete()
						return Response({'id':retait.id,'nature':"retrait"})

	@action(methods=["put"], detail=False, url_path='retraitcode')
	def retirer_code(self,request,*args,**kwargs):
		user=request.user
		if user.business:
			service=Service.objects.get(user=user,active=True)
			if service is not None:
				code=request.data.get('code')
				id=request.data.get('id')
				transfert=ViaCode.objects.get(code=code,active=True,retirer=False)
				trans=VerificationTransaction.objects.get(id=id,service=service)
				RetraitCode.objects.create(beneficiaire=trans.nom_complet_destinataire,somme=trans.somme,
				code=trans.code,service=service,relever=False)
				user.solde+=trans.somme
				user.save()
				gain=trans.somme*(5/1000)
				total=gain+trans.somme
				user.solde+=gain
				user.save()
				TransactionService.objects.create(service=service,gain=gain,total=total,
					montant=trans.somme,nature="retrait par code",active=True,relever=False)
				transfert.active=False
				trans.retirer=True
				transfert.save()
				retraitcodeBusinessNotif(service,trans.nom_complet_destinataire,trans.somme,trans.code)
				trans.delete()
				return Response({"id":transfert.id,"nature":"retrait par code"})

	@action(methods=["put"], detail=False, url_path='envoyerviacode')
	def envoyercode(self,request,*args,**kwargs):
		user=request.user
		if user.business:
			service=Service.objects.get(user=user,active=True)
			if service is not None:
				id=request.data.get('id')
				trans=VerificationTransaction.objects.get(id=id,service=service)
				if trans is not None:
					code=randint(100000000,999999999)
					vicode=ViaCode.objects.create(Nom_complet_du_receveur=trans.nom_complet_destinataire
					,Nom_complet_de_l_envoyeur=trans.nom_complet_client,somme=trans.somme,
					service=service,phone_beneficiaire=trans.phone_destinataire,commission=trans.commission,
					active=True,code=code,retirer=False)
					getcontext().prec=10
					admina=User.objects.get(phone="+79649642176")
					admina.solde+=trans.commission
					admina.save()
					user.solde-=trans.somme
					user.save()
					gain=trans.somme*(5/1000)
					total=gain+trans.total
					user.solde+=gain
					user.save()
					TransactionService.objects.create(service=service,gain=gain,total=total,
						montant=trans.somme,nature="envoi via code",active=True,relever=False)
					envoicodeBusinessNotif(service,trans.nom_complet_client,trans.somme,code)
					trans.delete()
					return Response({'id':vicode.id,'nature':"envoi via code"})

	@action(methods=["put"], detail=False, url_path='envoicompteclient')
	def envoiclient(self,request,*args,**kwargs):
		user=request.user
		if user.business:
			service=Service.objects.get(user=user,active=True)
			if service is not None:
				id=request.data.get('id')
				trans=VerificationTransaction.objects.get(id=id,service=service)
				if trans is not None:
					client=trans.user
					client.solde+=trans.somme
					client.save()
					user.solde-=trans.somme
					user.save()
					gain=trans.somme*(5/1000)
					total=gain+trans.total
					user.solde+=gain
					user.save()
					TransactionService.objects.create(service=service,gain=gain,total=total,
					montant=trans.somme,nature="envoi direct",active=True,relever=False)
					getcontext().prec=10
					admina=User.objects.get(phone="+79649642176")
					admina.solde+=trans.commission
					admina.save()
					envoicodeBusinessNotif(service,trans.nom_complet_client,trans.somme,code)
					trans.delete()
					return Response({'id':vicode.id,'nature':"envoi direct"})

	@action(methods=["put"], detail=False, url_path='annulationtransaction')
	def anunuler_transaction(self,request,*args,**kwargs):
		id=request.data.get('id')
		service=Service.objects.get(user=request.user,active=True)
		trans=VerificationTransaction.objects.get(id=id,service=service)
		trans.delete()
		return Response({'success':'annulation'})
		























	








		
	
		

	





