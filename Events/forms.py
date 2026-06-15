from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name', 'id': 'name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email', 'id': 'email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject', 'id': 'subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Leave a message here', 'id': 'message', 'style': 'height: 150px;'}),
        }

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control border-primary rounded-pill w-100 py-3 ps-4 pe-5',
                'placeholder': 'Your email',
                'style': 'height: 55px;',
            }),
        }

class TestimonialForm(forms.ModelForm):
    acknowledgment = forms.BooleanField(
        required=True,
        label=(
            "I certify that the information I have provided is true to the best of my knowledge, "
            "and I give my consent for this testimonial to be published on the website."
        ),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Testimonial
        fields = ['name', 'profession', 'text', 'image', 'acknowledgment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'profession': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Profession'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Testimonial'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class EventVolunteerApplicationForm(forms.ModelForm):
    areas_of_interest = forms.MultipleChoiceField(
        choices=[
            ('SGBV/CEFM', 'SGBV/CEFM'),
            ('Legal and Correctional Centre Apostolate', 'Legal and Correctional Centre Apostolate'),
            ('Micro Credit', 'Micro Credit'),
            ('Environment and Climate Change', 'Environment and Climate Change'),
            ('Human Rights', 'Human Rights'),
            ('Livelihood Support', 'Livelihood Support'),
            ('Health', 'Health'),
            ('Good Governance', 'Good Governance'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Which areas of our organization would you like to volunteer in? (Check all that apply):"
    )

    def clean_areas_of_interest(self):
        data = self.cleaned_data['areas_of_interest']
        return ','.join(data) 
    
    acknowledgment = forms.BooleanField(
        required=True,
        label="I certify that the volunteer information I have provided is true to the best of my knowledge. I understand that submitting this application does not guarantee placement, as Uromi JDPCI reserves the right to select volunteers based on program needs."
    )

    class Meta:
        model = EventVolunteerApplication
        fields = [
            'name', 'date_of_birth', 'gender', 'address', 'phone_number', 
            'email', 'preferred_contact_method', 'emergency_contact_name', 
            'emergency_contact_relationship', 'emergency_contact_phone', 
            'have_volunteered_before', 'why_interested_in_volunteering', 
            'affiliated_organizations', 
            'current_employer', 'highest_education_level',
            'prior_criminal_convictions', 'available_hours_days', 
            'relevant_training_experience_skills', 'physical_limitations', 
            'reference_one_name', 'reference_one_phone', 
            'reference_one_relationship', 'reference_two_name', 
            'reference_two_phone', 'reference_two_relationship', 
            't_shirt_size', 'how_heard_about_us', 'areas_of_interest', 
            'acknowledgment'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number(s)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'preferred_contact_method': forms.Select(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency Contact Name'}),
            'emergency_contact_relationship': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Relationship'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'have_volunteered_before': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Have you volunteered before? Please describe if yes'}),
            'why_interested_in_volunteering': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Why are you interested in volunteering with this organization?'}),
            'affiliated_organizations': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Are you affiliated with any community organizations or clubs? If so, please explain.'}),
            'current_employer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Who is your current employer (if applicable)?'}),
            'highest_education_level': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What is your highest level of education?'}),
            'prior_criminal_convictions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Do you have any prior criminal convictions or offenses? If so, please describe.'}),
            'available_hours_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'How many hours and days are you available for volunteer work?'}),
            'relevant_training_experience_skills': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'What training, experience, or skills do you have that may be related to the volunteer position desired?'}),
            'physical_limitations': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Please list any physical limitations you may have'}),
            'reference_one_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reference 1 Name'}),
            'reference_one_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reference 1 Phone'}),
            'reference_one_relationship': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reference 1 Relationship'}),
            'reference_two_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reference 2 Name'}),
            'reference_two_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reference 2 Phone'}),
            'reference_two_relationship': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reference 2 Relationship'}),
            't_shirt_size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What is your T-Shirt size?'}),
            'how_heard_about_us': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'How did you hear about us?'}),
        }

class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())  # Use CKEditor for the 'content' field

    class Meta:
        model = Article
        fields = ['title', 'brief', 'content', 'image', 'author', 'slug']