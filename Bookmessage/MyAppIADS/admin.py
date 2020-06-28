from django.contrib import admin
from .models import Publisher, Book, Member, Order, Review


class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'category', 'publisher'), ('num_pages', 'price', 'num_reviews')]
    list_display = ('title', 'category', 'price')
    actions = ['update_price']

    def update_price(self, request, queryset):
        for product in queryset:
            product.price = product.price + 10
            product.save()
        self.message_user(request, "Successfully Updated Book prices")
    update_price.short_description = "Increase Book price by 10 "


class OrderAdmin(admin.ModelAdmin):
    fields = ['books', ('member', 'order_type', 'order_date')]
    list_display = ('pk', 'member', 'order_type', 'order_date', 'total_items')


class PublisherAdmin(admin.ModelAdmin):
    fields = ['name', ('website', 'city', 'country',)]
    list_display = ('name', 'website', 'city')


class MemberAdmin(admin.ModelAdmin):
    fields =[('first_name', 'last_name', 'status', 'image'), ('address', 'city', 'province', ), ('last_renewal', 'auto_renew',
                                                                                        'borrowed_books')]
    list_display = ('first_name', 'last_name', 'status', 'get_borrowed_books', 'image_tag')

    def get_borrowed_books(self, obj):
        return [str(p) for p in obj.borrowed_books.all()]

#admin.site.register(Publisher)
# admin.site.register(Book)
#admin.site.register(Member)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
admin.site.register(Book, BookAdmin)
admin.site.register(Member, MemberAdmin)