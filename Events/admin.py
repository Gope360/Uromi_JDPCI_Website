from django.contrib import admin
from .models import *
from django.utils.text import slugify

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'volume', 'number', 'slug')
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author')
    search_fields = ('title', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Program, ProgramAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Event)
admin.site.register(Message)
admin.site.register(Subscription)
admin.site.register(Testimonial)
admin.site.register(Gallery)
admin.site.register(Image)
admin.site.register(ThematicArea)
admin.site.register(EventVolunteerApplication)

