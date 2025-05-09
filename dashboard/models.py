from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):              # for direct show the title name in database 
        return self.title

    class Meta:                     # for this class remove the extra s in admion table before:Notess after:Notes
       verbose_name = "notes"
       verbose_name_plural = "notes"   


#============================================ COMPLETE FOR NOTES =====================================================================================  


class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):              # for direct show the title name in database 
        return self.subject
    
#============================================ COMPLETE FOR HOMEWORK =====================================================================================  


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)

    def __str__(self):              # for direct show the title name in database 
        return self.title
    
    class Meta:                     # for this class remove the extra s in admion table before:Notess after:Notes
       verbose_name = "Todo"
       verbose_name_plural = "Todo"