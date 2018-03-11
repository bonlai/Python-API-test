from API.models import *
from sklearn.cluster import AgglomerativeClustering
import pandas as pd
import numpy as np
from django_pandas.io import read_frame

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

class UserClustering(object):
    def __init__(self):
        self.profileList=list(Profile.objects.all().order_by('user_id').values_list('user_id', flat=True))
        self.distanceMatrixLenght=len(self.profileList)
        
        qs = Profile.objects.all()
        self.profileTable = read_frame(qs,fieldnames=['user_id','dob', 'location', 'gender']).set_index('user_id')
        self.profileTable['dob']= pd.to_datetime(self.profileTable['dob'])
        
        self.interestDistanceMatrix=pd.DataFrame(index=self.profileList,columns=self.profileList)
        self.ageDistanceMatrix=pd.DataFrame(index=self.profileList,columns=self.profileList)
        self.locationDistanceMatrix=pd.DataFrame(index=self.profileList,columns=self.profileList)
        
        self.locationDifferent()
        self.interestDifferent()
        self.ageDifferent()

    @staticmethod
    def normalize(x):
        return((x - x.values.min()) / (x.values.max() - x.values.min()))

    def locationDifferent(self):      
        region=['Hong Kong Island','Hong Kong Island','Hong Kong Island','Hong Kong Island',
                'Kowloon','Kowloon','Kowloon','Kowloon','Kowloon','Kowloon',
                'New Territories','New Territories','New Territories','New Territories','New Territories','New Territories',
               'New Territories','New Territories']
        district=['Central and Western','Eastern','Southern','Wan Chai',
                  'Sham Shui Po','Kowloon City','Kwun Tong','Wong Tai Sin','Yau Tsim Mong',
                  'Islands','Kwai Tsing','North','Sai Kung','Sha Tin','Tai Po','Tsuen Wan','Tuen Mun','Yuen Long']
        districtRegionRelationship=pd.DataFrame(index=district)
        districtRegionRelationship['region']=region

        regionNameList=['Hong Kong Island','Kowloon','New Territories']
        regionDistanceMatrix=pd.DataFrame(index=regionNameList,columns=regionNameList)
        regionDistanceMatrix.iloc[0,1]=8.1
        regionDistanceMatrix.iloc[1,0]=8.1
        regionDistanceMatrix.iloc[0,2]=16.2
        regionDistanceMatrix.iloc[2,0]=16.2
        regionDistanceMatrix.iloc[1,2]=12.7
        regionDistanceMatrix.iloc[2,1]=12.7
        regionDistanceMatrix=regionDistanceMatrix.fillna(0)

        for i in range(0,self.distanceMatrixLenght-1):
            for j in range(i+1,self.distanceMatrixLenght):
                myIndex=self.profileList[i]
                otherIndex=self.profileList[j]
                myLocation=self.profileTable.loc[myIndex]['location']
                otherLocation=self.profileTable.loc[otherIndex]['location']
                myRegion=districtRegionRelationship.loc[myLocation].values[0]
                otherRegion=districtRegionRelationship.loc[otherLocation].values[0]
                self.locationDistanceMatrix.loc[myIndex,otherIndex]=regionDistanceMatrix.loc[myRegion,otherRegion]
                self.locationDistanceMatrix.loc[otherIndex,myIndex]=regionDistanceMatrix.loc[myRegion,otherRegion]

        self.locationDistanceMatrix.fillna(0, inplace=True)
        self.locationDistanceMatrix = UserClustering.normalize(self.locationDistanceMatrix)
        #print(self.locationDistanceMatrix)

    def interestDifferent(self):
        interestList=list(Interest.objects.all().order_by('id').values_list('id', flat=True))
        userInterestMatrix=pd.DataFrame(index=self.profileList,columns=interestList)

        for user in User.objects.all():
            for interest in user.enjoy.all():
                userInterestMatrix.loc[user.id][interest.id]=1
        
        userInterestMatrix.fillna(0,inplace=True)

        #calculate interest distance
        for i in range(0,self.distanceMatrixLenght-1):
            for j in range(i+1,self.distanceMatrixLenght):
                myIndex=self.profileList[i]
                otherIndex=self.profileList[j]
                temp=userInterestMatrix.loc[myIndex]-userInterestMatrix.loc[otherIndex]
                self.interestDistanceMatrix.loc[myIndex][otherIndex]=temp.abs().sum()
                self.interestDistanceMatrix.loc[otherIndex][myIndex]=temp.abs().sum()
        self.interestDistanceMatrix.fillna(0,inplace=True)
        self.interestDistanceMatrix=UserClustering.normalize(self.interestDistanceMatrix)
        #print(self.interestDistanceMatrix)

    def ageDifferent(self): 
        for i in range(0,self.distanceMatrixLenght-1):
            for j in range(i+1,self.distanceMatrixLenght):
                myIndex=self.profileList[i]
                otherIndex=self.profileList[j]
                yearDiff=abs((self.profileTable['dob'][myIndex]-self.profileTable['dob'][otherIndex]).days)/365
                self.ageDistanceMatrix.loc[myIndex][otherIndex]=yearDiff
                self.ageDistanceMatrix.loc[otherIndex][myIndex]=yearDiff
        self.ageDistanceMatrix.fillna(0,inplace=True)
        self.ageDistanceMatrix=UserClustering.normalize(self.ageDistanceMatrix)
        #print(self.ageDistanceMatrix)

    def clustering(self):
        totalDifferenceMatrix=(self.interestDistanceMatrix
                               +self.locationDistanceMatrix
                               +self.ageDistanceMatrix)/3
        clustering = AgglomerativeClustering(n_clusters=3, affinity='precomputed',linkage='average')
        clusterLabelList=clustering.fit_predict(totalDifferenceMatrix)
        for i in range(0,self.distanceMatrixLenght): 
            Profile.objects.filter(user_id=self.profileList[i]).update(cluster=clusterLabelList[i])