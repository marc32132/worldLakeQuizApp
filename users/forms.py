from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "username": "Username",
            "email": "Email",
            "password1": "Password",
            "password2": "Confirm password",
        }

        for field_name, placeholder in placeholders.items():
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs["placeholder"] = placeholder

        self.fields["email"].required = True

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "placeholder": "Username"
        })

        self.fields["password"].widget.attrs.update({
            "placeholder": "Password"
        })