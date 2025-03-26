**CS50web – Capstone Project**
**Michael P. Flynn**
**12/10/2024**

**README for Divert web application:  A Map of Water Districts and Water Rights in California**


## Distinctiveness and Complexity
The web application “Divert” is a web map of water districts and water rights (diversion points) in Central California, USA.  Specifically, the counties of Fresno, Kings, and Tulare are in focus as this area ground zero for the ongoing drought and fight over water resources.  What makes this project distint from other projects in the course is the use web maps while the use of rendering geoJSON objects from an API on a Leaflet map makes the project complex.  The web map consists of geographic points representing the exact location where water is diverted from it’s natural course and shapefiles representing water districts, irrigation districts, and water storage districts.  
Water districts are accessed through an API provided by the California Department of Water Resources (DWR) located here: <https://gis.water.ca.gov/arcgis/rest/services/Boundaries/i03_WaterDistricts/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson.>  A javascript function fetches the data through the API.  A filter is constructed to render only shapefiles that contain the word “District” and exclude the other, smaller water associations such as schools or mobile home parks.  The filtered shapefiles are rendered on the map with the help of the Leaflet package.  The properties are manipulated to show the name of the district when clicked.  

Points of diversion (water rights) are stored in a csv file in the local directory.  Data for the csv file was collected from the State of California Water Resources Control Board website:  <https://waterrightsmaps.waterboards.ca.gov/viewer/index.html?viewer=eWRIMS.eWRIMS_gvh#>.  The file contains datafields for:
- Longitude
- Latitude
- Application Number
- Owner
- Face Value of water right (measured in Acre Feet), etc.

In a Django View a DictReader is used to read the file and submit it row by row into the GeoPoint Model which creates location objects.  The location objects are returned where they are rendered on the map and water rights diversion list.  

The User can click on the existing blue points on the map and exam information about the water right.  The User can also scroll the right side of the application to see all the existing water rights.  By clicking anywhere on the map other than a water district or existing water right, the borrower can claim a new water right.  The coordinates of the map click are recorded in a form for a water right submission.  Submitting the form creates a new location object which is then added to the map and list.  

## Project files:
o	Views:
- Index:  A file path to the csv file containing geolocation data of all diversion points of water rights.  A dict reader parses through the file and enters the data in the GeoPoint django model  and returns a list of locations.
- Location_point:  Returns the specific, requested location from the locations list.
- Delete_all_pods:  Deletes all locations from the list and map.
- Login_view:  user authentication
- Logout_view:  logout
- Register:  register new user
- Map_river:  Shapefiles rendered with Folium package for enhanced presentation.
- Delete_geo_point:  Deletes one location.

o	URLS:
- path("", views.index, name="index"),
- path("login", views.login_view, name="login"),
- path("logout", views.logout_view, name="logout"),
- path("register/", views.register, name="register"),
- path("<int:location_id>", views.location_point, name="location_point"),
- path('delete-all-pods/', views.delete_all_pods, name='delete_all_pods'),
- path('location/', views.location, name="location"),
- path('map_river/', views.map_river, name='map_river'),
- path('map_foo/', views.map_foo, name='map_foo'),
- path('delete_geo_point/<int:location_id>', views.delete_geo_point, name='delete_geo_point')

o	Models:  GeoPoint model creates an object that contains geographic coordinates and information about water rights.

o	CSV:  File contains 645 records of water rights locations in central California, USA. 

o	Javascript:  Javascript is contained inside the Index.html file.  It constructs a map variable with the Leaflet package.  The map is centered and zoomed over California.  A locations variable is constructed from the locations list created by the GeoPoint model.  Each location is rendered on the map via the Leaflet marker function.  A geoJSON file is rendered on the same map with Leaflet which was called from the California DWR API. 

o	CSS:  Bootstrap, Leaflet

## Run application:
1.	Pip install django, geojson, folium, django-leaflet
2.	CD hydro
3.	Python manage.py runserver
4.	Register as a new user
5.	Log in
6.	Press “Load Map Data” button to see water diversion locations
7.	Explore map
8.	Click on map.  If you receive a message “You may apply for water diversion rights here”, then complet form on the left and submit to apply for new water diversion right.
9.	Press “Load Map Data” button to see updated water diversion locations
10.	Click on link to new water diversion on the right to see more information.
11.	Click delete button to delete application.


## Additional information:
- With more time and experience I would enhance the web application by including shapefiles of rivers, streams, and lakes.
- Locations of water wells would be another layer of valuble information to display.
- Trying to host large shapefiles on the local directory proved too difficult and memory intensive.
- Connecting to shapefiles via geoJSON API is better than downloading and rendering large files.











"# taft" 
