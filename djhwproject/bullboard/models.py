from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def avatar_path(instance, filename):
    return 'user{0}/avatars/{1}'.format(instance.user.id, filename)

def ads_path(instance, filename):
    return 'user{0}/ads/{1}'.format(instance.author.id, filename)

class Profile(models.Model):
    """
    Модель профиля пользователя доски объявлений
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    birth_date = models.DateField('Date of birth', null=True, blank=True)
    avatar = models.ImageField(upload_to=avatar_path, default=None)
    about = models.TextField('About', max_length=500, blank=True)

    def __str__(self):
        return str(self.user.username)


class Categories(models.Model):
    """
    Категории объявлений
    """
    title = models.CharField(max_length=50)
    descr = models.TextField(max_length=100)

    def __str__(self):
        return 'Title {}, description {}'.format(self.title, self.descr)


class Ads(models.Model):
    """
    Объявления пользователя
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=75)
    description = models.TextField(max_length=500, blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    photo_ad = models.ImageField(upload_to=ads_path)
    favorites = models.ManyToManyField(User, related_name='users_favorites', blank=True)
    categ = models.ForeignKey(Categories, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return 'Title {}, сategory{}, date {}, author {}, description {}'.format(self.title, self.categ,
                                                                                 self.date_published,
                                                                                 self.author.username, self.description)
    @property
    def get_favorites(self):
        """
        Показывает количество добавлений в избранное
        """
        return self.favorites.count()
    @property
    def photo_ad_url(self):
        if self.photo_ad and hasattr(self.photo_ad, 'url'):
            return self.photo_ad.url


class Feedback(models.Model):
    """
    Отзывы
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=700, blank=False)
    in_ad = models.ForeignKey(Ads, on_delete=models.CASCADE)
    date_publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{0} : {1}".format(self.author, self.text[:10] + "...")





