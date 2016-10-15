from django import forms
from django.db import transaction

import utils
from models import Forum, Thread, Post

class NewThreadForm(forms.Form):
    thread_min_len = utils.get_config('min_thread_title_chars')
    post_min_len = utils.get_config('min_post_chars')

    title = forms.CharField(label='Title',
                            max_length=1000,
                            min_length=thread_min_len)

    content = forms.CharField(label='Post Body',
                              min_length=post_min_len,
                              widget=forms.Textarea())

    forum = forms.ModelChoiceField(queryset=Forum.objects.all(),
                                   widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(NewThreadForm, self).__init__(*args, **kwargs)

        self.thread = None
        self.post = None

    @transaction.atomic
    def save(self, author):
        self.thread = Thread(
            title=self.cleaned_data['title'],
            forum=self.cleaned_data['forum'])

        self.thread.save()

        self.post = Post(
            thread=self.thread,
            content=self.cleaned_data['content'],
            author=author)

        self.post.save()

        return self.thread

