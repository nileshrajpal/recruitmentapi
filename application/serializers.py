from rest_framework import serializers, status

from user.models import User
from .models import Application, Education


class PostedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "is_admin"]


class ApplicationEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'qualification', 'passing_year', 'college', 'branch', 'percentage']

    def validate(self, data):
        percentage = data.get('percentage')
        if percentage < 0 or percentage > 100:
            raise serializers.ValidationError({'percentage': "Percentage value should be between 0 and 100"},
                                              code=status.HTTP_400_BAD_REQUEST)

        passing_year = data.get('passing_year')
        if passing_year < 1990 or passing_year > 2020:
            raise serializers.ValidationError({'passing_year': "Passing year should be between 1990 and 2020"},
                                              code=status.HTTP_400_BAD_REQUEST)

        return data


class ApplicationSerializer(serializers.ModelSerializer):
    posted_by = PostedBySerializer(read_only=True)
    posted_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    education = ApplicationEducationSerializer(many=True, required=False)

    class Meta:
        model = Application
        fields = ['id', 'posted_by', 'posted_at', 'updated_at', 'first_name', 'last_name', 'email', 'phone',
                  'address', 'education']

    def validate(self, data):
        phone = data.get('phone')
        try:
            if len(phone) != 10:
                raise serializers.ValidationError({'phone': "phone number should be 10 digit."},
                                                  code=status.HTTP_400_BAD_REQUEST)
            int(phone)
        except ValueError:
            raise serializers.ValidationError({'phone': "Invalid phone number value."},
                                              code=status.HTTP_400_BAD_REQUEST)
        return data

    def create(self, validated_data):
        if 'education' in validated_data:
            education = validated_data.pop('education')
            application = Application.objects.create(**validated_data)
            for edu in education:
                Education.objects.create(application=application, **edu)
            return application
        else:
            application = Application.objects.create(**validated_data)
            return application
