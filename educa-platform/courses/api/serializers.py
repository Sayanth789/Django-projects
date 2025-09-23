from django.db.models import Count
from rest_framework import serializers
from courses.models import Content, Course, Module, Subject


class SubjectSerializer(serializers.ModelSerializer):
    total_courses = serializers.SerializerMethodField()
    popular_courses = serializers.SerializerMethodField()

    def get_total_courses(self, obj):
        return obj.courses.count()

    def get_popular_courses(self, obj):
        courses = obj.courses.annotate(
            total_students=Count('students')
        ).order_by('-total_students')[:3]
        return [
            {"title": c.title, "total_students": c.total_students}
            for c in courses
        ]

    class Meta:
        model = Subject
        fields = ['id', 'title', 'total_courses', 'popular_courses']


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'subject', 'title', 'slug', 'overview',
            'created', 'owner', 'modules',
        ]


class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item']


class ModuleWithContentSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']


class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentSerializer(many=True)

    class Meta:
        model = Course
        fields = [
            'id', 'subject', 'title', 'slug', 'overview',
            'created', 'owner', 'modules'
        ]
