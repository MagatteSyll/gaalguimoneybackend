from django.urls import path,include
from .views import*
from rest_framework.routers import SimpleRouter



router=SimpleRouter()
router.register('lestransactions',LesTransactions)
#router.register('suspensionbusiness',SuspensionBusiness)
#router.register('suspensionprofessionnel',SuspensionProfesionnel)




urlpatterns=[
    path('',include(router.urls)),
   # path('isstaff/',IsStaff.as_view()),
    path('getclientdepot/',GetClientDepot.as_view()),
    path('getclientretrait/',GetClientRetrait.as_view()),
    path('verificationcode/',RetraitViaCode.as_view()),
    path('notifstaff/',NotifStaff.as_view()),
    path('adress/',Adressage.as_view()),
    path('recudepot/',RecuDepot.as_view()),
    path('recuretrait/',RecuRetrait.as_view()),
    path('commissionincluse/',CommissionEnvoiCodeInclus.as_view()),
    path('commissionnonincluse/',CommissionEnvoiCodeNonIncluse.as_view()),
    path('recuviacode/',RecuViaCode.as_view()),
    path('recuretraitcode/',RecuRetraitCode.as_view()),
    path('dernierestransaction/',LastMessageStaf.as_view()),
    path('gettransaction/',GetRansaction.as_view()),
    path('getuseractivation/',VerificationPourActivation.as_view()),
    path('getpolza/',GetPolza.as_view()),
    path('activationduclient/',ActivationDuClient.as_view()),
    path('getclientdesactivation/',GetClientDesactivation.as_view()),
    path('getpolzadesactivation/', ConfirmationDesactivation.as_view()),
    path('confirmationdesactivation/',DesactivationDuClient.as_view()),
    path('verificationnouvelmembre/',VerificationNouvelMembreStaf.as_view()),
    path('getpolzanouvelmembre/',GetClientNouvelMembreStaf.as_view()),
    path('confirmationnouveaumembrestaff/',ConfirmationStaff.as_view()),
    path('ajoutpub/',AjoutNewPub.as_view()),
    #path('createbusiness/', CreateBusiness.as_view()),
    path('getpointacces/',GetPointAcces.as_view()),
    path('getregion/',GetRegion.as_view()),
    #path('getqrcode/',GetQrCode.as_view()),
    #path('getpublicpay/',GetPublicPay.as_view()),
    #path('verificationbusiness/',VerificationSuspensionBusiness.as_view()),
    #path('getuserbusiness/',GetBusinessUser.as_view()),
    #path('createprofessionnel/',CreateProfesionnel.as_view()),
    #path('verificationprofessionnel/',VerificationSuspensionProfessionnel.as_view()),
    #path('getpayprofessionnel/',GetProfessionnelPay.as_view()),
    #path('getqrprofessionnel/',GetQrCodeProfessionnel.as_view()),
    path('getlesdepots/',GetLesDepots.as_view()),
    path('releverdepot/',ReleverDepot.as_view()),
    path('getlesretraits/',GetLesRetraits.as_view()),
    path('releveretrait/',ReleverRetrait.as_view()),
    path('getlesretraitscode/',GetLesRetraitCode.as_view()),
    path('releverretraitcode/',ReleveRetraitCode.as_view()),
    path('getlesenvoiscodes/', GetEnvoiCode.as_view()),
    path('releverenvoicode/',ReleveEnvoiCode.as_view()),
    path('getlesenvois/',GetLesEnvoi.as_view()),
    path('releverenvoi/',ReleveEnvoi.as_view()),
    #path('getlespayements/',GetLesPayements.as_view()),
    #path('releverpayement/',RelevePayement.as_view()),
    path('getlespayementsgaalguishop/',GetLesPayementsGaalguiShop.as_view()),
    path('releverpayementgaalguishop/',RelevePayementGaalguiShop.as_view()),
    path('getlesannulationsgaalguishop/',AnnulationGaalguiShop.as_view()),
    path('releveannulationgaalguishop/',ReleveAnnulationGaalguiShop.as_view()),
    #path('getlespayementsperiodic/',GetPayementPeriodic.as_view()),
    #path('relevepayementperiodic/',RelevePayementPeriodic.as_view()),
    #path('getsuspensionperiodic/',GetSuspensionPeriodic.as_view()),
    #path('relevesuspensionperiodic/',ReleveSuspensionPayementPeriodic.as_view()),
    path('verificationclientreactivation/',VerifyClientReactivation.as_view()),
    path('getpolzareactivation/',GetUserReactivation.as_view()),
    path('reactivationuser/',ReactivationClient.as_view())
    
    



    

    

 





]