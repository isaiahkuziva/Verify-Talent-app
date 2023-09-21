from rest_framework import serializers

from .models import Company, Department, Employee, Role, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 
                  'date_of_birth', 'profile_picture']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'address', 'phone_number', 'website']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'company']

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    company = CompanySerializer()
    department = DepartmentSerializer()
    role = RoleSerializer()

    class Meta:
        model = Employee
        fields = ['id', 'user', 'company', 'department', 
                  'role', 'start_date', 'end_date']