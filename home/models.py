from __future__ import absolute_import, unicode_literals

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.core.blocks import URLBlock, DateBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.search import index
from blog.models import BlogPage





class HomePage(Page):
    """Home page model."""

    templates = "home/home_page.html"

    body = RichTextField(blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
    
    def blogs(self):
        # Get list of live blog pages that are descendants of the ResourceIndexPage page
    
        # Order by most recent date first
        blogs = BlogPage.objects.all().order_by('-date')[:3]

        return blogs

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['blogs'] = self.blogs()
        return context
            
    
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]
    
    content_panels = Page.content_panels + [
     
        FieldPanel('body'),
       
    ]

class About(Page):
    """About model."""

    templates = "home/about.html"

    body = RichTextField(blank=True)

    def blogs(self):
        # Get list of live blog pages that are descendants of the ResourceIndexPage page
    
        # Order by most recent date first
        blogs = BlogPage.objects.all().order_by('-date')[:3]

        return blogs

    def get_context(self, request):
        context = super(About, self).get_context(request)
        context['blogs'] = self.blogs()
        return context
            
    
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]
    
    content_panels = Page.content_panels + [
     
        FieldPanel('body'),
       
    ]
    



        

