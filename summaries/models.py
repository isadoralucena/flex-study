from django.db import models
from django.contrib.auth.models import User

class Summary(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='summaries')

    def __str__(self):
        return self.title
    
class SummaryViews(models.Model):
    ip = models.GenericIPAddressField()
    summary = models.ForeignKey(Summary, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.ip