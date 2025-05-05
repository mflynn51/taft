from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import csv
import json
from django.contrib import messages
import folium, requests
from folium import GeoJson
from django.core.paginator import Paginator
from .models import GeoPoint
from django.contrib.auth.models import User
from django.db import IntegrityError



# empty list of locations 
locations = []

@csrf_exempt
def index(request):
    if request.user.is_authenticated:
        csv_file_path = "divert/data/waterPod3.csv"
    
        # Parse the CSV file and populate the model
        with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
            #decoded_file = csvfile.read().decode('utf-8').splitlines()
            reader = csv.DictReader(csvfile)

            for row in reader:
                #latitude, longitude, pod, podType, podRate, units, podStorage, owner, faceValueAF, maxDiversionFlow, unitsFlow, status= row #row[0], row[1], float(row[2]), float(row[3]), row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]
                
                
                GeoPoint.objects.get_or_create(
                    latitude=float(row['latitude']), 
                    longitude=float(row['longitude']), 
                    pod=(row['pod']), 
                    podType=(row['podType']),
                    podRate=int(row['podRate']), 
                    units=(row['units']), 
                    podStorage=int(row['podStorage']), 
                    owner=(row['owner']), 
                    faceValueAF=float(row['faceValueAF']), 
                    maxDiversionFlow=float(row['maxDiversionFlow']), 
                    unitsFlow=(row['unitsFlow']), 
                    status=(row['status'])
                )
                
        locationsX = list(GeoPoint.objects.values('latitude', 'longitude', 'pod', 'podType', 'podRate', 'units', 'podStorage', 'owner', 'faceValueAF', 'maxDiversionFlow', 'unitsFlow', 'status'))
        locations = sorted(locationsX, key=lambda x: x['pod'])
        locations_total  = GeoPoint.objects.all().order_by('-id')
        paginator = Paginator(locations_total, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "divert/index.html", {'locations': locations, 'page_obj': page_obj})
    else:
        return HttpResponseRedirect(reverse("login"))
    
@csrf_exempt
def location(request):
    if request.method == 'POST':
        data = request.POST
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        pod = data.get("pod")
        podType = data.get("podType")
        podRate = data.get("podRate")
        units = data.get("units")
        podStorage = data.get("podStorage")
        owner = data.get("owner")
        faceValueAF = data.get("faceValueAF")
        maxDiversionFlow = data.get("maxDiversionFlow")
        unitsFlow = data.get("unitsFlow")
        status = data.get("status")

        if latitude and longitude and pod:
            location = GeoPoint(latitude=latitude, longitude=longitude, pod=pod, podType=podType, podRate=podRate, units=units, podStorage=podStorage, owner=owner, faceValueAF=faceValueAF, maxDiversionFlow=maxDiversionFlow, unitsFlow=unitsFlow, status=status)
            location.save()
            
            return redirect('index')
        else:
            return JsonResponse({'error': 'Invalid data'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def location_point(request, location_id):
    
    location = GeoPoint.objects.get(id=location_id)
    
    return render(request, "divert/location_point.html", {
        "location": location,
    })      

# delete all diversion points
@csrf_exempt
def delete_all_pods(request):
    if request.method == 'POST':
        GeoPoint.objects.all().delete()
        messages.success(request, "All PODs have been deleted.")
    else:
        messages.error(request, "Invalid request method.")

    # Redirect to the map or another page
    return redirect('index')

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "divert/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "divert/login.html")
    
@csrf_exempt
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, "divert/register.html")

@csrf_exempt
def map_river(request):
    locations = list(GeoPoint.objects.values('latitude', 'longitude', 'pod', 'podType', 'podRate', 'units', 'podStorage', 'owner', 'faceValueAF', 'maxDiversionFlow', 'unitsFlow', 'status'))
    
    return render(request, 'divert/map_river.html', {'locations': locations})

@csrf_exempt
def map_aws(request):
    if request.user.is_authenticated:
        csv_file_path = "divert/data/waterPod3.csv"
    
        # Parse the CSV file and populate the model
        with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
            #decoded_file = csvfile.read().decode('utf-8').splitlines()
            reader = csv.DictReader(csvfile)

            for row in reader:
                # locations = list(GeoPoint.objects.values('latitude', 'longitude', 'pod', 'podType', 'podRate', 'units', 'podStorage', 'owner', 'faceValueAF', 'maxDiversionFlow', 'unitsFlow', 'status'))
                
                locationsX = list(GeoPoint.objects.values('latitude', 'longitude', 'pod', 'podType', 'podRate', 'units', 'podStorage', 'owner', 'faceValueAF', 'maxDiversionFlow', 'unitsFlow', 'status'))
                locations = sorted(locationsX, key=lambda x: x['pod'])
                locations_total  = GeoPoint.objects.all().order_by('-id')
                paginator = Paginator(locations_total, 10)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)

    return render(request, 'divert/map_aws.html', {'locations': locations, 'page_obj': page_obj})

@csrf_exempt
def map_aws_libre(request):
    
    return render(request, 'divert/map_aws_libre.html')

'''
def map_foo(request):
    csv_file_path = "/workspaces/mflynn51/hydro/divert/data/waterPod2.csv"
    
    # Parse the CSV file and populate the model
    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
        #decoded_file = csvfile.read().decode('utf-8').splitlines()
        reader = csv.DictReader(csvfile)

        for row in reader:
            #latitude, longitude, pod, podType, podRate, units, podStorage, owner, faceValueAF, maxDiversionFlow, unitsFlow, status= row #row[0], row[1], float(row[2]), float(row[3]), row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]
            
            GeoPoint.objects.get_or_create(
                latitude=float(row['latitude']), 
                longitude=float(row['longitude']), 
                pod=(row['pod']), 
                podType=(row['podType']), 
                podRate=int(row['podRate']), 
                units=(row['units']), 
                podStorage=int(row['podStorage']), 
                owner=(row['owner']), 
                faceValueAF=float(row['faceValueAF']), 
                maxDiversionFlow=float(row['maxDiversionFlow']), 
                unitsFlow=(row['unitsFlow']), 
                status=(row['status'])
            )
            
    locationsX = list(GeoPoint.objects.values('latitude', 'longitude', 'pod', 'podType', 'podRate', 'units', 'podStorage', 'owner', 'faceValueAF', 'maxDiversionFlow', 'unitsFlow', 'status'))
    locations = sorted(locationsX, key=lambda x: x['pod'])
    locations_total  = GeoPoint.objects.all().order_by('-id')
    paginator = Paginator(locations_total, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "divert/map_foo.html", {'locations': locations, 'page_obj': page_obj})
'''

@csrf_exempt
def delete_geo_point(request, location_id):
    location = get_object_or_404(GeoPoint, id=location_id)

    if request.method == "POST":
        
        location.delete()
        return redirect('index')  # Replace 'map' with your map view name

    return render(request, 'divert/location_point', {'location': location})