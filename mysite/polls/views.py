from django import forms
from django.db.models import F
from django.forms import CharField, ModelForm
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic

from .models import Choice, Question


class QuestionForm(ModelForm):
    is_first_load = True
    prefix = "question"

    class Meta:
        model = Question
        fields = ["question_text", "pub_date", "description"]
        widgets = {
            "pub_date": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"class": "form-control", "placeholder": "Select a date", "type": "date"},
            ),
            "question_text": forms.TextInput(
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
        labels = {
            "pub_date": "Published Date",
            "question_text": "Text",
            "description": "Description",
        }


class QuestionChoiceForm(ModelForm):
    prefix = "choice"

    class Meta:
        model = Choice
        fields = ["id", "choice_text", "description"]
        widgets = {
            "choice_text": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Titel", "type": "text"},
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
        labels = {"choice_text": "Text", "description": "Description"}


class EmptyChoiceForm(forms.Form):
    prefix = "choice"
    choice_text = CharField(
        max_length=200,
        label="Text",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Text", "type": "text"},
        ),
    )
    description = CharField(
        max_length=1_000,
        label="Description",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Description", "type": "text", "rows": 2}
        ),
    )


class ReadQuestion(generic.DetailView):
    model = Question
    template_name = "polls/read_question.html"


def create_question(request):
    if request.method == "POST":
        # Handle the main QuestionForm
        question_form = QuestionForm(data=request.POST)

        # Handle choices from the form (submitted via POST)
        choice_forms = []
        total_choices = int(request.POST.get("total_choices", 0))
        descriptions = request.POST.getlist("choice-description", default=[])
        choice_texts = request.POST.getlist("choice-choice_text", default=[])
        for i in range(total_choices):
            choice_forms.append(
                QuestionChoiceForm(
                    data={
                        "choice-choice_text": choice_texts[i],
                        "choice-description": descriptions[i],
                    }
                )
            )

        if "add_choice" in request.POST:
            choice_forms.append(
                EmptyChoiceForm(data={"choice-choice_text": "", "choice-description": ""})
            )

        # Deleting a choice based on its index

        elif "delete_choice" in request.POST:
            delete_index = int(request.POST["delete_choice"])
            if 0 <= delete_index < total_choices:
                if total_choices > 1:
                    del choice_forms[delete_index]
                    total_choices -= 1
                else:
                    # Optionally, you can show a message that at least one choice must remain
                    print("Cannot delete the last choice.")

            # Saving the form if the question form is valid

        elif question_form.is_valid():
            question = question_form.save()

            # Saving choices after the question is saved
            for choice_form in choice_forms:
                print("choice form")
                if choice_form.is_valid() and not isinstance(
                    choice_form, EmptyChoiceForm
                ):  # Only save valid choices
                    print("valid form")
                    choice_model: Choice = choice_form.save(commit=False)
                    choice_model.question = question
                    choice_model.save()
                    # choice_form.save_m2m()

            return redirect("polls:index")  # Adjust this as per your URL
        # else:
        #     raise KeyError("Invalid Option!")
    else:
        question_form = QuestionForm(data={"question-question_text": ""})
        choice_forms = [
            EmptyChoiceForm(data={"choice-choice_text": "", "choice-description": ""})
        ]  # Initialize with one empty choice

    # Render the form with existing data
    return render(
        request,
        "polls/add_with_choice.html",
        {
            "question_form": question_form,
            "choice_forms": choice_forms,
            "total_choices": len(choice_forms),
        },
    )


def update_question(request: HttpRequest, pk):
    question = get_object_or_404(Question, pk=pk)
    choices = list(Choice.objects.filter(question=question))

    question_form = QuestionForm(instance=question)

    print(question_form.__dict__)

    if request.method == "GET":
        choice_forms = [QuestionChoiceForm(instance=choice) for choice in choices]

    elif request.method == "POST":
        question_form = QuestionForm(data=request.POST, instance=question)

        total_choices = int(request.POST.get("total_choices", 0))
        descriptions = request.POST.getlist("choice-description", default=[])
        choice_texts = request.POST.getlist("choice-texts", default=[])
        choice_forms: list[QuestionChoiceForm] = []

        choice_ids = request.POST.getlist("choice-choice_id", default=[])
        choice_texts = request.POST.getlist("choice-choice_text", default=[])
        descriptions = request.POST.getlist("choice-description", default=[])

        for i in range(total_choices):
            choice_id = choice_ids[i]
            choice_text = choice_texts[i]
            description = descriptions[i]

            choice_forms.append(
                QuestionChoiceForm(
                    data={
                        "choice-choice_id": choice_id,
                        "choice-choice_text": choice_text,
                        "choice-description": description,
                    }
                )
            )

        # Handle adding a new choice
        if "add_choice" in request.POST:
            choice_forms.append(
                EmptyChoiceForm(data={"choice-choice_text": "", "choice-description": ""})
            )

        # Handle deleting a choice
        elif "delete_choice" in request.POST:
            delete_index = int(request.POST["delete_choice"])
            if 0 <= delete_index < total_choices:
                if total_choices > 1:
                    del choice_forms[delete_index]
                    total_choices -= 1
                else:
                    print("Cannot delete the last choice.")

        # Save the question and choices
        elif question_form.is_valid():
            question = question_form.save()

            # Create a set of existing choice IDs New
            existing_choice_ids = {choice.pk for choice in choices}

            # Add or update choices line 1 new
            new_choice_ids = set()
            for i in range(total_choices):
                choice_id = choice_ids[i]
                choice_text = choice_texts[i]
                description = descriptions[i]

                choice = Choice.objects.filter(pk=choice_id).first() if choice_id else None
                choice_form = QuestionChoiceForm(
                    data={"choice-choice_text": choice_text, "choice-description": description},
                    instance=choice,
                )

                if choice_form.is_valid():
                    if choice:
                        choice.choice_text = choice_text
                        choice.description = description
                        choice.save()
                    else:
                        choice_model: Choice = choice_form.save(commit=False)
                        choice_model.question = question
                        choice_model.save()
                        choice_form.save_m2m()

                # Add the choice ID to the new_choice_ids set
                if choice_id:
                    new_choice_ids.add(int(choice_id))

            # all choices to delete and save
            to_be_deleted = existing_choice_ids - new_choice_ids

            # Delete choices that are no longer in the form
            for choice_id in to_be_deleted:
                Choice.objects.filter(pk=choice_id).delete()

            return redirect("polls:index")

    return render(
        request,
        "polls/update_question.html",
        {
            "question_id": pk,
            "question_form": question_form,
            "choice_forms": choice_forms,
            "total_choices": len(choice_forms),
        },
    )


class DeleteQuestion(generic.DeleteView):
    model = Question
    success_url = reverse_lazy("polls:index")
    template_name = "polls/delete_question.html"


class UpdateQuestion(generic.UpdateView):
    model = Question
    fields = ["question_text", "pub_date"]
    template_name = "polls/update_question.html"
    success_url = reverse_lazy("polls:index")


class IndexView(generic.ListView):
    template_name = "polls/list_question.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:20]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])

    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
