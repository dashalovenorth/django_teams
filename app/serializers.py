from django.contrib.auth.models import User
from rest_framework import serializers

from app.models import Project, Developer, Team


class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = "id", "name", 'surname', 'position'

    def create(self, validated_data):
        user = User.objects.create(username=validated_data["name"])
        user.save()
        validated_data["user_id"] = user.id
        return super().create(validated_data)


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    developers = DeveloperSerializer(read_only=True, many=True, required=False)

    class Meta:
        model = Team
        fields = 'name', 'developers'

    def create(self, validated_data):
        developer = self.context["request"].data.get("developer")
        if developer:
            validated_data["developers"] = [
                Developer.objects.get(pk=developer)
            ]
        return super().create(validated_data)


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = "id", "name", "date_start", "status"
