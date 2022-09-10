from django.urls import path,include
from .views import*
from rest_framework.routers import SimpleRouter
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet


router=SimpleRouter()
router.register('resetpassword',ResetPassword)
router.register('managecode',RemoveCode)
router.register('envoyerdirect',EnvoyerDirect)
router.register('envoyercode', EnvoiViaCodeDirect)
 




urlpatterns=[
    path('',include(router.urls)),
    path('getphonecode/',GetCodeInscription.as_view()),
    path('verificationtel/',ConfirmationCode.as_view()),
    path('getuserphone/',GetPhoneCode.as_view()),
    path('finalisationinscription/',FinalisationRegistration.as_view()),
    path('login/',MyTokenObtainPairView.as_view()),
    path('token/refresh/',MyTokenRefreshPairView.as_view()),
    path('verifenvoi/',VerificationCredentialsEnvoi.as_view()),
    path('verificationviacode/',VerificationSomme.as_view()),
    path('getuser/',GetUser.as_view()),
    path('islog/',Authent.as_view()),
    path('message/',UserMessages.as_view()),
    path('verificationpayement/',VerificationPhonePourPayement.as_view()),
    path('payementgaalguishop/',Payementgaalgui.as_view()),
    path('annulationcommandegaalguishop/',AnnulationCommandeGaalgui.as_view()),
    path('recherchemessage/',RechercheMessage.as_view()),
    path('lastmessage/',LastMessages.as_view()),
    path('resetconfirmation/',ResetVerification.as_view()),
    path('recudirect/',RecuDirect.as_view()),
    path('recucode/',RecuCode.as_view()),
    path('messagespecifique/',RecuDonne.as_view()),
    path('getransaction/',GetRansactionEnvoiDirect.as_view()),
    path('getransactioncode/',GetRansactionCode.as_view()),
    path('getpub/',GetPub.as_view()),
    path('codereset/',CodeReset.as_view()),
    path('qrverification/',GetCodeQr.as_view()),
    path('getprofessionnel/',GetProfessionnel.as_view()),
    path('payementqrcode/',PayementQrCode.as_view()),
    path('recupayement/',RecuPayement.as_view()),
    path("verificationphonepourgaalguishop/",LierSonCompteGaalguiShop.as_view()),
    path("getnotification/",UserNotif.as_view()),
    path("usereadnotif/",UserNotifRead.as_view()),
    path("getbadgenotif/",UserBadgeNotif.as_view()),
    path("verifynumb/",VerifyContact.as_view()),
    path("getbeneficiaire/",GetUserFromPhone.as_view()),
    path("getuserweb/",GetUserFromId.as_view()),
    path('getuserqrcode/',GetUserQrCode.as_view()),
    path('qrcodeenvoiverification/',VerificationClientQrCodePay.as_view()),
    path('getuserdevice/',FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}))
    
    

]