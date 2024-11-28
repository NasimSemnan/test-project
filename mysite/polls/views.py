from typing import Any

from django import forms
from django.conf import settings
from django.db.models import F
from django.forms import BaseModelForm, CharField, DateField, ModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic

from .models import Choice, Question


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["question_text", "pub_date"]
        widgets = {
            "pub_date": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"class": "form-control", "placeholder": "Select a date", "type": "date"},
            ),
        }
        labels = {"pub_date": "Published Date"}


class QuestionChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ["id", "choice_text", "description"]
        widgets = {
            "choice_text": forms.TextInput(
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
        }
        labels = {"choice_text": "Text", "description": "Description"}


class EmptyChoiceForm(forms.Form):
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
        for i in range(total_choices):
            choice_text = request.POST.get(f"choice_{i}_choice_text", "")
            description = request.POST.get(f"choice_{i}_description", "")
            choice_forms.append(
                QuestionChoiceForm(
                    data={
                        "choice_text": choice_text,
                        "description": description,
                    }
                )
            )

        # Adding a new choice dynamically
        # if "delete_choice" in request.POST:
        #     print("value is:", request.POST["delete_choice"])

        if "add_choice" in request.POST:
            choice_forms.append(EmptyChoiceForm(data={"choice_text": "", "description": ""}))

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
                # _c_form = QuestionChoiceForm(
                #     data={"choice_text": choice["choice_text"], "description": choice["description"]}
                # )
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
        question_form = QuestionForm(initial={"question_text": ""})
        choice_forms = [{"choice_text": "", "description": ""}]  # Initialize with one empty choice

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

    if request.method == "GET":
        # Get existing choices
        choice_forms = [QuestionChoiceForm(instance=choice) for choice in choices]

    elif request.method == "POST":
        question_form = QuestionForm(data=request.POST, instance=question)

        total_choices = int(request.POST.get("total_choices", 0))

        choice_forms: list[QuestionChoiceForm] = []

        choice_ids = request.POST.getlist("choice_id", default=[])
        choice_texts = request.POST.getlist("choice_text", default=[])
        descriptions = request.POST.getlist("description", default=[])
        for i in range(total_choices):
            choice_id = choice_ids[i]
            choice_text = choice_texts[i]
            description = descriptions[i]

            choice_forms.append(
                QuestionChoiceForm(
                    data={
                        "id": choice_id,
                        "choice_text": choice_text,
                        "description": description,
                    }
                )
            )

        # Handle adding a new choice
        if "add_choice" in request.POST:
            choice_forms.append(EmptyChoiceForm(data={"choice_text": "", "description": ""}))

        # Handle deleting a choice
        elif "delete_choice" in request.POST:
            delete_index = int(request.POST["delete_choice"])
            if 0 <= delete_index < total_choices:
                if total_choices > 1:
                    # remove the choice form
                    del choice_forms[delete_index]
                    total_choices -= 1
                else:
                    # Optionally, you can show a message that at least one choice must remain
                    print("Cannot delete the last choice.")

        # Save the question and choices
        elif question_form.is_valid():
            question = question_form.save()

            # Save choices after the question is saved
            choice_ids = request.POST.getlist("choice_id", default=[])
            choice_texts = request.POST.getlist("choice_text", default=[])
            descriptions = request.POST.getlist("description", default=[])

            # add or update
            for i in range(total_choices):
                choice_id = choice_ids[i]
                choice_text = choice_texts[i]
                description = descriptions[i]

                choice = next(
                    (cf for cf in choices if cf.pk == (int(choice_id) if choice_id else None)),
                    None,
                )
                choice_form = QuestionChoiceForm(
                    instance=choice, data={"choice_text": choice_text, "description": description}
                )

                if choice_form.is_valid():
                    choice_model: Choice = choice_form.save(commit=False)
                    choice_model.question = question
                    choice_model.save()

            to_be_deleted = [c for c in choices if filter(lambda x: c.pk == x, choice_ids)]
            if len(to_be_deleted):
                for c in to_be_deleted:
                    c.delete()

            return redirect("polls:index")

    return render(
        request,
        "polls/update_question.html",
        {
            "question_form": question_form,
            "choice_forms": choice_forms,
            "total_choices": len(choice_forms),
        },
    )


class AddQuession(generic.CreateView):
    model = Question
    fields = ["question_text", "pub_date"]
    template_name = "polls/add_question.html"
    success_url = reverse_lazy("polls:index")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        print("valid", form.data)
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        print("invalid", form.data)
        return super().form_invalid(form)

    def get_absolute_url(self):
        return reverse("polls:detail", args=[str(self.id)])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({"choices": [Choice(), Choice()]})

        print(context)
        return context
        # print(QuestionChoiceForm(prefix="choice_0_"))
        # context.update(QuestionChoiceForm(prefix="choice_0_"))

    def get(self, request: HttpRequest, *args: str, **kwargs: reverse_lazy) -> HttpResponse:  # type: ignore
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: reverse_lazy) -> HttpResponse:  # type: ignore
        print(self.get_form())
        return super().post(request, *args, **kwargs)


# def add_question_choice(request: HttpRequest, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # Add an empty choice by adding a new form instance
#     num_choices = question.choices.count()
#     new_choice_form = QuestionChoiceForm(prefix=f"choice_{num_choices}")

#     # Process current forms
#     return render(
#         request,
#         "polls/add_with_choice.html",
#         {
#             "question_form": QuestionForm(instance=question),
#             "choice_forms": [
#                 QuestionChoiceForm(prefix=f"choice_{i}", instance=choice)
#                 for i, choice in enumerate(question.choices.all())
#             ]
#             + [new_choice_form],
#             "total_choices": len(question.choices),
#         },
#     )


# def remove_question_choice(request: HttpRequest):
#     pass


# def add_question(request: HttpRequest):
#     if request.method == "POST":
#         question_form = QuestionForm(request.POST)

#         # This will hold the list of choice forms
#         choice_forms = []
#         for i in range(int(request.POST.get("total_choices", "1"))):
#             choice_forms.append(QuestionChoiceForm(request.POST, prefix=f"choice_{i}"))

#         # all_choices_valid = True
#         # for choice_form in choice_forms:
#         #     if choice_form.is_valid() is False:
#         #         all_choices_valid = False

#         # if question_form.is_valid() and all_choices_valid:
#         if question_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
#             question = question_form.save()

#             for cf in choice_forms:
#                 choice = cf.save(commit=False)
#                 choice.question = question
#                 choice.save()

#             return redirect(
#                 "list_question", pk=question.pk
#             )  # Adjust this as per your URL structure
#     else:
#         question_form = QuestionForm()
#         choice_forms = [
#             QuestionChoiceForm(prefix="choice_0"),
#             QuestionChoiceForm(prefix="choice_1"),
#         ]

#     return render(
#         request,
#         "polls/add_with_choice.html",
#         {
#             "question_form": question_form,
#             "choice_forms": choice_forms,
#             "total_choices": len(choice_forms),
#         },
#     )


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


# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)


# # ...
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})


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
