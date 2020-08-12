import django_filters
from django_filters import DateFilter, CharFilter

from .models import *


class OrderFilter(django_filters.FilterSet):
	note = CharFilter(lookup_expr='icontains')

	class Meta:
		model = Order
		fields = ['product', 'product__category', 'status']
		exclude = ['customer', 'date_created']


# Strange way to customize the filter label without 
# directly defining the filter in the class
OrderFilter.base_filters['product__category'].label = 'Category'
