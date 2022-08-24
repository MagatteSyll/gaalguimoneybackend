from django.urls import path,include
from .views import*
from rest_framework.routers import SimpleRouter


urlpatterns=[
    path('payementsde/',PayementFactureSDE.as_view()),
    path('getpayement/',GetPayement.as_view()),
    path('getpayementbusinessuser/',GetPayementBusinessUser.as_view()),
    path('getpayementprofessionnel/',GetPayementProfessionnelUser.as_view()),
    path("releverbusiness/",ReleverPayementBusiness.as_view()),
    path("releverprofessionnel/",ReleverPayementProfessionnel.as_view()),
    path("getrcode/",GetQrCode.as_view()),
    path("getpayofficiel/",GetPayOfficiel.as_view()),
    path("verificationbusinesspayslug/",VerifSlugPayementBusiness.as_view()),
    path("getbusinessmodel/",GetBusinessModel.as_view()),
    path("qrcodepayementbusiness/",QrCodePayementBusiness.as_view()),
    path("getbusinesspayement/",GetPayementQrBusiness.as_view()),
    path("getsinglepaybusiness/",GetSinglePayementBusiness.as_view()),
    path("getsinglepayprofessionnel/",GetSinglePayementProfessionnel.as_view())
    






]