import django_filters
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    # Filter by participant username
    participant = django_filters.CharFilter(method='filter_by_participant')
    # Filter by date range
    start_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['participant', 'start_date', 'end_date']

    def filter_by_participant(self, queryset, name, value):
        return queryset.filter(conversation__participants__username=value)
