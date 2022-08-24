from django.contrib import admin
from .models import*




'''
class PayModelAdmin(admin.ModelAdmin):
	list_display=['alias','get_adress']
	class Meta:
		model=PayModel

	@admin.display(empty_value='???')
	def get_adress(self, obj):
		return obj.adress.pays.name

class BusinessModelAdmin(admin.ModelAdmin):
	list_display=['nom','contact','get_region','get_pays']
	search_fields=['nom']
	class Meta:
		model=BusinessModel

	@admin.display(empty_value='???')
	def get_region(self, obj):
		return obj.adress.region

	@admin.display(empty_value='???')
	def get_pays(self, obj):
		return obj.adress.pays.name


class CodeGenerateAdmin(admin.ModelAdmin):
	list_display=['get_business']
	search_fields=['business__nom']
	list_display_links=['get_business']

	@admin.display(empty_value='???')
	def get_business(self, obj):
		return obj.business.nom


class ProfessionnelAdmin(admin.ModelAdmin):
	list_display=['nom','created']
	list_display_links =['nom']
	class Meta:
		model=Professionel





class PayementProfessionnelAdmin(admin.ModelAdmin):
	list_display=['nom_complet_client','get_professionnel','montant']
	list_display_links=['nom_complet_client','get_professionnel']
	class Meta:
		model=PayementProfessionnel

	@admin.display(empty_value='???')
	def get_professionnel(self, obj):
		return obj.professionnel.nom

class PayementBusinessAdmin(admin.ModelAdmin):
	list_display=['nom_complet_client','get_business','somme']
	search_fields=['nom_complet_client']
	list_display_links=['nom_complet_client','get_business']
	class Meta:
		model=PayementBusiness

	@admin.display(empty_value='???')
	def get_business(self, obj):
		return obj.business.nom

class PayementPeriodicAdmin(admin.ModelAdmin):
	list_display=['get_professionnel','get_business','montant']
	list_display_links=['get_professionnel','get_business']
	class Meta:
		model=PayementPeriodic

	@admin.display(empty_value='???')
	def get_professionnel(self, obj):
		if obj.professionnel is not None:
			return obj.professionnel.nom
		return "compte professionnel"

	@admin.display(empty_value='???')
	def get_business(self, obj):
		if obj.business is not None:
			return obj.business.nom
		return "compte business"

class SuspensionPayementPeriodicAdmin(admin.ModelAdmin):
	list_display=['get_professionnel','get_business','montant']
	list_display_links=['get_professionnel','get_business']
	class Meta:
		model=SuspensionPayementPeriodic

	@admin.display(empty_value='???')
	def get_professionnel(self, obj):
		if obj.professionnel is not None:
			return obj.professionnel.nom
		return "compte professionnel"

	@admin.display(empty_value='???')
	def get_business(self, obj):
		if obj.business is not None:
			return obj.business.nom
		return "compte business"


class CodeGenerateProfessionnelAdmin(admin.ModelAdmin):
	list_display=['get_professionnel']
	list_display_links=['get_professionnel']

	class Meta:
		model=CodeGenerateProfessionnel

	@admin.display(empty_value='???')
	def get_professionnel(self, obj):
		return obj.professionnel.nom









admin.site.register(PayementProfessionnel,PayementProfessionnelAdmin)
admin.site.register(BusinessModel,BusinessModelAdmin)
admin.site.register(PayementBusiness,PayementBusinessAdmin)
admin.site.register(Professionel,ProfessionnelAdmin)
admin.site.register(CodeGenerate,CodeGenerateAdmin)
admin.site.register(PayModel,PayModelAdmin)
admin.site.register(PayementPeriodic,PayementPeriodicAdmin)
admin.site.register(SuspensionPayementPeriodic,SuspensionPayementPeriodicAdmin)
admin.site.register(CodeGenerateProfessionnel,CodeGenerateProfessionnelAdmin)

'''