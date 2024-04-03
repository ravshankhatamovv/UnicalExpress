from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType

from .models import Product, Category, ProductImage, Shop

class ProductPriceListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just next the filter options.
    title = _("price filter")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "price"

    def lookups(self, request, model_admin):
        return [
            ("0-10", _("0-10")),
            ("10-20", _("10-20")),
            ("20-30", _("20-30")),
            ("30-40", _("30-40")),
            ("40-50", _("40-50")),
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '0-10' or '10-20' etc.)
        # to decide how to filter the queryset.
        if self.value() == "0-10":
            return queryset.filter(
                price__gte=0,
                price__lte=10,
            )
        if self.value() == "10-20":
            return queryset.filter(
                price__gte=10,
                price__lte=20,
            )
        if self.value() == "20-30":
            return queryset.filter(
                price__gte=20,
                price__lte=30,
            )
        if self.value() == "30-40":
            return queryset.filter(
                price__gte=30,
                price__lte=40,
            )
        if self.value() == "40-50":
            return queryset.filter(
                price__gte=40,
                price__lte=50,
            )


class ProductInline(admin.TabularInline):
    """
    makes a way to access to product through category panel
    """
    model=Product.category.through
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    provide easy-readable layout at Product panel with various features
    """
    list_display = ["title", "amount", "price","photo"]
    search_fields = ('title','id')
    list_filter = ["active",ProductPriceListFilter]
    ordering = ('price',)
    readonly_fields = ['photo']

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """
    provide easy-readable layout at Shop panel with various features
    """
    list_display=["title","photo"]
    readonly_fields = ['photo']
    search_fields = ('title',)
    

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    provide easy-readable layout at ProductImage panel with various features
    """
    readonly_fields = ['img_preview']
    list_display = ['image_name', 'img_preview']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    provide easy-readable layout at Category panel with various features 
    """
    list_display_links=("title",)
    list_display=["title", "parents"]
    search_fields=("title","id", "product_category__id","product_category__title")
    inlines=[
        ProductInline,
    ]



class MyAdminSite(admin.AdminSite):
    """
    this class for responsible for site header.There is Demo project set fot it
    """
    site_header = "Demo Project"


admin_site = MyAdminSite(name="admin")


