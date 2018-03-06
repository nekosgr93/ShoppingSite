from django.shortcuts import render, redirect, reverse, get_object_or_404
from products.models import Product
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import Comment_form
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from braces.views import SelectRelatedMixin
from .models import Comments
# Create your views here.

@login_required
def comment(request, product_id):
    if request.method == "POST" and 'add_comment' in request.POST:
        comment_form = Comment_form(request.POST)
        if comment_form.is_valid():
            form = comment_form.save(commit=False)
            product = Product.objects.get(id=product_id)
            star_rating = request.POST['star_rating']
            form.user = request.user
            form.product = product
            form.star_rating = star_rating
            form.save()
            product.total_star_rating()
            return redirect('products:product_detail', username=product.user.username, slug=product.slug)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        comment_form = Comment_form()
    return render(request, 'comments/comments_form.html', {'form': comment_form})


def edit_comment(request, id):
    comment = get_object_or_404(Comments, id=id)
    product = comment.product
    if request.method == "POST":
        form = Comment_form(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('products:product_detail', username=product.user.username, slug=product.slug)
    else:
        form = Comment_form(instance=comment)
    return render(request, 'comments/comments_form.html', {'form': form})


def remove_comment_confirm(request, id):
    comment = get_object_or_404(Comments, id=id)
    product = comment.product
    if request.method == 'POST' and comment.user == request.user:
        comment.delete()
        return redirect('products:product_detail', username=product.user.username, slug=product.slug)
    return render(request, 'comments/remove_confirm.html', {'comment': comment})




# def comment_list(request, product_id):
#     product = Product.objects.get(id=product_id)
#     list = product.comment.all()
#     return render(request, 'comments/comment_list.html', {'list': list})