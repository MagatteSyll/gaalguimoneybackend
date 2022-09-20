from .models import*
import json
#from channels.layers import get_channel_layer
#from asgiref.sync import async_to_sync





def depotStaffNotif(employe,client,somme):
	notifcation="Depot de " +" " + str(somme) + " " +" CFA par " + " " + client.prenom + " " + client.nom 
	NotificationStaff.objects.create(employe=employe,notification=notifcation) 

def depotBusinessNotif(service,client,somme):
	notifcation="Depot de " +" " + str(somme) + " " +" CFA par " + " " + client.prenom + " " + client.nom 
	NotificationService.objects.create(service=service,notification=notifcation) 


def retraitStaffNotif(employe,client,somme):
	notifcation="retrait de " +" " + str(somme) + " " +" CFA par "+ " " +  client.prenom + " " + client.nom 
	NotificationStaff.objects.create(employe=employe,notification=notifcation) 

def retraitBusinessNotif(service,client,somme):
	notifcation="retrait de " +" " + str(somme) + " " +" CFA par "+ " " +  client.prenom + " " + client.nom 
	NotificationService.objects.create(service=service,notification=notifcation) 

def retraitcodeStaffNotif(employe,receveur,somme,code):
	notifcation="retrait par code de  " +" " + str(somme) + " " +" CFA par " + " " + receveur +" "+ ",code:"+" "+str(code)
	NotificationStaff.objects.create(employe=employe,notification=notifcation) 

def retraitcodeBusinessNotif(service,receveur,somme,code):
	notifcation="retrait par code de  " +" " + str(somme) + " " +" CFA par " + " " + receveur +" "+ ",code:"+" "+str(code)
	NotificationService.objects.create(service=service,notification=notifcation) 

def envoicodeStaffNotif(employe,envoyeur,somme,code):
	notifcation="envoi via code:" +" " + str(code) + " "+"de" + " " + str(somme) + " " +" CFA par " + " "+ envoyeur
	NotificationStaff.objects.create(employe=employe,notification=notifcation) 

def envoicodeBusinessNotif(service,envoyeur,somme,code):
	notifcation="envoi via code:" +" " + str(code) + " "+"de" + " " + str(somme) + " " +" CFA par " + " "+ envoyeur
	NotificationService.objects.create(service=service,notification=notifcation) 


def comptebusineesStaffNotif(employe,nom):
	notifcation="Creation du compte business de " +" " + nom 
	NotificationStaff.objects.create(employe=employe,notification=notifcation) 

def activationStaffNotif(employe,prenom,nom):
	notifcation="Activation du compte de " +" " +prenom + " " + nom
	NotificationStaff.objects.create(employe=employe,notification=notifcation) 

def desactivationStaffNotif(employe,prenom,nom):
	notifcation="Desacivation du compte  " +" " +prenom + " " + nom
	NotificationStaff.objects.create(employe=employe,notification=notifcation) 

def reactivationCompteNotif(employe,prenom,nom):
	notifcation="Réactivation du compte  " +" " +prenom + " " + nom
	NotificationStaff.objects.create(employe=employe,notification=notifcation) 

def ajoutpubStaffNotif(employe,description):
	notifcation="Ajout d image publicitaire " +" " + description
	NotificationStaff.objects.create(employe=employe,notification=notifcation) 

def suspensionbusinessStaffNotif(employe,nom):
	notifcation="Suspension du compte business " +" " + nom 
	NotificationStaff.objects.create(employe=employe,notification=notifcation) 

def creationcompteprofessionnelStaffNotif(employe,alias):
	notifcation="Creation du compte professionnel de " +" " +alias 
	NotificationStaff.objects.create(employe=employe,notification=notifcation) 

def suspensioncompteprofessionnelStaffNotif(employe,alias):
	notifcation="Suspension du compte professionnel de " +" " +alias 
	NotificationStaff.objects.create(employe=employe,notification=notifcation) 

def gaalguipayNotifStaffSDE(employe,numero,montant,client):
	notifcation="Payement de la facture SDE  numero" +" " +str(numero) +" "+ ",client:"+" "+ client +" "+ ",montant:"+" "+ str(montant)
	NotificationStaff.objects.create(employe=employe,notification=notifcation) 




	




	
	