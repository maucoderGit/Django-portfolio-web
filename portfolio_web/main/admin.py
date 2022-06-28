from django.contrib import admin

from main.models import Project, Tag

# Register your models here.

class TagInline(admin.TabularInline):
    model = Project.tag_set.through
#    formset= AtLeastOneRequiredInlineFormSet
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    inlines = [TagInline, ]
    fields = ['title', 'headline', 'pub_date', 'content_text']
    list_display = ('title', 'headline', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields: list = ['title', 'headline']

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.save()

admin.site.register(Project, ProjectAdmin)
admin.site.register(Tag)