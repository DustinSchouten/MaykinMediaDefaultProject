from django import forms


class CityForm(forms.Form):
    city = forms.CharField(max_length=255)


class ReservationForm1(forms.Form):
    hotel_room = forms.ChoiceField(widget=forms.RadioSelect, required=True)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        room_choices = kwargs.pop('room_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['hotel_room'].choices = room_choices

    def clean(self):
        cleaned_data = super().clean()
        field_start_date = cleaned_data.get('start_date')
        field_end_date = cleaned_data.get('end_date')

        # Validate that the filled in end date value is greather than the filled in start date
        if field_end_date <= field_start_date:
            raise forms.ValidationError("The selected end date must occur later in time than the selected start date.")

        return cleaned_data


class ReservationForm2(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email_address = forms.EmailField()
    address = forms.CharField()
    postal_code = forms.CharField(min_length=6, max_length=6)
    country = forms.ChoiceField(
        choices=[
            ('Netherlands', 'Netherlands'),
            ('Belgium', 'Belgium'),
            ('Germany', 'Germany'),
        ],
        required=True,
    )
