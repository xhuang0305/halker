from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import F
import markdown
from django.utils.html import strip_tags
from markdownx.models import MarkdownxField
from model_utils.models import TimeStampedModel
from model_utils import FieldTracker

User = get_user_model()

# Create your models here.
class Category(models.Model):
    """
    文章的分类
    """
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    """
    标签
    """
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name
    
class Post(TimeStampedModel):
    """
    文章
    """
    # 文章标题
    title = models.CharField(max_length = 70)
    # 文章正文
    body = MarkdownxField()
    # 文章摘要
    excerpt = models.CharField(max_length = 200, blank = True)
    # 分类
    category = models.ForeignKey(Category)
    # 标签
    tags = models.ManyToManyField(Tag, blank = True)
    # 作者
    author = models.ForeignKey(User)
    # 阅读量
    views = models.PositiveIntegerField(default=0)
    # 检查字段变化
    tracker = FieldTracker()
    
    def save(self, *args, **kwargs):
        if self.tracker.has_changed('body'):
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args, **kwargs)
    
    def increase_views(self):
        self.views = F('views') + 1
        self.save(update_fields=['views'])
        self.refresh_from_db(fields=['views'])
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-created']
