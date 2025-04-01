from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe, Comment, Category
import base64

class RecipeForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    image = forms.ImageField(required=False, label='Изображение рецепта')

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'steps', 'cooking_time', 'categories']

    def save(self, commit=True):
        instance = super().save(commit=False)
        uploaded_image = self.cleaned_data.get('image')
        
        if uploaded_image:
            image_data = uploaded_image.read()
            instance.image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Ваш комментарий'
        }