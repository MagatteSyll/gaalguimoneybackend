from django.contrib import admin
from .models import*




class AccesAdmin(admin.ModelAdmin):
	list_display=['adress','get_region','get_pays']
	search_fields=['adress']
	class Meta:
		model=PointAcces

	@admin.display(empty_value='???')
	def get_region(self, obj):
		return obj.region.region

	@admin.display(empty_value='???')
	def get_pays(self, obj):
		return obj.region.pays.name
 

class UserAdmin(admin.ModelAdmin):
	list_display=['prenom', 'nom', 'phone','solde', 'active', 'professionnel', 'business','is_admin',
	 'is_staff', 'is_staff_simple','is_staff_bureau','is_staff_comptable','is_staff_manager','is_staff_techique']
	search_fields=['prenom','nom', 'phone']
	list_filter = ("is_staff","is_staff_simple","is_staff_bureau","is_staff_techique","is_staff_manager",
		"is_staff_comptable","professionnel","business")
	class Meta:
		model=User

	'''@admin.display(empty_value='???')
	def get_adress(self, obj):
		return obj.point_acces.adress'''

class EnvoiAdmin(admin.ModelAdmin):
	list_display=['get_envoyeur','somme','phone_receveur']
	list_display_links =[  'get_envoyeur']
	search_fields=['envoyeur__prenom']
	class Meta:
		model=Envoi
	@admin.display(empty_value='???')
	def get_envoyeur(self, obj):
		return obj.envoyeur.prenom+" "+obj.envoyeur.nom


class DepotAdmin(admin.ModelAdmin):
	list_display=['get_depositaire','somme',]
	list_display_links =[ 'get_depositaire']
	search_fields=['depositaire__prenom']
	class Meta:
		model=Depot

	@admin.display(empty_value='???')
	def get_depositaire(self, obj):
		return obj.depositaire.prenom+" "+obj.depositaire.nom

class VerificationTransactionAdmin(admin.ModelAdmin):
	list_display=['get_user','id']
	class Meta:
		model=VerificationTransaction

	@admin.display(empty_value='???')
	def get_user(self, obj):
		return obj.user.prenom+" "+obj.user.nom

class RetraitAdmin(admin.ModelAdmin):
	list_display=['get_beneficiaire','somme',]
	list_display_links =['get_beneficiaire']
	search_fields=['beneficiaire__prenom' ]
	class Meta:
		model=Retrait

	@admin.display(empty_value='???')
	def get_beneficiaire(self, obj):
		return obj.beneficiaire.prenom+" "+obj.beneficiaire.nom

class ViaCodeAdmin(admin.ModelAdmin):
	list_display=['Nom_complet_du_receveur', 'somme','code','active']
	search_fields=['Nom_complet_du_receveur','code']
	list_filter = ("active", )
	class Meta:
		model=ViaCode



class MessagesAdmin(admin.ModelAdmin):
	list_display=['get_user', 'nature_transaction',]
	search_fields=[ 'user__prenom' ]
	list_display_links =[ 'get_user']
	class Meta:
		model=Messages

	@admin.display(empty_value='???')
	def get_user(self, obj):
		return obj.user.prenom+" "+obj.user.nom
'''

class PhoneVerificationEnModifiantAdmin(admin.ModelAdmin):
	list_display=[ 'get_user','code','active']
	search_fields=['user__prenom' ]
	list_display_links =[ 'get_user']
	class Meta:
		model=PhoneVerificationCode

	@admin.display(empty_value='???')
	def get_user(self, obj):
		return obj.user.prenom+" "+obj.user.nom'''

class PayementGaalguiShopAdmin(admin.ModelAdmin):
	list_display=['get_user','livraison']
	search_fields=['user__prenom' ]
	list_display_links =['get_user']
	class Meta:
		model=PayementGaalgui

	@admin.display(empty_value='???')
	def get_user(self, obj):
		return obj.user.prenom+" "+obj.user.nom

class AnnulationGaalguiShopAdmin(admin.ModelAdmin):
	list_display=['get_user','get_total']
	list_display_links =['get_user']
	class Meta:
		model=AnnulationGaalguiShop

	@admin.display(empty_value='???')
	def get_user(self, obj):
		return obj.payement.user.prenom+" "+obj.payement.user.nom

	@admin.display(empty_value='???')
	def get_total(self, obj):
		return obj.payement.total+" "+obj.payement.total


class QrCodeClientAdmin(admin.ModelAdmin):
	list_display=['get_user']
	list_display_links=['get_user']
	class Meta:
		model=QrCodeClient

	@admin.display(empty_value='???')
	def get_user(self, obj):
		return obj.user.prenom+" "+obj.user.nom



class RegionAdmin(admin.ModelAdmin):
	list_display=['region','get_pays']
	search_fields=['region' ]
	class Meta:
		model=Region

	@admin.display(empty_value='???')
	def get_pays(self, obj):
		return obj.pays.name

class PhoneConfirmationInscriptionAdmin(admin.ModelAdmin):
	list_display=['phone','code',]
	search_fields=['phone' ]
	class Meta:
		model=PhoneConfirmation


class ServiceAdmin(admin.ModelAdmin):
	list_display=['get_user','adress','contact']
	search_fields=['adress','contact']
	list_display_links=['get_user']
	class Meta:
		model=Service

	@admin.display(empty_value='???')
	def get_user(self, obj):
		return obj.user.prenom+" "+obj.user.nom

class ContinentAdmin(admin.ModelAdmin):
	list_display=['continent']
	search_fields=['continent',]
	list_display_links=['continent']
	class Meta:
		model=Continent


class MonaieAdmin(admin.ModelAdmin):
	list_display=['monaie','valeur_CFA']
	search_fields=['monaie',]
	list_display_links=['monaie']
	class Meta:
		model=Monaie





admin.site.register(User,UserAdmin)
admin.site.register(Envoi,EnvoiAdmin)
admin.site.register(Depot,DepotAdmin)
admin.site.register(Retrait,RetraitAdmin)
admin.site.register(ViaCode,ViaCodeAdmin)
admin.site.register(Messages,MessagesAdmin)
#admin.site.register(PhoneVerificationCode,PhoneVerificationEnModifiantAdmin)
admin.site.register(PayementGaalgui,PayementGaalguiShopAdmin)
admin.site.register(PhoneConfirmation,PhoneConfirmationInscriptionAdmin)
admin.site.register(Region,RegionAdmin)
admin.site.register(VerificationTransaction,VerificationTransactionAdmin)
admin.site.register(Pays)
admin.site.register(PointAcces,AccesAdmin)
admin.site.register(AnnulationGaalguiShop,AnnulationGaalguiShopAdmin)
admin.site.register(QrCodeClient,QrCodeClientAdmin)
admin.site.register(Service,ServiceAdmin)
admin.site.register(Continent,ContinentAdmin)
admin.site.register(Monaie,MonaieAdmin)




	





		
	
		
	