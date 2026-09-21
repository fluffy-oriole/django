from rest_framework import serializers


"""
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    class Meta:
        model = Student
        fields = ['id', 'name', 'group']
"""