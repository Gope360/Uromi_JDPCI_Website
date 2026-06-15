from django.views.generic import *
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator


class HomePageView(TemplateView):
    template_name = 'Events/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscription_form'] = SubscriptionForm()  # Subscription form
        return context

    def post(self, request, *args, **kwargs):
        form_type = request.POST.get('form_type')

        # Handling subscription form submission
        if form_type == 'subscription_form':
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                subscription_form.save()
                messages.success(request, "You have successfully subscribed to our newsletter!")
                return redirect('home')  # Refresh the page with success message
            else:
                context = self.get_context_data()
                context['subscription_form'] = subscription_form
                return self.render_to_response(context)

        context = self.get_context_data()
        return self.render_to_response(context)
        

class NewsletterView(ListView):
    model = Newsletter
    template_name = 'Events/newsletter.html'  # Adjust as needed
    context_object_name = 'newsletters'
    paginate_by = 9  # Show 9 newsletters per page, as per your requirements
    ordering = ['-date']

class NewsletterDetailView(DetailView):
    model = Newsletter
    template_name = 'Events/newsletter-details.html'
    context_object_name = 'newsletter'

# class NewsletterDetailView(DetailView):
#     model = Newsletter
#     template_name = 'Events/newsletter-details.html'  # Ensure this template exists
#     context_object_name = 'newsletter'

class TeamView(TemplateView):
    template_name = "Events/teams.html"

class FaqsView(TemplateView):
    template_name = "Events/faqs.html"

class AboutView(TemplateView):
    template_name = "Events/about.html"

class ContactView(TemplateView):
    template_name = "Events/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MessageForm()
        return context

    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            # Add a success message
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # Redirect to the same page to prevent resubmission on refresh
        return render(request, self.template_name, {'form': form})

class DonationView(TemplateView):
    template_name = "Events/donation.html"

class EventPageView(TemplateView):
    template_name = 'Events/events.html'
    def get_context_data(self, **kwargs):
        # Get the current date and time
        current_time = timezone.now()
        # Categorize events based on the date
        context = super().get_context_data(**kwargs)
        context['upcoming_events'] = Event.objects.filter(start_date__gt=current_time).order_by('start_date')
        context['active_events'] = Event.objects.filter(start_date__lte=current_time, end_date__gte=current_time).order_by('start_date')
        recent_events = Event.objects.filter(end_date__lt=current_time).order_by('-end_date')
        paginator = Paginator(recent_events, 10)  # Show 10 events per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

        return context

class ProgramListView(ListView):
    model = Program
    template_name = 'Events/programs.html'
    context_object_name = 'programs'

class ProgramDetailView(DetailView):
    model = Program
    template_name = 'Events/program_detail.html'
    context_object_name = 'program'
    slug_field = 'slug'  # By default, DetailView uses `pk`, so we need to specify the slug field
    slug_url_kwarg = 'slug'  # The keyword argument in the URL


class TestimonialFormView(TemplateView):
    template_name = "Events/testimonial-form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonial_form'] = TestimonialForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your testimonial has been submitted successfully!")
            context = self.get_context_data()
            return render(request, self.template_name, context)
        else:
            messages.error(request, "There was an error in your submission. Please check the form for errors.")
            context = self.get_context_data()
            context['testimonial_form'] = form
            return render(request, self.template_name, context)

class TestimonialListView(ListView):
    model = Testimonial
    template_name = 'Events/testimonial.html'  # Adjust this path to your actual template
    context_object_name = 'testimonials'  # The variable name used in the template

    def get_queryset(self):
        return Testimonial.objects.all().order_by('-id')

class EventVolunteerApplicationView(CreateView):
    model = EventVolunteerApplication
    form_class = EventVolunteerApplicationForm
    template_name = 'Events/volunteer_application.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your application has been submitted successfully!")
        return self.render_to_response(self.get_context_data())

    def form_invalid(self, form):
        messages.error(self.request, "There was an error in your submission. Please check the form for errors.")
        return self.render_to_response(self.get_context_data(form=form))
    
class ArticleListView(ListView):
    model = Article
    template_name = 'Events/article.html'
    paginate_by = 6  # Number of articles per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Return all articles ordered by the most recent date
        context['articles'] = Article.objects.all().order_by('-date')
        # 1. Most recent article (single article)
        context['most_recent_article'] = Article.objects.all().order_by('-date').first()
        # 2. Top 6 most viewed articles
        context['most_viewed_articles'] = Article.objects.all().order_by('-views')[:6]

        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'Events/article_detail.html'

    def get_object(self):
        return get_object_or_404(Article, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        # Increment the view count
        article.views += 1
        article.save()

        # Get the previous and next articles based on their IDs
        context['previous_article'] = Article.objects.filter(id__lt=article.id).order_by('-id').first()
        context['next_article'] = Article.objects.filter(id__gt=article.id).order_by('id').first()

        return context
