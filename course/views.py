from decimal import Decimal
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from department.models import Department
from university.models import University
from users.models import UserAccount
from users.permissions import *
from .serializers import *


@api_view(['GET'])
@permission_classes([UniversityAdminToMod])
def get_courses(request):
    try:
        courses = Course.objects.filter(university=request.user.university)
    except Course.DoesNotExist:
        return Response(status=404)

    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([UniversityAdminToMod])
def get_section(request):
    section_id = request.GET.get('section_id')

    try:
        section = Section.objects.get(id=section_id)
    except Section.DoesNotExist:
        return Response(status=404)

    serializer = SectionSerializer(section)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([UniversityAdminToMod])
def get_course_sections(request):
    course_id = request.GET.get('course_id')

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response(status=404)

    sections = Section.objects.filter(course=course)
    return Response(SectionSerializer(sections, many=True).data)


@api_view(['POST'])
@permission_classes([UniversityAdminToMod])
def create_section(request):
    name = request.data.get('name')
    trimester = request.data.get('trimester')
    course_id = request.data.get('course_id')

    try:
        course = Course.objects.filter(id=course_id).first()
    except Course.DoesNotExist:
        return Response(status=404)

    if course is None:
        return Response(status=404)

    section = Section.objects.create(name=name, trimester=trimester, course=course)
    return Response(SectionSerializer(section).data)


@api_view(['POST'])
@permission_classes([UniversityAdminToMod])
def update_section(request):
    section_id = request.data.get('section_id')
    name = request.data.get('name')
    trimester = request.data.get('trimester')

    try:
        section = Section.objects.filter(id=section_id).first()
    except Section.DoesNotExist:
        return Response(status=404)

    if section is None:
        return Response(status=404)

    section.name = name
    section.trimester = trimester
    section.save()
    return Response(SectionSerializer(section).data)


@api_view(['POST'])
@permission_classes([UniversityAdminToMod])
def delete_section(request):
    section_id = request.data.get('section_id')

    try:
        section = Section.objects.filter(id=section_id).first()
    except Section.DoesNotExist:
        return Response(status=404)

    if section is None:
        return Response(status=404)

    section.delete()
    return Response(status=200)


@api_view(['POST'])
@permission_classes([UniversityAdminToMod])
def create_course(request):
    name = request.data.get('name')
    code = request.data.get('code')
    credit = request.data.get('credit')
    course_type = request.data.get('type')
    department_id = request.data.get('department_id')

    try:
        university = request.user.university
        department = Department.objects.get(id=department_id)
    except University.DoesNotExist:
        return Response(status=404)

    if university is None or department is None:
        return Response(status=404)

    course = Course.objects.create(name=name, code=code, credit=credit, type=course_type, department=department, university=university)
    return Response(CourseSerializer(course).data)


@api_view(['POST'])
@permission_classes([UniversityAdminToMod])
def delete_course(request):
    course_id = request.data.get('course_id')

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response(status=404)

    if course is None:
        return Response(status=404)

    course.delete()
    return Response({
        'status': 'success',
        'message': 'Course Removed'
    })


@api_view(['POST'])
@permission_classes([UniversityAdminToMod])
def add_faculty_to_section(request):
    section_id = request.data.get('section_id')
    faulty_id = request.data.get('faculty_id')

    try:
        section = Section.objects.get(id=section_id)
        faulty = UserAccount.objects.get(id=faulty_id)
    except Section.DoesNotExist or UserAccount.DoesNotExist or UserAccount.user_type != UserType.FACULTY:
        return Response(status=404)

    if section is None or faulty is None:
        return Response(status=404)

    section.faulty.add(faulty)
    section.save()

    return Response({
        'status': 'success',
        'message': 'Faulty Added'
    })

