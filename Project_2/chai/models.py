from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 

class ChaiVariety(models.Model):
    CHAI_TYPE_CHOICE=[
        ('ML','MASALA'),
        ('GR','GINGER'),
        ('KL','KIWI'),
        ('PL','PLAIN'),
        ('EL','ELAICHI'),
    ]
    name= models.CharField(max_length=100)
    image= models.ImageField(upload_to='chais/')
    date_addded=models.DateTimeField(default=timezone.now)
    type=models.CharField(max_length=2,choices=CHAI_TYPE_CHOICE)
    ingredients = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    reviewrating = models.FloatField(default=0.0) 
    description= models.CharField(default= "no description yet")

    def __str__(self):
        return self.name

class ChaiReview(models.Model):
    chai = models.ForeignKey(ChaiVariety, on_delete=models.CASCADE, related_name='reviews')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        default=5
    )
    comment=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.chai.name} ({self.rating})"

