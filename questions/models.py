from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', verbose_name="User's avatar")
    rating = models.IntegerField(default=0, verbose_name="Answer rating")


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tag name")

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def get_hot_questions(self):
        return self.order_by('-rating')

    def get_new_questions(self):
        return self.order_by('-creation_date')

    def get_tag_questions(self, tag):
        return self.filter(tags__name=tag)


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="Question title")
    text = models.TextField(verbose_name="Full question text")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, verbose_name="Question rating")
    creation_date = models.DateTimeField(default=timezone.now, verbose_name="Publication time")
    answer_count = models.IntegerField(default=0, verbose_name="Count of answers")
    is_active = models.BooleanField(default=True, verbose_name="If question is active")
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True)
    objects = QuestionManager()

    def like(self):
        self.rating += 1
        self.save()
        self.author.rating += 1
        self.author.save()
        return self.rating

    def dislike(self):
        self.rating -= 1
        self.save()
        self.author.rating -= 1
        self.author.save()
        return self.rating

    def get_answers(self):
        return self.answer_set.all()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-creation_date']


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(verbose_name="Answer text")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    creation_date = models.DateTimeField(default=timezone.now, verbose_name="Publication time")
    rating = models.IntegerField(default=0, verbose_name="Answer rating")
    is_active = models.BooleanField(default=True, verbose_name="is active")
    is_right = models.BooleanField(default=False, verbose_name="marked by autor as right")

    def like(self):
        self.rating += 1
        self.save()
        self.author.rating += 1
        self.author.save()
        return self.rating

    def dislike(self):
        self.rating -= 1
        self.save()
        self.author.rating -= 1
        self.author.save()
        return self.rating


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="who set")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    is_positive = models.BooleanField(default=True, verbose_name="like/dislike selector")


def question_like(question_id, author):
    question = Question.objects.get(pk=question_id)
    like = Like.objects.filter(author=author, question=question).first()
    if like:
        if like.is_positive:
            return question.rating
        else:
            like.delete()
            return question.like()
    else:
        Like.objects.create(author=author, question=question, is_positive=True)
        return question.like()


def question_dislike(question_id, author):
    question = Question.objects.get(pk=question_id)
    like = Like.objects.filter(author=author, question=question).first()
    if like:
        if not like.is_positive:
            return question.rating
        else:
            like.delete()
            return question.dislike()
    else:
        Like.objects.create(author=author, question=question, is_positive=False)
        return question.dislike()


def answer_like(answer_id, author):
    answer = Answer.objects.get(pk=answer_id)
    like = Like.objects.filter(author=author, answer=answer).first()
    if like:
        if like.is_positive:
            return answer.rating
        else:
            like.delete()
            return answer.like()
    else:
        Like.objects.create(author=author, answer=answer, is_positive=True)
        return answer.like()


def answer_dislike(answer_id, author):
    answer = Answer.objects.get(pk=answer_id)
    like = Like.objects.filter(author=author, answer=answer).first()
    if like:
        if not like.is_positive:
            return answer.rating
        else:
            like.delete()
            return answer.dislike()
    else:
        Like.objects.create(author=author, answer=answer, is_positive=False)
        return answer.dislike()
