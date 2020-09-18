from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.spots import Spot
from ..serializers import SpotSerializer, UserSerializer

class Spots(generics.ListCreateAPIView):
  permission_classes=(IsAuthenticated,)
  serializer_class = SpotSerializer
  def get(self, request):
    """index request"""
    spots = Spot.objects.all()
    # spots = Spot.objects.filter(owner=request.user.id)
    data = SpotSerializer(spots, many=True).data
    return Response({ 'spots': data })

  def post(self, request):
    """Create request"""
    request.data['spot']['owner'] = request.user.id
    spot = SpotSerializer(data=request.data['spot'])
    if spot.is_valid():
      spot.save()
      return Response({ 'spot': spot.data }, status=status.HTTP_201_CREATED)

    return Response(spot.errors, status=status.HTTP_400_BAD_REQUEST)

class SpotDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes=(IsAuthenticated,)
  def get(self, request, pk):
    """Show request"""
    spot = get_object_or_404(Spot, pk=pk)
    if not request.user.id == spot.owner.id:
      raise PermissionDenied('Unauthorized, you do not own this spot')

    data = SpotSerializer(spot).data
    return Response({ 'spot': data })

  def delete(self, request, pk):
    """Delete request"""
    spot = get_object_or_404(Spot, pk=pk)
    if not request.user.id == spot.owner.id:
      raise PermissionDenied('Unauthorized, you do not own this spot')

    spot.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

  def partial_update(self, request, pk):
    """Update Request"""
    if request.data['spot'].get('owner', False):
      del request.data['spot']['owner']
    spot = get_object_or_404(Spot, pk=pk)
    if not request.user.id == spot.owner.id:
      raise PermissionDenied('Unauthorized, you do not own this spot')

    request.data['spot']['owner'] = request.user.id
    data = SpotSerializer(spot, data=request.data['spot'])
    if data.is_valid():
      data.save()
      return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
