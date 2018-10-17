from rest_framework.viewsets import ViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate

from snippr.serializers import user
from django.contrib.auth.models import User


class UserViews(ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = User.objects.all()
        serializer = user.UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = User.objects.filter(pk=pk).first()
        if(user):
            serializer = user.UserSerializer(user)
            return Response(serializer.data)
        return Response("User does not exist.")


class RegistrationViews(ViewSet):

    def create(self, request):
        obj = request.data
        x = user.RegisterSerializer(data=obj)
        res = {"message": "Please input correct credentials", }
        if x.is_valid() is True:
            new_user = x.save()
            res['message'] = "Successfully registered"
        return Response(res)


class LoginViews(ViewSet):

    def create(self, request):
        obj = request.data
        auth_user = authenticate(username=obj['username'], password=obj['password'])
        retval = {'message': 'incorrect'}
        if auth_user is not None:
            retval = user.LoginSerializer(user)
            retval = retval.data
            retval['message'] = 'successful'
        return Response(retval)
