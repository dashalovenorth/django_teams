from django import forms

from .models import Developer, Project, Team


class TeamForm(forms.ModelForm):
    developers = forms.ModelMultipleChoiceField(
        queryset=Developer.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Team
        fields = ["name", "developers"]


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "date_start", "status"]  # Removed 'teams' field

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get teams that the current developer belongs to
        self.fields["teams"] = forms.ModelMultipleChoiceField(
            queryset=Team.objects.filter(developers__user=user),
            widget=forms.CheckboxSelectMultiple(),
            required=False,
        )
