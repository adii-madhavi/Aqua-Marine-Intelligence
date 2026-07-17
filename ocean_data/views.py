import json
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import MarineRecord, SpeciesGrowthCondition

# --- Page Views ---
def landing(request):
    """Renders the project landing page."""
    return render(request, 'landing.html')

def home(request):
    """Renders the main monitoring dashboard."""
    return render(request, 'home.html')

# --- Authentication APIs ---
def signup_api(request):
    """Handles new user registration."""
    if request.method == "POST":
        data = json.loads(request.body)
        if not User.objects.filter(username=data.get('username')).exists():
            User.objects.create_user(
                username=data.get('username'), 
                password=data.get('password'), 
                email=data.get('email')
            )
            return JsonResponse({"message": "User created successfully!"})
        return JsonResponse({"message": "User already exists"}, status=400)

def login_api(request):
    """Handles user authentication."""
    if request.method == "POST":
        data = json.loads(request.body)
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user:
            login(request, user)
            return JsonResponse({"message": "Login successful!"})
        return JsonResponse({"message": "Invalid credentials"}, status=401)

def logout_api(request):
    """Safely logs out the user."""
    logout(request)
    return JsonResponse({"message": "Logged out successfully!"})

# --- Species & Recommendation APIs ---
def species_api(request):
    """Returns the full master dataset for all species."""
    species = SpeciesGrowthCondition.objects.all()
    data = [{
        "name": s.species_name, 
        "description": s.description,
        "min_temp": s.min_temp, 
        "max_temp": s.max_temp,
        "salinity": s.salinity_ppt,
        "ph": s.ideal_ph
    } for s in species]
    return JsonResponse(data, safe=False)

def recommend_species_api(request):
    """Filters species based on the requested +/- 2 degree interval."""
    try:
        curr_t = float(request.GET.get('temp', 0))
        curr_s = float(request.GET.get('salinity', 0))
        
        # Matches species within 2 degrees and 5 ppt salinity
        matches = SpeciesGrowthCondition.objects.filter(
            min_temp__lte=curr_t + 2,
            max_temp__gte=curr_t - 2,
            salinity_ppt__gte=curr_s - 5,
            salinity_ppt__lte=curr_s + 5
        )
        data = [{"name": s.species_name, "desc": s.description, "ph": s.ideal_ph} for s in matches]
        return JsonResponse(data, safe=False)
    except (ValueError, TypeError):
        return JsonResponse([], safe=False)

def search_water_body(request):
    """Allows searching the master database by name."""
    name_query = request.GET.get('name', '').lower()
    species = SpeciesGrowthCondition.objects.filter(species_name__icontains=name_query)
    data = [{"name": s.species_name, "desc": s.description} for s in species]
    return JsonResponse(data, safe=False)

# --- Environmental Data APIs ---
def add_record_api(request):
    """Saves coastal logs with correct Latitude and Longitude."""
    if request.method == 'POST':
        data = json.loads(request.body)
        
        loc = data.get('location')
        temp = float(data.get('temperature', 0))
        salt = float(data.get('salinity', 0))
        
        # Pulls actual coordinates from frontend to fix the Map API
        # Uses default Mumbai coordinates if input is missing
        lat = data.get('lat', 19.0760) 
        lng = data.get('lng', 72.8777)

        # Status check logic
        status_str = "DANGER" if temp > 30 or salt > 40 else "SAFE"
        
        MarineRecord.objects.create(
            location=loc,
            temperature=temp,
            salinity=salt,
            latitude=lat,
            longitude=lng,
            status=status_str
        )
        return JsonResponse({"message": "Record saved successfully at correct location!"})

def get_all_records(request):
    """Fetches all history logs for the table and map markers."""
    records = list(MarineRecord.objects.all().order_by('-date_added').values())
    return JsonResponse(records, safe=False)