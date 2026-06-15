from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path(
        '20th-anniversary',
        TemplateView.as_view(template_name='20th-anniversary.html'),
        name='20th-anniversary'
    ),
    path('about-us', AboutView.as_view(), name="about"),
    path('newsletters', NewsletterView.as_view(), name='newsletter'),
    path('newsletter/<slug:slug>/', NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('teams', TeamView.as_view(), name="teams"),
    path('events', EventPageView.as_view(), name="events"),
    path('programs/', ProgramListView.as_view(), name='programs'),
    path('programs/<slug:slug>/', ProgramDetailView.as_view(), name='program_detail'),
    path('volunteer/apply/', EventVolunteerApplicationView.as_view(), name='volunteer-apply'),
    path('volunteer/success/', TemplateView.as_view(template_name='success.html'), name='volunteer-success'),
    path('contact', ContactView.as_view(), name="contact"),
    path('support-us', DonationView.as_view(), name="donation"),
    path('testimonial-form', TestimonialFormView.as_view(), name="testimonial"),
    path('testimonials/', TestimonialListView.as_view(), name='testimonial'),
    path('articles/', ArticleListView.as_view(), name='article'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('faqs', FaqsView.as_view(), name="faqs"),
]
