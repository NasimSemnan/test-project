from django import forms
from django.db import IntegrityError
from django.forms import ModelForm
from django.shortcuts import redirect, render
from django.views import generic

from .models import Poll, Question


class PollForm(ModelForm):
    is_first_load = True
    prefix = "poll"
    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all(), widget=forms.CheckboxSelectMultiple, required=False
    )

    class Meta:
        model = Poll
        fields = ["title", "description", "pub_date", "questions"]
        widgets = {
            "pub_date": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"class": "form-control", "placeholder": "Select a date", "type": "date"},
            ),
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "text", "type": "text"},
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Description",
                    "type": "text",
                    "rows": 2,
                },
            ),
            "questions": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "text", "type": "text"},
            ),
        }
        labels = {
            "title": "Title",
            "description": "Description",
            "pub_date": "Published Date",
            "questions": "Questions",
        }


class PollIndexView(generic.ListView):
    template_name = "polls/poll/list_poll.html"
    context_object_name = "latest_poll_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Poll.objects.order_by("-id")[:20]


def create_poll(request):
    if request.method == "POST":
        poll_form = PollForm(data=request.POST)
        if poll_form.is_valid():
            try:
                poll = poll_form.save(commit=False)
                poll.save()
                poll.questions.set(poll_form.cleaned_data["questions"])
                poll.save()
                return redirect("polls:poll_index")
            except IntegrityError:
                return render(request, "polls/poll/create_poll.html", {"poll_form": poll_form})

    else:
        poll_form = PollForm()
        # poll_form = PollForm(data={"title": "", "date": "", "description": "", "questions": ""})

    return render(
        request,
        "polls/poll/creat_poll.html",
        {
            "poll_form": poll_form,
        },
    )
