from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# class Profile(models.Model):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)
# 	image = models.ImageField(default='default.jpg', upload_to='profile_pics')

# 	def __str__(self):
# 		return f'{self.user.username} Profile'

# 	def save(self, *args, **kwargs):
# 		# First we call the parent class's save method
# 		super().save(*args, **kwargs)
# 		# Open the image of the current instance
# 		img = Image.open(self.image.path)

# 		# Check to see if image is larger than 300 pixels
# 		if img.height > 300 or img.width > 300:
# 			# Set max output size
# 			output_size = (300, 300)
# 			# Resize image to output size
# 			img.thumbnail(output_size)
# 			# Save resized image to same path to overwrite it
# 			img.save(self.image.path)


class Customer(models.Model):
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=20, null=True)
	email = models.EmailField(max_length=255, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name


# class Tag(models.Model):
# 	name = models.CharField(max_length=100, null=True)

# 	def __str__(self):
# 		return self.name


class Product(models.Model):
	CATEGORY = (
			('Indoor', 'Indoor'),
			('Outdoor', 'Outdoor'),
			)
	name = models.CharField(max_length=200, null=True)
	price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=255, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	# tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name


class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=1000, blank=True, null=True)

	def __str__(self):
		return self.customer.name + ": " + self.product.name

