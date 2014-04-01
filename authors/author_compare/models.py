from django.db import models

# Create your models here.
class Author(models.Model):
    author = models.CharField(max_length=50)
    dic_stopwords = models.FileField(upload_to='pickle')
    dic_clean = models.FileField(upload_to='pickle')
    num_words = models.IntegerField(default=0)
    avg_words = models.FileField(upload_to='pickle')
    var_words = models.FileField(upload_to='pickle')
    var_sen = models.FileField(upload_to='pickle')
    bigram_clean = models.FileField(upload_to='pickle')
    bigram = models.FileField(upload_to='pickle')
    trigram_clean = models.FileField(upload_to='pickle')
    pic = models.FileField(upload_to='pictures',null=True, blank=True )
    def __unicode__(self):
        return self.author
