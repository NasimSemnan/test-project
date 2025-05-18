from django import forms
from django.db import IntegrityError
from django.forms import ModelForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from .models import Poll, Question


class PollForm(ModelForm):
    is_first_load = True
    prefix = "poll"
    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all(), widget=forms.CheckboxSelectMultiple, required=True
    )
    total_questions = forms.IntegerField(
        label="Total Questions",
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control", "readonly": "readonly"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['total_questions'].initial = Question.objects.count()

    class Meta:
        model = Poll
        fields = ["title", "description", "pub_date", "questions"]

        widgets = {
            "pub_date": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"class": "form-control", "placeholder": "Select a date", "type": "date"},
            ),
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title", "type": "text"},
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Description",
                    "type": "text",
                    "rows": 2,
                },
            ),
        }


class UpdatePoll(generic.UpdateView):
    model = Question
    fields = ["question_text", "pub_date"]
    template_name = "polls/update_poll.html"
    success_url = reverse_lazy("polls:index")


class DeletePoll(generic.DeleteView):
    model = Question
    template_name = "polls/delete_poll.html"
    success_url = reverse_lazy("polls:index")


class PollIndexView(generic.ListView):
    template_name = "polls/poll/list_poll.html"
    context_object_name = "latest_poll_list"

    def get_queryset(self):
        return Poll.objects.order_by("-id")[:20]


def create_poll(request):
    if request.method == "POST":
        poll_form = PollForm(data=request.POST)
        if poll_form.is_valid():
            try:
                poll: Poll = poll_form.save(commit=False)
                poll.save()
                poll.questions.set(poll_form.cleaned_data["questions"])
                poll.save()
                return redirect("polls:poll_index")
            except IntegrityError:
                return render(request, "polls/poll/create_poll.html", {"poll_form": poll_form})

    else:
        poll_form = PollForm(initial={"total_questions": Question.objects.count()})

    return render(
        request,
        "polls/poll/create_poll.html",
        {
            "poll_form": poll_form,
        },
    )
