from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from .serializers import SignupSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'detail': 'Compte créé. En attente de validation par un administrateur.'},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"
        send_mail(
            subject='Réinitialisation de mot de passe',
            message=f'Réinitialise ton mot de passe : {reset_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
    except User.DoesNotExist:
        pass
    return Response({'detail': 'Si cet email existe, un lien a été envoyé.'})


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    uid = request.data.get('uid')
    token = request.data.get('token')
    password = request.data.get('password')
    try:
        user_id = urlsafe_base64_decode(uid).decode('ascii') 
        user = User.objects.get(pk=user_id)
        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Token invalide ou expiré.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response({'detail': 'Mot de passe mis à jour.'})
    except User.DoesNotExist:
        return Response({'detail': 'Utilisateur introuvable.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)