'''
Created on 2017年6月21日

@author: huangxing
'''
from django.contrib.syndication.views import Feed

from .models import Post

class AllPostsRssFeed(Feed):
    
    title = 'halker的个人技术博客'
    
    link = '/'
    
    description = 'halker的所有博客'
    
    def items(self):
        return Post.objects.all()
    
    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)
    
    def item_description(self, item):
        return item.body