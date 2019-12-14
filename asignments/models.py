from django.db import models
from django.db.models.query import QuerySet
from django.dispatch import receiver
from .signalUtils import UpdateSignal
from .encrypt import encryptfile
from django.db.models.signals import post_save

# Creating a QuerySet to handel update of content
class MyModelQueryset(QuerySet):

    # defining update function to send signals on update of content
    def update(self, **kwargs):
        model_id = self[0].id
        m1 = MyModel.objects.get(id = model_id)
        # checking for filefield
        if 'myfile' in kwargs.keys():
            print('inside')
            kwargs['myencryption'] = encryptfile(kwargs['myfile'])
        # sending update signal
        UpdateSignal.send(MyModel, olderModel = m1, changedArguments = kwargs)
        print(kwargs)
        return super().update(**kwargs)

# Create your models here.
class MyModel(models.Model):

    # assigning MyModelQuerySet to MyModel
    objects = MyModelQueryset.as_manager()

    # defining the model
    myfilename = models.CharField(max_length = 200)
    myfile = models.FileField(upload_to='asignments/uploads/')
    myencryption = models.CharField(max_length = 1500)

    # defining string representation of model class
    def __str__(self):
        return self.myfilename



# creating a reciever function for UpdateSignal to store the message in output.txt
@receiver(UpdateSignal,sender = MyModel)
def onUpdateCalled(sender,**kwargs):
    # making the output
    output = "The model " + kwargs['olderModel'].myfilename + " is updated."
    
    for key in kwargs['changedArguments'].keys():
        if key == 'myfilename':
            output = output + ' The older value of myfilename is ' + kwargs['olderModel'].myfilename + " and new value is " + kwargs['changedArguments'][key]
        if key == 'myencryption':
            output = output + ' The older value of myencryption is ' + kwargs['olderModel'].myencryption + " and new value is " + kwargs['changedArguments'][key]
        if key == 'myfile':
            output = output + ' The older value of myfile is ' + kwargs['olderModel'].myfile.name + " and new value is " + kwargs['changedArguments'][key].name
    
    output = output + '\n'
    
    # saving to file
    f = open('output.txt','a')
    f.write(output)
    f.close()

# reciever function for post_save signal 
@receiver(post_save,sender = MyModel)
def onSaveCalled(sender,**kwargs):
    # making the output
    output = ""

    output = output + "The model " + kwargs['instance'].myfilename + " is created with fields myfilename = " + kwargs['instance'].myfilename + " myencryption = " + kwargs['instance'].myencryption +" and myfile = "+ kwargs['instance'].myfile.name
    output = output + "\n"

    # saving output to file
    f = open('output.txt','a')
    f.write(output)
    f.close()
