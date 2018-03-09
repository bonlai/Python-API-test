from API.models import *
import pandas as pd
import numpy as np

class SlopeOne(object):
    def __init__(self):
        self.init_rating_matrix()
        self.init_diff_freq_matrix()

    def init_rating_matrix(self):
        self.userIdList=list(User.objects.all().order_by('id').values_list('id', flat=True))
        self.restaurantIdList=list(Restaurant.objects.all().values_list('id', flat=True))
        #self.test="hi"
        #print(self.test)
        self.ratingMatrix = pd.DataFrame(index=self.userIdList,columns=self.restaurantIdList)
        allReviews=Review.objects.all()
        for review in allReviews:
            self.ratingMatrix.at[review.user_id,review.restaurant_id]=review.rating
        #print(self.ratingMatrix)

    def init_diff_freq_matrix(self):
        self.diffMatrix = pd.DataFrame(index=self.restaurantIdList,columns=self.restaurantIdList)
        self.freqMatrix = pd.DataFrame(index=self.restaurantIdList,columns=self.restaurantIdList)
        matrixLenght=len(self.restaurantIdList)
        for i in range(0,matrixLenght-1):
            for j in range(i+1,matrixLenght):
                ratingIndex1=self.restaurantIdList[i]
                ratingIndex2=self.restaurantIdList[j]
                temp=self.ratingMatrix[ratingIndex1].sub(self.ratingMatrix[ratingIndex2])
                count=temp.count()
                sum=temp.sum()
                if(count==0):
                    self.diffMatrix.at[ratingIndex1,ratingIndex2]=0
                    self.diffMatrix.at[ratingIndex2,ratingIndex1]=0
                else:
                    self.diffMatrix.at[ratingIndex1,ratingIndex2]=sum/count
                    self.diffMatrix.at[ratingIndex2,ratingIndex1]=-sum/count
                self.freqMatrix.at[ratingIndex1,ratingIndex2]=count
                self.freqMatrix.at[ratingIndex2,ratingIndex1]=count
        #print(self.diffMatrix)

    def predict(self,userId,restaurantId):
        if(np.isnan(self.ratingMatrix.loc[userId,restaurantId])):
            notnullindex=self.ratingMatrix.loc[userId,:].dropna().index
            length=len(notnullindex)
            ratingSum=0
            freqSum=0
            for i in range(0,length):
                ratingSum+=((self.ratingMatrix.loc[userId,notnullindex[i]]+
                            self.diffMatrix.loc[restaurantId][notnullindex[i]])*
                            self.freqMatrix.loc[restaurantId][notnullindex[i]])
                freqSum+=self.freqMatrix.loc[restaurantId][notnullindex[i]]
            if(freqSum!=0):
                return ratingSum/freqSum
            else:
                return 0
        else:
            return self.ratingMatrix.loc[userId,restaurantId]

