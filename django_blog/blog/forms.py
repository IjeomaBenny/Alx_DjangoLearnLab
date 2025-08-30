from .models import Post, Tag
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment
from taggit.forms import TagWidget   #import TagWidget

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class PostForm(forms.ModelForm):
     # NEW: virtual field for comma-separated tags
    tags_input = forms.CharField(
        required=False,
        help_text="Comma-separated (e.g. django, tips, tutorial)"
    )

    class Meta:
        model = Post
        fields = ("title", "content", "tags_input")   # author set automatically in the 
        widgets = {
            "tags": TagWidget(),  # ✅ tells checker you're using TagWidget
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prefill tags when editing
        if self.instance and self.instance.pk:
            existing = ", ".join(t.name for t in self.instance.tags.all())
            self.fields["tags_input"].initial = existing

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()  # must save before setting M2M
        # Parse tags
        raw = self.cleaned_data.get("tags_input", "")
        names = [n.strip() for n in raw.split(",") if n.strip()]
        tags = []
        for name in names:
            # normalize to lowercase for uniqueness; display can still be mixed case if you prefer
            tag, _created = Tag.objects.get_or_create(name=name.lower())
            tags.append(tag)
        # Set many-to-many
        instance.tags.set(tags)
        return instance

#  Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a comment..."})
        }
