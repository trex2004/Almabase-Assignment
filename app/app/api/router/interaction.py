from django.urls import path
from app.api.viewsets.interaction import RecentInteractionsView, TopContactsView, SpamReportsView, CreateInteractionView


urlpatterns = [
    path("interactions/create", CreateInteractionView.as_view()),
    path('interactions/recent/<uuid:user_id>', RecentInteractionsView.as_view(), name='recent-interactions'),
    path('interactions/top/<uuid:user_id>', TopContactsView.as_view(), name='top-contacts'),
    path('interactions/spam', SpamReportsView.as_view(), name='spam-reports'),
]
