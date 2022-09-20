from .models import Messages
from staff.models import NotificationAdmina
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import decimal
from pay.models import*
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message



def notif(user,title,body):
    devices = FCMDevice.objects.filter(user=user)
    for device in devices:
        device.send_message(Message(data={"titre": title,"body":body}))
#Pay
def notifpayement(client,somme):
    message=' Retrait'+" "+ str(somme)+ " " +' CFA pour le renouvellevement de votre compte professionnel ,solde actuel:'+ str(decimal.Decimal(client.solde))
    Messages.objects.create(user=client,message=message,nature_transaction='payement',should_notify=True)
    

def notifactivationbusiness(client):
    message=' Votre compte business a ete active avec succes'
    Messages.objects.create(user=client,message=message,nature_transaction="activation compte",should_notify=True,is_trans=False)
   

def notifdesactivationbusiness(client):
    message=' Votre compte business a ete desactive avec succes'
    Messages.objects.create(user=client,message=message,nature_transaction="activation compte",should_notify=True,is_trans=False)
    


def qrpayementNotif(envoyeur,receveur,somme,commission,payeur,objet,total,beneficiaire):
    messagereceveur=objet +" "+ "+" + " " + somme +" "+ ",solde "+" "+ str(decimal.Decimal(receveur.solde))
    messageenvoyeur=objet +" "+ "-" + " " + somme +" "+ ",solde "+" "+ str(decimal.Decimal(envoyeur.solde))
    business=BusinessModel.objects.get(user=receveur)
    total=commission+somme
    Messages.objects.create(user=envoyeur,message=messageenvoyeur,nature_transaction='payement',
    should_notify=False,is_trans=True,montant=somme,commission=commission,total=total,beneficiaire=beneficiaire)
    PayementBusiness.objects.create(message=message,business=business,somme=somme,commission=commission,
    total=total,relever=False)
    #notif(receveur,message)

    
def depotNotif(depositaire,somme):
    message="Depot de " + " " +  str(somme) + " " + " francs ,solde actuel:" + " " + str(decimal.Decimal(depositaire.solde))+" "+"CFA"
    Messages.objects.create(user=depositaire,message=message,nature_transaction='depot',
        montant=somme,should_notify=True,is_trans=True)
    notif(depositaire,"Depot GaalguiMoney",message)


def RetraitNotif(beneficiaire,somme):
    message=" Retrait  de " + " " + str(somme) +" " + " francs,solde actuel:"+ " " + str(decimal.Decimal(beneficiaire.solde))+" "+"CFA"
    Messages.objects.create(user=beneficiaire,message=message,nature_transaction='retrait',montant=somme,should_notify=True,is_trans=True)
    notif(beneficiaire,"Retrait GaalguiMoney",message)

def EnvoiDirectNotif(envoyeur,receveur,somme,frais,employe,total,sommecoteclient):
    messageSend="Envoi de " + " " + str(sommecoteclient) + " " +  envoyeur.pays.monaie_associe.monaie+ " " + "a"+" "+  receveur.prenom + " " +  receveur.nom + " " + ",solde actuel:"+ " " + str(decimal.Decimal(envoyeur.solde))+" "+ envoveur.pays.monaie_associe.monaie
    messageGet= "Reception de " + " "  + str(somme) + " " + receveur.pays.monaie_associe.monaie  + " " + " de "+" " + envoyeur.prenom +" "+ envoyeur.nom +" "+" solde actuel"+" " +  str(decimal.Decimal(receveur.solde))+" "+receveur.pays.monaie_associe.monaie
    beneficiaire=receveur.prenom+" "+ receveur.nom
    donnateur=envoyeur.prenom+" "+ envoyeur.nom
    Messages.objects.create(user=receveur,message=messageGet,nature_transaction='reception',montant=sommecoteclient,
    donnateur=donnateur,should_notify=True,is_trans=True)
    Messages.objects.create(user=envoyeur,message=messageSend,nature_transaction='envoi direct',
        montant=somme,commission=frais,total=total,beneficiaire=beneficiaire,should_notify=False,is_trans=True)
   # NotificationAdmina.objects.create(employe=employe,somme=frais,nature='envoi direct')
    notif(receveur,"Reception GaalguiMoney",messageGet)


def EnvoiViaCodeNotif(envoyeur,trans,code,):
    message="Envoi de " + " " + str(trans.sommecoteclient) +" "+ trans.user.pays.monaie_associe.monaie+ " " +"par code"+" "+str(code)+ " " +",solde actuel:"+ " "+ str(decimal.Decimal(envoyeur.solde))+" "+ trans.user.pays.monaie_associe.monaie
    Messages.objects.create(user=envoyeur,message=message,nature_transaction='envoi via code',montant=somme,
        code=code,commission=frais,beneficiaire=receveur,total=total,should_notify=False,is_trans=True)
    #NotificationAdmina.objects.create(user=admina,somme=frais,nature="envoi via code")


def CodePayementEGaalgui(client,code):
    message='Votre code de verification est:'+" " + str(code)
    Messages.objects.create(user=client,message=message,nature_transaction='code',should_notify=True,is_trans=True)
    notif(client,"Code de verification",message)

def PayementEgaalgui(client,somme):
    message="Achat a  GaalguiShop de " + " " + str(somme) +" "+ " ,solde actuel:"+ " "+ str(decimal.Decima(client.solde))+" "+"CFA"
    Messages.objects.create(user=client,message=message,nature_transaction='payement',should_notify=True,
    is_trans=True)
    notif(client,"Payement E-GaalguiShop",message)


def AnnulationCommandeGaalguiShopNotif(client,somme,nom):
    message='Annulation de la commande  '+" "+ nom +" "+ "sur GaalguiShop + "+ " "+ str(somme)+ " "+ "solde actuel"+ " "+ str(decimal.Decimal(client.solde))
    Messages.objects.create(user=client,message=message,nature_transaction="annulation commande",
should_notify=True,is_trans=False)
    notif(client,"Annulation E-GaalguiShop",message)

def ActivationClientNotif(client):
    message="Votre compte a ete active avec succes,bienvenu dans la famille GaalguiMoney!"
    Messages.objects.create(user=client,message=message,nature_transaction="activation compte",should_notify=True,
    is_trans=False)
    notif(client,"Activation compte",message)

def NotifGaalguiPay(client,montant,nom,logo):
    message="Payement "+ " "+ nom +" "+ "-"+ str(montant)+" "+ ",solde actuel"+" " + str(client.solde)
    Messages.objects.create(user=client,message=message,nature_transaction="payement",
should_notify=False,is_trans=False,montant=montant,logo=logo)







