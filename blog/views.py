from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 5
	template_name = 'blog/post/list.html'

def post_list(request):
	object_list = Post.published.all()
	paginator = Paginator(object_list, 5)	# Pięć postów na każdej stronie
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# Jeżeli zmienna page nie jest liczbą całkowitą, wówczas pobieramy pierwszą stronę wyników.
		posts = paginator.page(1)
	except EmptyPage:
		# Jeżeli page ma wartość większą niż numer ostatniej ze stron, to pobierana jest ostatnia strona.
		posts = paginator.page(paginator.num_pages)
	return render(request, 'blog/post/list.html', {'page':page, 'posts': posts})

def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
	return render(request, 'blog/post/detail.html', {'post': post})
