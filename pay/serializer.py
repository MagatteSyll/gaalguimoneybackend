from .models import*
from rest_framework import serializers
from user.serializer import UserSerializer,RegionSerializer
from staff.serializer import EmployeSerializer





'''
class PayModelSerializer(serializers.ModelSerializer):
	class Meta:
		model=PayModel
		fields="__all__"



class ProfessionnelSerializer(serializers.ModelSerializer):
	user=serializers.SerializerMethodField()
	adress=serializers.SerializerMethodField()
	class Meta:
		model=Professionel
		fields="__all__"
	def get_user(self,obj):
		return UserSerializer(obj.user).data

	def get_adress(self,obj):
		return RegionSerializer(obj.adress).data

class PayementProfessionnelSerializer(serializers.ModelSerializer):
	professionnel=serializers.SerializerMethodField()
	employe=serializers.SerializerMethodField()
	class Meta:
		model=PayementProfessionnel
		fields="__all__"


	def get_professionnel(self,obj):
		return ProfessionnelSerializer(obj.professionnel).data

	def get_employe(self,obj):
		return EmployeSerializer(obj.employe).data


		

class BusinessModelSerializer(serializers.ModelSerializer):
	user=serializers.SerializerMethodField()
	adress=serializers.SerializerMethodField()
	class Meta:
		model=BusinessModel
		fields='__all__'

	def get_user(self,obj):
		return UserSerializer(obj.user).data

	def get_adress(self,obj):
		return RegionSerializer(obj.adress).data


class PayementBusinessSerializer(serializers.ModelSerializer):
	business=serializers.SerializerMethodField()
	class Meta:
		model=PayementBusiness
		fields="__all__"

	def  get_business(self,obj):
		return BusinessModelSerializer(obj.business).data



class PayementPeriodicSerializer(serializers.ModelSerializer):
	professionnel=serializers.SerializerMethodField()
	business=serializers.SerializerMethodField()

	class Meta:
		model=PayementPeriodic
		fields='__all__'

	def  get_business(self,obj):
		return BusinessModelSerializer(obj.business).data

	def get_professionnel(self,obj):
		return ProfessionnelSerializer(obj.professionnel).data



class SuspensionPayementPeriodicSerializer(serializers.ModelSerializer):
	professionnel=serializers.SerializerMethodField()
	business=serializers.SerializerMethodField()

	class Meta:
		model=SuspensionPayementPeriodic
		fields='__all__'

	def  get_business(self,obj):
		return BusinessModelSerializer(obj.business).data

	def get_professionnel(self,obj):
		return ProfessionnelSerializer(obj.professionnel).data
'''



		
		


	


		
