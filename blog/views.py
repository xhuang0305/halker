from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from comments.forms import CommentForm
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
# Create your views here.
# 首页
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        
        context.update(pagination_data)
        return context
    
    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        
        left = right = []
        left_has_more = right_has_more = False
        first = last = False
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range
        if page_number == 1:
            right = page_range[page_number:page_number+2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number-3) > 0 else 0:page_number-1]
            
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]
            
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
                
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        
        context = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return context
    
# 博客详情页
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    
    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response
    
    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset = None)
        md = markdown.Markdown([
                            'markdown.extensions.extra',
                            'markdown.extensions.codehilite',
                            TocExtension(slugify=slugify)
                          ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post
    
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context
    
# 归档页面
class ArchivesView(IndexView):
    
    def get_queryset(self):
        return super(ArchivesView, self).get_queryset().filter(created__year = self.kwargs.get('year'),
                                                               created__month = self.kwargs.get('month'))
# 分类页面
class CategoryView(IndexView):
    
    def get_queryset(self):
        cate = get_object_or_404(Category, pk = self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
# 搜索
class SearchView(IndexView):
    
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        if not q:
            return render(request, 'blog/index.html', {'error_msg': '请输入关键字'})
            
        return IndexView.get(self, request, *args, **kwargs)
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        return super(SearchView, self).get_queryset().filter(Q(title__icontains = q) | Q(body__icontains = q))

# 标签页面   
class TagView(IndexView):
    
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk = self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)