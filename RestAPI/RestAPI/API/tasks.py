from background_task import background
from API.recommendation import *


@background(schedule=1)
def autoClustering():
    u=UserClustering()
    u.clustering()

autoClustering(repeat=43200)