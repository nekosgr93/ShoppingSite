from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from products.models import Product
from django.shortcuts import render
from django.contrib.auth.models import User

class Welcome(TemplateView):
    template_name = 'welcome.html'



class Index(TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.all()
        product_list = []
        for user in users:
            product_list.extend(Product.objects.filter(user=user))
        context['products'] = product_list
        return context

def product_query(request):
    ext_query_string = slugify(request.GET.get('query'))
    contain_query_string = request.GET.get('query')
    if contain_query_string:
        contain_query_string = contain_query_string.split()
    query_result = []

    ext_query = Product.objects.filter(slug=ext_query_string)
    if ext_query and ext_query:
        # print(ext_query)
        query_result.extend(ext_query)

    for string in contain_query_string:
        contain_query = Product.objects.filter(slug__icontains=string)
        # print(contain_query)
        check_list = contain_query_check(query_result, contain_query)
        query_result.extend(check_list)
        print(query_result)
    return render(request, 'query_result.html', {'query_result': query_result})


def contain_query_check(query_result, query_list):
    slug_list = []
    check = []
    for item in query_result:
        slug_list.append(item.slug)
    for query in query_list:
        if query.slug not in slug_list:
            check.append(query)
    return check
