from django.db import models
import datetime
from django.forms import ModelForm
from django.contrib.auth.models import User
from push_notifications.models import APNSDevice, GCMDevice

class tempUser(models.Model):
    email    = models.EmailField(max_length=100,unique=True,blank=False)
    password = models.CharField(max_length=100)
    DateTimeCreated = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
             self.DateTimeCreated = datetime.datetime.today()
        return super(tempUser, self).save(*args, **kwargs)

class Profile(models.Model):
    username  = models.EmailField(max_length=100,unique=True)
    confirmationCode = models.CharField(max_length=50)
    authToken = models.CharField(max_length=100)
 
class Team(models.Model):
    name = models.CharField(max_length=200,unique=True,primary_key=True)
    
    def __unicode__(self):
        return self.name

class LeagueType(models.Model):
     name = models.CharField(max_length=200,unique=True,primary_key=True)
     countryFlagUrl = models.ImageField(upload_to='flags/',default='flags/none/no-img.jpg')

     def __unicode__(self):
        return self.name

class League(models.Model):
     name = models.CharField(max_length=200,unique=True,primary_key=True)

     def __unicode__(self):
        return self.name
     
class PredictionDetail(models.Model):
    name = models.CharField(max_length=200)
    message = models.TextField(max_length=1000)

    def __unicode__(self):
       return self.name

class Unit(models.Model):
     value = models.CharField(max_length=200)

     def __unicode__(self):
         return self.value

class CompletedText(models.Model):
     message = models.CharField(max_length=255)
  
     def __unicode__(self):
        return self.message 

class Prediction(models.Model):
     leagueType = models.ForeignKey(LeagueType)
     league     = models.ForeignKey(League) 
     flagURL    = models.CharField(max_length=200,editable = False)
     homeTeam   = models.ForeignKey(Team,related_name = 'statusPrediction_home_team')
     awayTeam   = models.ForeignKey(Team,related_name = 'statusPrediction_away_team')
     tipDetail = models.ForeignKey(PredictionDetail)
     isPushNotifSend = models.BooleanField()
     isCompleted = models.BooleanField(default = False) 
     completedText = models.ForeignKey(CompletedText)   
     DateTimeCreated = models.DateTimeField()
     DateTimeCompleted = models.DateTimeField()
     isPredictionVerified = models.CharField(max_length=50)
     verified = models.BooleanField()
     covered = models.BooleanField()
     pending = models.BooleanField()
  
     def save(self,*args,**kwargs):
          
         self.flagURL = self.leagueType.countryFlagUrl
         if self.verified:
            self.isPredictionVerified = "Verified"
         elif self.covered:
            self.isPredictionVerified = "Covered"
         elif self.pending : 
            self.isPredictionVerified = "Pending"
         else : 
            self.isPredictionVerified = "Not-Verified"                       
	 
         if self.isPushNotifSend :
            devices =  GCMDevice.objects.filter(active = True)
            devices.send_message({"message" : "New Prediction available"})
            #appledevice = APNSDevice.objects.get(active = True)
                    
         return super(Prediction,self).save(*args,**kwargs)     
                      
          
class PurchasedPrediction(models.Model):
      userID = models.IntegerField()
      predictionID = models.IntegerField()
      DateTime = models.DateTimeField(editable = False)

      def save(self,*args,**kwargs):
          if not self.id : 
             self.DateTime = datetime.datetime.today()     
          return super(PurchasedPrediction,self).save(*args,**kwargs)

class Credit(models.Model):
       name = models.CharField(max_length=30)

       def __unicode__(self):
           return self.name

class PurchasedCredit(models.Model):
       userID = models.IntegerField()
       dateTime = models.DateTimeField(editable = False)
       credit = models.IntegerField()
       creditID = models.IntegerField()
       
       def save(self, *args, **kwargs):
           ''' On save, update timestamps '''
           if not self.id:
              self.dateTime = datetime.datetime.today()
           return super(PurchasedCredit,self).save(*args, **kwargs)

class UserCredit(models.Model):
      user = models.ForeignKey(User)
      credit = models.IntegerField()



# Create your models here.
