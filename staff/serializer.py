from rest_framework import serializers
from .models import*
from user.serializer import EmployeSerializer


class NotificationStaffSerializer(serializers.ModelSerializer):
	employe=serializers.SerializerMethodField()
	class Meta:
		model=NotificationStaff
		fields="__all__"

	def get_employe(self,obj):
		return EmployeSerializer(obj.employe).data



class TendancePubSerializer(serializers.ModelSerializer):
	class Meta:
		model=TendancePub
		fields='__all__'



class ActionStaffSerializer(serializers.ModelSerializer):
	employe=serializers.SerializerMethodField()
	class Meta:
		model=ActionStaff
		fields="__all__"

	def get_user(self,obj):
		return EmployeSerializer(obj.user).data

