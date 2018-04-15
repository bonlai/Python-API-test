from background_task import background
from API.recommendation import *

@background(schedule=1)
def autoClustering():
    u=UserClustering()
    u.clustering()

@background(schedule=1)
def calDistanceRate():
    c=Context()
    c.calDistanceRate()

@background(schedule=1)
def slopeOneCal():
    s=SlopeOne()
    for requestUser in User.objects.all():
        for gathering in Gathering.objects.filter(is_start=False):
            requestRestaurant=gathering.restaurant

            value=s.predict(requestUser.id,requestRestaurant.id) 
            
            obj, created = RecommendedRate.objects.update_or_create(
                    gathering=gathering, user=requestUser,
                    defaults={'restaurant_rate':value}
            )

calDistanceRate(repeat=60)
autoClustering(repeat=60)
slopeOneCal(repeat=60)