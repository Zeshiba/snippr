from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from snippr.models.userprofile import UserProfile, Feedback
from snippr.models.tracking import Tracking
from snippr.serializers.commit import CommitSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.six import text_type


class UserSerializer(serializers.HyperlinkedModelSerializer):
    issue_count = serializers.SerializerMethodField()
    issues = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    resolved_count = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'issues',
            'issue_count',
            'comment_count',
            'resolved_count',
            'id'
        )

    def get_issue_count(self, obj):
        ret = obj.commits.count()
        return ret

    def get_issues(self, obj):
        commits = obj.commits.order_by('-id')[:10]
        ret = CommitSerializer(commits, many=True)
        return ret.data

    def get_comment_count(self, obj):
        ret = obj.comments.count()
        return ret

    def get_resolved_count(self, obj):
        ret = Tracking.objects.filter(user=obj).exclude(resolved__isnull=True).count()
        return ret

    def get_id(self, obj):
        ret = obj.userprofile.id
        return ret


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = (
            'user',
            'message',
        )


class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        UserProfile.objects.create(user=user)
        return user


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(TokenObtainPairSerializer, self).validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = text_type(refresh)
        data['access'] = text_type(refresh.access_token)
        serializer = UserSerializer(self.user)
        data['user'] = serializer.data

        return data
