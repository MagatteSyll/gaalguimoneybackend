from django.shortcuts import render
from .serializer import*
from .models import*
from rest_framework.views import APIView
from rest_framework.response import Response
from decimal import*
from user.models import*
from user.notification import NotifGaalguiPay
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from staff.models import*
from staff.notif import gaalguipayNotifStaffSDE
from rest_framework import  permissions






def notify(user,data):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(user.group, {
    'type': 'notify',
    'value': data
    })

class PayementFactureSDE(APIView):
	def post(self,request):
		data=request.data
		getcontext().prec=10
		montant=Decimal(data['montant'])
		if montant>0:
			sde=PayModel.objects.get(alias="SDE")  #alias=" " ,adress="" si on a plusieurs receveurs
			montant=Decimal(data['montant'])
			numero=data['numero']
			nom=data['nom_complet_client']
			professionnel=Professionel.objects.get(paymodel=sde,active=True)
			if request.user.is_staff==True:
				employe=Employe.objects.get(user=request.user,active=True)
				if employe is not None:
					action="Payement de la facture SDE  numero"+ str(numero) +" "+ "montant:" +" "+ str(montant)
					ActionStaff.objects.create(action=action,employe=employe,nature="payement")
					professionnel.user.solde+=montant
					professionnel.user.save()
					message="Payement de la facture numero"+" "+ str(numero)+" "+ ",client:"+ " "+ nom+" "+ "montant:"+" "+ str(montant)+" "+ ",solde actuel:"+" "+ str(professionnel.user.solde)
					payement=PayementProfessionnel.objects.create(message=message,professionnel=professionnel,
						nom_complet_client=nom,montant=montant,employe=employe,relever=False)
					gaalguipayNotifStaffSDE(employe,numero,montant,nom)
					return Response({'id':payement.id,'alias':professionnel.nom})
			else:
				if request.user.solde>=montant:
					professionnel.user.solde+=montant
					professionnel.user.save()
					request.user.solde-=montant
					request.user.save()
					message="Payement de la facture numero"+" "+ str(numero)+" "+ ",client:"+ " "+ nom+" "+ "montant:"+" "+ str(montant)+" "+ ",solde actuel:"+" "+ str(professionnel.user.solde)
					payement=PayementProfessionnel.objects.create(message=message,professionnel=professionnel,
					nom_complet_client=nom,montant=montant,relever=False)
					messageuser="-"+" "+ str(montant) +" "+ ",payement facture "+" "+professionnel.nom+" "+"numero"+" "+numero+" "+ "solde actuel"+" "+str(request.user.solde)
					Messages.objects.create(user=request.user,message=messageuser,nature_transaction='payement',
						should_notify=False,is_trans=True,montant=montant,commission=0,total=montant,)
					#notif(professionnel.user,message)
					return Response({'id':payement.id,'alias':professionnel.nom})



class GetPayement(APIView):
	def post(self,request):
		id=request.data.get('id')
		payement=PayementProfessionnel.objects.get(id=id)
		if request.user.is_staff:
			employe=Employe.objects.get(user=request.user,active=True)
			if employe is not None and payement.employe==employe:
				serializer=PayementProfessionnelSerializer(payement)
				return Response(serializer.data)
		else:
			user=request.user
			if payement.user==user:
				serializer=PayementProfessionnelSerializer(payement)
				return Response(serializer.data)




class GetPayementBusinessUser(APIView):
	def get(self,request):       
		user=request.user
		if user.business==True:
			business=BusinessModel.objects.get(user=user)
			pay=PayementBusiness.objects.filter(business=business,relever=False).order_by("-id")
			serializer=PayementBusinessSerializer(pay,many=True)
			return Response(serializer.data)
		return Response(None)

class GetSinglePayementBusiness(APIView):
	def post(self,request):
		user=request.user
		business=BusinessModel.objects.get(user=user)
		id=request.data.get("id")
		pay=PayementBusiness.objects.get(id=id,business=business)
		serializer=PayementBusinessSerializer(pay)
		return Response(serializer.data)


class ReleverPayementBusiness(APIView):
	def post(self,request):
		user=request.user
		business=BusinessModel.objects.get(user=user)
		id=request.data.get("id")
		pay=PayementBusiness.objects.get(business=business,id=id)
		pay.relever=True
		pay.save()
		return Response({"success":"relever"})


class GetPayementProfessionnelUser(APIView):
	def get(self,request):
		user=request.user
		if user.professionnel==True:
			professionnel=Professionel.objects.get(user=user)
			pay=PayementProfessionnel.objects.filter(professionnel=professionnel,relever=False).order_by("-id")
			serializer=PayementProfessionnelSerializer(pay,many=True)
			return Response(serializer.data)
		return Response(None)


class GetSinglePayementProfessionnel(APIView):
	def post(self,request):
		user=request.user
		professionnel=Professionel.objects.get(user=user)
		id=request.data.get("id")
		pay=PayementProfessionnel.objects.get(id=id,professionnel=professionnel)
		serializer=PayementProfessionnelSerializer(pay)
		return Response(serializer.data)





class ReleverPayementProfessionnel(APIView):
	def post(self,request):
		user=request.user
		professionnel=Professionel.objects.get(user=user)
		id=request.data.get("id")
		pay=PayementProfessionnel.objects.get(professionnel=professionnel,id=id)
		pay.relever=True
		pay.save()
		return Response({"success":"relever"})



class GetQrCode(APIView):
	def get(self,request):
		user=request.user
		if user.business==True:
			business=BusinessModel.objects.get(user=user)
			code=CodeGenerate.objects.get(business=business)
			img=code.code.url
			return Response({"code":img})
		if user.professionnel==True:
			professionnel=Professionel.objects.get(user=user)
			code=CodeGenerateProfessionnel.objects.get(professionnel=professionnel)
			img=code.code.url
			return Response({"code":img})



class GetPayOfficiel(APIView):
	permission_classes=[permissions.AllowAny]
	def get(self,request):
		#tenir compte du pays
		pay=PayModel.objects.filter(active=True).order_by("-id")
		serializer=PayModelSerializer(pay,many=True)
		return Response(serializer.data)
		


class VerifSlugPayementBusiness(APIView):
	def post(self,request):
		data=request.data
		slug=data['slug']
		business=BusinessModel.objects.get(slug=slug,active=True)
		if business is not None and business.user!=request.user:
			return Response({'id':business.id})



class GetBusinessModel(APIView):
	def post(self,request):
		id=request.data.get("id")
		business=BusinessModel.objects.get(id=id,active=True)
		serializer=BusinessModelSerializer(business)
		return Response(serializer.data)


		
					
class QrCodePayementBusiness(APIView):
	def post(self,request):
		data=request.data
		id=data['id']
		business=BusinessModel.objects.get(id=id,active=True)
		if business is not None and business.user!=request.user:
			getcontext().prec=10
			nom=data['nom']
			somme=Decimal(data['somme'])
			commission =0
			total=somme  #+commission
			objet=data["objet"]
			message="vide" 
			if somme>0 and  request.user.solde>=total:
				pay=PayementBusiness.objects.create(nom_complet_client=nom,somme=somme,message=message,
					business=business,total=total,relever=False)
				business.user.solde+=somme
				business.user.save()
				nouveau=objet+" "+ "+"+" "+ str(somme)+ " "+ " solde actuel"+" "+ str(user.solde)
				pay.message=nouveau
				pay.save()
				request.user.solde-=total
				request.user.save()
				messageenvoyeur=objet +" "+ "-" + " " + str(total) +" "+ ",solde actuel "+" "+ str(request.user.solde)
				Messages.objects.create(user=request.user,message=messageenvoyeur,nature_transaction='payement',
    should_notify=False,is_trans=True,montant=somme,commission=commission,total=total,beneficiaire=business.user.nom)
				return Response({'id':pay.id})





class GetPayementQrBusiness(APIView):
	def post(self,request):
		id=request.data.get("id")
		pay=PayementBusiness.objects.get(id=id)
		serializer=PayementBusinessSerializer(pay)
		return Response(serializer.data)







	
		





		
		
		
		








		






				


		
		









