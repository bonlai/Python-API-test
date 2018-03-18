from background_task import background
from API.recommendation import *
import googlemaps

@background(schedule=1)
def autoClustering():
    u=UserClustering()
    u.clustering()

@background(schedule=1)
def calDistanceRate():
    gmaps = googlemaps.Client(key='AIzaSyBUcE5kC4G6NL0hb8VjqFOAsZLGaQoWO7Q')  
    for requestUser in User.objects.all():
        if (requestUser.profile.latitude!=None):
            for gathering in Gathering.objects.all():
                origins = (requestUser.profile.latitude, requestUser.profile.longitude)
                distance = gmaps.distance_matrix(origins,gathering.restaurant.address)
                result=distance.get('rows')[0].get('elements')[0].get('duration')
                if (result!=None):
                    distance_rate=result.get('value')
                    print(requestUser.id,gathering.id,distance_rate)
                    obj, created = RecommendedRate.objects.update_or_create(
                        gathering=gathering, user=requestUser,
                        defaults={'distance_rate': distance_rate}
                    )

@background(schedule=1)
def slopeOneCal():
    s=SlopeOne()
    for requestUser in User.objects.all():
        for gathering in Gathering.objects.all():
            requestRestaurant=gathering.restaurant

            value=s.predict(requestUser.id,requestRestaurant.id) 
            
            obj, created = RecommendedRate.objects.update_or_create(
                    gathering=gathering, user=requestUser,
                    defaults={'restaurant_rate':value}
            )

calDistanceRate(repeat=60)
autoClustering(repeat=43200)
slopeOneCal(repeat=60)