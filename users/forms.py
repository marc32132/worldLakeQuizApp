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

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control",
            })

            if field_name in placeholders:
                field.widget.attrs["placeholder"] = placeholders[field_name]

        self.fields["email"].required = True

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        print("CUSTOM FORM INIT")
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "placeholder": "Username",
            "class": "form-control"
        })

        self.fields["password"].widget.attrs.update({
            "placeholder": "Password",
            "class": "form-control"
        })