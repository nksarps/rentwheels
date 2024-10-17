from .models import Listing
from .serializers import ListingSerializer
from accounts.permissions import IsVerified
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


def get_listing_or_404(id):
    try:
        return Listing.objects.get(id=id)
    except Listing.DoesNotExist:
        return None


def listing_not_found_response():
    return Response(
        {
            'success':False,
            'message':'Listing does not exist'
        }, status=status.HTTP_404_NOT_FOUND
    )


@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_listing(request):
    if request.method == 'POST':
        serializer = ListingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    'success':True,
                    'message':serializer.data
                }, status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'success':False,
                'message':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def get_listing_by_id(request, id):
    if request.method == 'GET':
        listing = get_listing_or_404(id=id)
        if not listing:
            return listing_not_found_response()

        serializer = ListingSerializer(listing)

        return Response(
            {
                'success':True,
                'message':serializer.data
            }, status=status.HTTP_201_CREATED
        )


@api_view(['GET'])
def get_all_listings(request):
    if request.method == 'GET':
        listings = Listing.objects.all()

        serializer = ListingSerializer(listings, many=True)

        return Response(
            {
                'success':True,
                'message':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def update_listing(request, id):
    if request.method == 'PUT' or request.method == 'PATCH':
        listing = get_listing_or_404(id=id)
        if not listing:
            return listing_not_found_response()

        serializer = ListingSerializer(listing, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    'success':True,
                    'message':serializer.data
                }, status=status.HTTP_200_OK
            )
        return Response(
            {
                'success':False,
                'message':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_listing(request, id):
    if request.method == 'DELETE':
        listing = get_listing_or_404(id=id)
        if not listing:
            return listing_not_found_response()

        listing.delete()

        return Response(
            {
                'success':True,
                'message':'Listing deleted!'
            }, status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET'])
def search_for_listing(request):
    if request.method == 'GET':
        query = request.query_params.get('query')
        if not query:
            return Response(
                {
                    'success':True,
                    'message':'Provide a search query'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        results = Listing.objects.filter(
            Q(make__icontains=query) |
            Q(model__icontains=query) |
            Q(body_type__icontains=query)
        )

        serializer = ListingSerializer(results, many=True)

        return Response(
            {
                'success':True,
                'results':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
def filter_listings(request):
    if request.method == 'GET':
        make = request.query_params.get('make')
        model = request.query_params.get('model')
        body_type = request.query_params.get('body_type')

        if not make and not model and not body_type:
            return Response(
                {
                    'success':False,
                    'message':'Provide a filter query'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        results = Listing.objects.all()
        if make:
            results = results.filter(make__icontains=make)
        if model:
            results = results.filter(model__icontains=model)
        if body_type:
            results = results.filter(body_type__icontains=body_type)
        
        serializer = ListingSerializer(results, many=True)

        return Response(
            {
                'success':True,
                'results':serializer.data
            }, status=status.HTTP_200_OK
        )

        
