import os

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from .models import Company, Department, Employee, Role, User
from .serializers import (CompanySerializer, DepartmentSerializer,
                          EmployeeSerializer, RoleSerializer, UserSerializer)


def single_entry_update(request):
    if request.method == 'POST':
        serializer = EmployeeSerializer(data=request.POST)
        if serializer.is_valid():
            employee = serializer.save()
            # Handle success and return response
            return render(request, 'success.html', {'employee': employee})
        else:
            # Handle validation errors and return response
            return render(request, 'single_entry_update.html', {'serializer': serializer})
    else:
        serializer = EmployeeSerializer()
        return render(request, 'single_entry_update.html', {'serializer': serializer})

def is_valid_file_format(file_obj):
    valid_extensions = ['.csv', '.xlsx']  # List of valid file extensions
    
    # Get the file extension
    file_extension = os.path.splitext(file_obj.name)[1].lower()
    
    # Check if the file extension is in the list of valid extensions
    if file_extension in valid_extensions:
        return True
    else:
        return False

class BulkUploadView(generics.CreateAPIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES['file']
        # Process and validate the uploaded file
        try:
            # Validate the file format (e.g., check file extension, MIME type)
            if not is_valid_file_format(file_obj):
                return Response({'error': 'Invalid file format.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Parse the file based on its format
            parsed_data = parse_file(file_obj)
            
            # Deserialize the data using the appropriate serializer
            serializer = EmployeeSerializer(data=parsed_data, many=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Save or update the employee or company data in the database
            serializer.save()
            
            # Handle success and return response
            return redirect('api:bulk_upload_success')
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def bulk_upload_success(request):
    return render(request, 'success.html')

def user_profile(request, username):
    user = User.objects.get(username=username)
    serializer = UserSerializer(user)
    return render(request, 'user_profile.html', {'serializer': serializer.data})

def company_details(request, company_id):
    company = Company.objects.get(id=company_id)
    departments = Department.objects.filter(company=company)
    company_serializer = CompanySerializer(company)
    department_serializer = DepartmentSerializer(departments, many=True)
    return render(request, 'company_details.html', {
        'company': company_serializer.data,
        'departments': department_serializer.data
    })

def department_details(request, department_id):
    department = Department.objects.get(id=department_id)
    employees = Employee.objects.filter(department=department)
    department_serializer = DepartmentSerializer(department)
    employee_serializer = EmployeeSerializer(employees, many=True)
    return render(request, 'department_details.html', {
        'department': department_serializer.data,
        'employees': employee_serializer.data
    })

class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DepartmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer