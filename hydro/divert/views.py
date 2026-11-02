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
from .models import GeoPoint, ProductionRecord, TreeBlock
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.conf import settings
from datetime import datetime



# empty list of locations 
locations = []

@csrf_exempt
def index(request):
    if request.user.is_authenticated:
        csv_file_path = settings.BASE_DIR / "divert" / "data" / "waterPod3.csv"

        # Parse the CSV file and populate the model
        with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
            #decoded_file = csvfile.read().decode('utf-8').splitlines()
            reader = csv.DictReader(csvfile)

            for row in reader:
                #latitude, longitude, pod, podType, podRate, units, podStorage, owner, faceValueAF, maxDiversionFlow, unitsFlow, status= row #row[0], row[1], float(row[2]), float(row[3]), row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]
                
                
                GeoPoint.objects.get_or_create(
                    latitude=float(row['latitude']),
                    longitude=float(row['longitude']),
                    pod=row['pod'],
                    podType=row['podType'],
                    podRate=int(row['podRate']),
                    units=row['units'],
                    podStorage=int(row['podStorage']),
                    owner=row['owner'],
                    faceValueAF=float(row['faceValueAF']),
                    maxDiversionFlow=float(row['maxDiversionFlow']),
                    unitsFlow=row['unitsFlow'],
                    status=row['status'],
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
        csv_file_path = settings.BASE_DIR / "divert" / "data" / "waterPod3.csv"

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

PRODUCTION_SIZE_FIELDS = [
    ("BINS", "bins"),
    ("JUICE ", "juice"),
    ("CULLS", "culls"),
] + [
    (f"{csv_prefix} {size}", f"{field_prefix}_{size}")
    for csv_prefix, field_prefix in [
        ("SUNKIST", "sunkist"),
        ("CHOICE", "choice"),
        ("SK EXP BRIX", "sk_exp_brix"),
        ("SK EXPORT", "sk_export"),
        ("SK EXP HP", "sk_exp_hp"),
        ("CH EXP HP", "ch_exp_hp"),
        ("SK EXP PO/BA", "sk_exp_po_ba"),
    ]
    for size in [36, 40, 48, 56, 72, 88, 113, 138, 163, 180]
]


def _parse_production_date(value):
    value = (value or "").strip()
    if not value:
        return None
    return datetime.strptime(value, "%m/%d/%y").date()


def _parse_production_float(value):
    value = (value or "").strip()
    if not value:
        return None
    return float(value)


def _parse_production_row(row):
    fields = {
        "pool": row["POOL"],
        "year": int(row["YEAR"]),
        "variety": row["VARIETY"],
        "parcel": row["PARCEL"],
        "apn": row["APN"],
        "ranch": row["RANCH"],
        "ranch_code": row["RANCH_CODE"],
        "pack_start": _parse_production_date(row["PACK_START"]),
        "pack_end": _parse_production_date(row["PACK_END"]),
        "grower": row["GROWER"],
        "block": row["BLOCK"],
        "bins": _parse_production_float(row["BINS"]),
    }
    for csv_header, field_name in PRODUCTION_SIZE_FIELDS:
        fields[field_name] = _parse_production_float(row[csv_header])
    return ProductionRecord(**fields)


def _load_production_records():
    csv_file_path = settings.BASE_DIR / "divert" / "data" / "production Rod.csv"

    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        return [_parse_production_row(row) for row in reader if row["POOL"].strip()]


def _load_cvp_class1_contracts():
    """CVP Class 1 contract rows keyed by IDforMap, for joining to OBJECTID on the water districts layer."""
    csv_file_path = settings.BASE_DIR / "divert" / "data" / "CVP Class 1 contracts for GIS 03052021.csv"

    contracts = {}
    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            id_for_map = (row.get("IDforMap") or "").strip()
            if not id_for_map:
                continue
            contracts[id_for_map] = {
                "agency_uniq": (row.get("AGENCYUNIQ") or "").strip(),
                "agency": (row.get("Friant Division Contracts") or "").strip(),
                "cvp_contract": (row.get("CVP Contract ") or "").strip(),
                "contract": (row.get("Contract ") or "").strip(),
                "division": (row.get("CVP Division") or "").strip(),
                "unit": (row.get("Unit") or "").strip(),
                "contract_class": (row.get("Class") or "").strip(),
                "max_contract_quantity": (row.get("Max Contract Quantity") or "").strip(),
                "mi_use": (row.get("M&I Use") or "").strip(),
                "contract_amount_ag": (row.get("Contract Amount for AG") or "").strip(),
                "expiry": (row.get("Contract Expiry") or "").strip(),
            }
    return contracts


@csrf_exempt
def map_farm(request):
    production_records = _load_production_records()
    ranches = sorted({record.ranch for record in production_records})
    tree_blocks = TreeBlock.objects.all().order_by('name')
    tree_blocks_json = [
        {
            'name': tree_block.name,
            'coordinates': [list(point) for point in tree_block.coordinates],
        }
        for tree_block in tree_blocks
    ]
    return render(request, 'divert/map_farm.html', {
        'production_records': production_records,
        'ranches': ranches,
        'tree_blocks': tree_blocks,
        'tree_blocks_json': tree_blocks_json,
        'cvp_class1_contracts': _load_cvp_class1_contracts(),
    })

@csrf_exempt
def map_putt(request):
    return render(request, 'divert/map_putt.html')

@csrf_exempt
def map_pool(request):
    records = _load_production_records()

    selected_pool = request.GET.get('pool')
    if selected_pool:
        records = [record for record in records if record.pool == selected_pool]

    pools = [
        {
            "record": record,
            "fields": [
                (field.verbose_name, getattr(record, field.name))
                for field in ProductionRecord._meta.fields
                if field.name != "id"
            ],
        }
        for record in records
    ]
    return render(request, 'divert/map_pool.html', {'pools': pools, 'selected_pool': selected_pool})

@csrf_exempt
def map_ranch(request):
    selected_ranch = request.GET.get('ranch')
    records = _load_production_records()
    if selected_ranch:
        records = [record for record in records if record.ranch == selected_ranch]

    return render(request, 'divert/map_ranch.html', {
        'production_records': records,
        'selected_ranch': selected_ranch,
    })

def map_foo(request):
    csv_file_path = settings.BASE_DIR / "divert" / "data" / "waterPod3.csv"
    
    # Parse the CSV file and populate the model
    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
        #decoded_file = csvfile.read().decode('utf-8').splitlines()
        reader = csv.DictReader(csvfile)

        for row in reader:
            #latitude, longitude, pod, podType, podRate, units, podStorage, owner, faceValueAF, maxDiversionFlow, unitsFlow, status= row #row[0], row[1], float(row[2]), float(row[3]), row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]
            
            GeoPoint.objects.get_or_create(
                latitude=float(row['latitude']),
                longitude=float(row['longitude']),
                pod=row['pod'],
                podType=row['podType'],
                podRate=int(row['podRate']),
                units=row['units'],
                podStorage=int(row['podStorage']),
                owner=row['owner'],
                faceValueAF=float(row['faceValueAF']),
                maxDiversionFlow=float(row['maxDiversionFlow']),
                unitsFlow=row['unitsFlow'],
                status=row['status'],
            )
            
    locationsX = list(GeoPoint.objects.values('latitude', 'longitude', 'pod', 'podType', 'podRate', 'units', 'podStorage', 'owner', 'faceValueAF', 'maxDiversionFlow', 'unitsFlow', 'status'))
    locations = sorted(locationsX, key=lambda x: x['pod'])
    locations_total  = GeoPoint.objects.all().order_by('-id')
    paginator = Paginator(locations_total, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "divert/map_foo.html", {'locations': locations, 'page_obj': page_obj})


@csrf_exempt
def create_tree_block(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    required_fields = [
        'name', 'variety', 'year_planted',
        'lat1', 'lon1', 'lat2', 'lon2', 'lat3', 'lon3', 'lat4', 'lon4',
    ]
    if not all(data.get(field) not in (None, '') for field in required_fields):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    try:
        optional_point = lambda field: float(data[field]) if data.get(field) not in (None, '') else None
        tree_block = TreeBlock.objects.create(
            name=data['name'],
            apn=data.get('apn', ''),
            variety=data['variety'],
            bud=data.get('bud', ''),
            rootstock=data.get('rootstock', ''),
            year_planted=int(data['year_planted']),
            lat1=float(data['lat1']), lon1=float(data['lon1']),
            lat2=float(data['lat2']), lon2=float(data['lon2']),
            lat3=float(data['lat3']), lon3=float(data['lon3']),
            lat4=float(data['lat4']), lon4=float(data['lon4']),
            lat5=optional_point('lat5'), lon5=optional_point('lon5'),
            lat6=optional_point('lat6'), lon6=optional_point('lon6'),
        )
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid field values'}, status=400)

    return JsonResponse({
        'id': tree_block.id,
        'name': tree_block.name,
        'apn': tree_block.apn,
        'variety': tree_block.variety,
        'bud': tree_block.bud,
        'rootstock': tree_block.rootstock,
        'year_planted': tree_block.year_planted,
        'coordinates': [list(point) for point in tree_block.coordinates],
    })


@csrf_exempt
def tree_block_detail(request, pk):
    tree_block = get_object_or_404(TreeBlock, pk=pk)

    coordinates = [list(point) for point in tree_block.coordinates]
    centroid = [
        sum(point[0] for point in coordinates) / len(coordinates),
        sum(point[1] for point in coordinates) / len(coordinates),
    ]

    block_name = (tree_block.name or '').strip().lower()
    production_records = [
        record for record in _load_production_records()
        if (record.ranch or '').strip().lower() == block_name
    ]

    return render(request, 'divert/tree_block_detail.html', {
        'tree_block': tree_block,
        'coordinates_json': coordinates,
        'centroid_json': centroid,
        'production_records': production_records,
    })


@csrf_exempt
def delete_tree_block(request, pk):
    tree_block = get_object_or_404(TreeBlock, pk=pk)

    if request.method == "POST":
        tree_block.delete()
        return redirect('map_farm')

    return redirect('tree_block_detail', pk=pk)


@csrf_exempt
def delete_geo_point(request, location_id):
    location = get_object_or_404(GeoPoint, id=location_id)

    if request.method == "POST":
        
        location.delete()
        return redirect('index')  # Replace 'map' with your map view name

    return render(request, 'divert/location_point', {'location': location})