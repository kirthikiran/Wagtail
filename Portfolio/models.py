from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.search import index




class PortfolioPage(Page):
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    date = models.DateField(blank=True, null=True)
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

   
    
    def main_images(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('main_image'),
        FieldPanel('intro'),
        FieldPanel('body', classname='full'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]


class PortfolioPageGalleryImage(Orderable):
    page = ParentalKey(PortfolioPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

class PortfolioIndexPage(Page):
    intro = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    @property
    def portfolios(self):
        # Get list of live Portfolio pages that are descendants of this page
        portfolios = PortfolioPage.objects.live().descendant_of(self)

        # Order by most recent date first
        portfolios = portfolios.order_by('date')

        return portfolios

    def get_recent_portfolios(self):
        max_count = 3 # max count for displaying post
        return PortfolioPage.objects.all().order_by('-first_published_at')[:max_count]

    def get_context(self, request):
        # Get portfolios
        portfolios = self.portfolios

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            portfolios = portfolios.filter(tags__name=tag)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(portfolios, 8)  # Show 5 portfolios per page
        try:
            portfolios = paginator.page(page)
        except PageNotAnInteger:
            portfolios = paginator.page(1)
        except EmptyPage:
            portfolios = paginator.page(paginator.num_pages)

        # Update template context
        context = super(PortfolioIndexPage, self).get_context(request)
        context['portfolios'] = portfolios
        context['recents'] = self.get_recent_portfolios()
  
        
        return context

    def get_sitemap_urls(self):
        return [
            {
                'location': self.full_url,
                'lastmod': self.latest_revision_created_at,
                'changefreq': 'monthly',
                'priority': .5
            }
        ]
        
PortfolioIndexPage.content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full"),
     
    ]

PortfolioIndexPage.promote_panels = Page.promote_panels

