from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from .forms import PostForm
from .models import Post


def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        print("*************************** POST")
        print(form)
        print(form.errors)
        if form.is_valid():
            print("*************************** VALID")
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            print(post)
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
