from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from multiselectfield import MultiSelectField
from ckeditor.fields import RichTextField
import math
    

class Program(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='programs/')
    slug = models.SlugField(unique=True, blank=True, null=True)  # The slug field for the URL

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Automatically generate the slug from the title
        super(Program, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('program_detail', kwargs={'slug': self.slug})

class Article(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    brief = models.CharField(max_length=300)  # New brief field
    content = RichTextField()  # Use CKEditor RichTextField for the content
    image = models.ImageField(upload_to='article/')
    slug = models.SlugField(unique=True)  # Added slug field
    author = models.CharField(max_length=100)  # Author name entered manually
    views = models.IntegerField(default=0)  # Track views
    author_profile_picture = models.ImageField(upload_to='author_pics/', null=True, blank=True)  # Author profile picture


    def get_read_time(self):
        words_per_minute = 200  # Average reading speed
        content_words = len(self.content.split())
        read_time_minutes = content_words / words_per_minute
        return math.ceil(read_time_minutes) 

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name} - {self.subject}'

class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField()  # The actual testimonial
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledgment = models.BooleanField(default=False)  # Added acknowledgment field

    def __str__(self):
        return f"Testimonial by {self.name}"
    
class Gallery(models.Model):
    month = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.month

class Image(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='images', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class ThematicArea(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class Newsletter(models.Model):
    title = models.CharField(max_length=60)
    brief = models.TextField()
    volume = models.IntegerField()
    number = models.IntegerField()
    edition = models.CharField(max_length=60)
    date = models.DateField(auto_now_add=True) 
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    image = models.ImageField(upload_to='newsletter-images/', blank=True, null=True)
    newsletter = models.FileField(upload_to='newsletters/', max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('newsletter_detail', kwargs={'slug': self.slug})

    def get_download_url(self):
        return self.newsletter.url  # Returns the URL of the uploaded PDF

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='events/')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title

class EventVolunteerApplication(models.Model):
    # VOLUNTEER'S GENERAL INFORMATION
    name = models.CharField(max_length=255)  # Name
    date_of_birth = models.DateField()  # Date of Birth
    gender = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female')])  # Gender
    address = models.TextField()  # Address
    phone_number = models.CharField(max_length=15)  # Phone Number(s)
    email = models.EmailField()  # Email Address
    preferred_contact_method = models.CharField(max_length=10, choices=[('Phone', 'Phone'), ('Email', 'Email')])  # Preferred Method of Contact

    # EMERGENCY CONTACT
    emergency_contact_name = models.CharField(max_length=255)  # Name of Emergency Contact
    emergency_contact_relationship = models.CharField(max_length=255)  # Relationship
    emergency_contact_phone = models.CharField(max_length=15)  # Emergency Contact Phone

    AREAS_OF_INTEREST_CHOICES = [
        ('SGBV/CEFM', 'SGBV/CEFM'),
        ('Legal and Correctional Centre Apostolate', 'Legal and Correctional Centre Apostolate'),
        ('Micro Credit', 'Micro Credit'),
        ('Environment and Climate Change', 'Environment and Climate Change'),
        ('Human Rights', 'Human Rights'),
        ('Livelihood Support', 'Livelihood Support'),
        ('Health', 'Health'),
        ('Good Governance', 'Good Governance'),
    ]

    areas_of_interest = MultiSelectField(
        choices=AREAS_OF_INTEREST_CHOICES,
        max_length=255
    )

    # ABOUT THE VOLUNTEER
    have_volunteered_before = models.TextField(blank=True, null=True)  # Previous volunteer experience
    why_interested_in_volunteering = models.TextField()  # Why are you interested in volunteering
    volunteer_position_preferences = models.TextField()  # List of volunteer position preferences
    available_hours_days = models.CharField(max_length=255)  # Availability for volunteer work
    relevant_training_experience_skills = models.TextField()  # Related training or skills
    affiliated_organizations = models.TextField(blank=True, null=True)  # Community organizations or clubs affiliation
    current_employer = models.CharField(max_length=255, blank=True, null=True)  # Current employer
    highest_education_level = models.CharField(max_length=255, blank=True, null=True)  # Highest level of education
    prior_criminal_convictions = models.TextField(blank=True, null=True)  # Prior criminal convictions or offenses


    # PHYSICAL LIMITATIONS
    physical_limitations = models.TextField(blank=True, null=True)  # Physical limitations

    # REFERENCES
    reference_one_name = models.CharField(max_length=255)  # Reference 1 Name
    reference_one_phone = models.CharField(max_length=15)  # Reference 1 Phone
    reference_one_relationship = models.CharField(max_length=255)  # Reference 1 Relationship
    reference_two_name = models.CharField(max_length=255)  # Reference 2 Name
    reference_two_phone = models.CharField(max_length=15)  # Reference 2 Phone
    reference_two_relationship = models.CharField(max_length=255)  # Reference 2 Relationship

    # MISCELLANEOUS
    t_shirt_size = models.CharField(max_length=10)  # T-Shirt size
    how_heard_about_us = models.TextField()  # How did you hear about us

    # Acknowledgment
    acknowledgment = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)  # Timestamp for submission

    def __str__(self):
        return self.name