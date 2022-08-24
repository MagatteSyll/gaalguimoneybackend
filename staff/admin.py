from django.contrib import admin
from .models import*


class ActionStaffAdmin(admin.ModelAdmin):
	list_display=['get_employe', 'created',]
	list_display_links =['get_employe']
	list_filter = ("nature", )
	class Meta:
		model=ActionStaff

	@admin.display(empty_value='???')
	def get_employe(self, obj):
		return obj.employe.user.prenom+" "+obj.employe.user.nom

class EmployeAdmin(admin.ModelAdmin):
	list_display=['get_user','adress','get_region','get_pays']
	list_display_links=['get_user']
	class Meta:
		model=Employe

	@admin.display(empty_value='???')
	def adress(self, obj):
		return obj.point_acces.adress

	@admin.display(empty_value='???')
	def get_user(self, obj):
		return obj.user.prenom+" "+obj.user.nom

	@admin.display(empty_value='???')
	def get_region(self, obj):
		return obj.point_acces.region.region

	@admin.display(empty_value='???')
	def get_pays(self, obj):
		return obj.point_acces.region.pays.name



class TendancePubAdmin(admin.ModelAdmin):
	list_display=['description','active']
	search_fields=['description']
	class Meta:
		model=TendancePub



class NotificationStaffAdmin(admin.ModelAdmin):
	list_display=['get_employe',]
	#search_fields=['user__prenom' ]
	list_display_links =[ 'get_employe']
	class Meta:
		model=NotificationStaff

	@admin.display(empty_value='???')
	def get_employe(self, obj):
		return obj.employe.user.prenom+" "+obj.employe.user.nom


admin.site.register(TendancePub,TendancePubAdmin)
admin.site.register(ActionStaff,ActionStaffAdmin)
admin.site.register(NotificationStaff,NotificationStaffAdmin)
admin.site.register(Employe,EmployeAdmin)

