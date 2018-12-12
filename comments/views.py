from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import Comment_form
from .models import Comments
from products.models import Product


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


@login_required
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
