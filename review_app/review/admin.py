from django.contrib import admin
from review.models import Review,Product,Category,ReviewReaction

# Register your models here.

admin.site.register(Review)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ReviewReaction)
