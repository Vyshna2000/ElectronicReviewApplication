from django.db import models
from django.contrib.auth.models import User

# Existing models remain unchanged...

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.brand})"

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum([r.rating for r in reviews]) / reviews.count(), 1)
        return 0

    def total_reviews(self):
        return self.reviews.count()


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.user.username} - {self.rating}★"

    def total_likes(self):
        return self.reactions.filter(reaction_type='like').count()

    def total_dislikes(self):
        return self.reactions.filter(reaction_type='dislike').count()



class ReviewReaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')
        indexes = [
            models.Index(fields=['review', 'reaction_type']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.reaction_type} - Review ID: {self.review.id}"



from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PasswordResetOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)  # ✅ required!
