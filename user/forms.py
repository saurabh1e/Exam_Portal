from django import forms
from user.models import UserProfile
from ckeditor.widgets import CKEditorWidget
from user.models import user


class UserEditForm(forms.ModelForm):
    username = forms.IntegerField(help_text="Please enter a username.")
    """Form for viewing and editing name fields in a User object.

    A good reference for Django forms is:
    http://pydanny.com/core-concepts-django-modelforms.html
    """

    def __init__(self, *args, **kwargs):

        # TODO: this doesn't seem to work. Need to get to the bottom of it.
        #self.base_fields["display_name"].min_length = 2
        #self.base_fields["display_name"].validators.append(MinLengthValidator)
        #print self.base_fields['display_name'].validators
        super(forms.ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = user
        fields = ('username', 'first_name')


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = user

    def is_valid(self):
        #log.info(force_text(self.errors))
        return super(UserAdminForm, self).is_valid()



class UserProfileForm(forms.ModelForm):

    avatar_url = forms.ImageField( help_text="Select a profile image to upload.", required=True)
    dob = forms.DateField()
    cv = forms.FileField(help_text="enter your cv",required=true)

    class Meta:
        model = UserProfile
        exclude = ( )
        fields = ('dob', 'avatar_url')
