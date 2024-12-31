from django import forms
from django.forms import ModelForm
from django.shortcuts import redirect, render
from django.views import generic

from .models import Poll


class PollForm(ModelForm):
    is_first_load = True
    prefix = "poll"

    class Meta:
        model = Poll
        fields = ["title", "description", "pub_date"]
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
        }
        labels = {
            "title": "Title",
            "description": "Description",
            "pub_date": "Published Date",
        }


class PollIndexView(generic.ListView):
    template_name = "polls/poll/list_poll.html"
    context_object_name = "latest_poll_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Poll.objects.order_by("-id")[:20]


def create_poll(request):
    if request.method == "POST":
        # Handle the main QuestionForm
        poll_form = PollForm(data=request.POST)
        if poll_form.is_valid():
            poll = poll_form.save()  # noqa: F841
        # Handle choices from the form (submitted via POST)
        # choice_forms = []
        # total_choices = int(request.POST.get("total_choices", 0))
        # descriptions = request.POST.getlist("choice-description", default=[])
        # choice_texts = request.POST.getlist("choice-texts", default=[])
        # for i in range(total_choices):
        #     choice_forms.append(
        #         QuestionChoiceForm(
        #             data={
        #                 "choice-choice_text": choice_texts[i],
        #                 "choice-description": descriptions[i],
        #             }
        #         )
        #     )

        # if "add_choice" in request.POST:
        #     choice_forms.append(
        #         EmptyChoiceForm(data={"choice-choice_text": "", "choice-description": ""})
        #     )

        # # Deleting a choice based on its index

        # elif "delete_choice" in request.POST:
        #     delete_index = int(request.POST["delete_choice"])
        #     if 0 <= delete_index < total_choices:
        #         if total_choices > 1:
        #             del choice_forms[delete_index]
        #             total_choices -= 1
        #         else:
        #             # Optionally, you can show a message that at least one choice must remain
        #             print("Cannot delete the last choice.")

        # Saving the form if the question form is valid

        # Saving choices after the question is saved
        # for choice_form in choice_forms:
        #     print("choice form")
        #     # _c_form = QuestionChoiceForm(
        #     #     data={"choice_text": choice["choice_text"], "description": choice["description"]}
        #     # )
        #     if choice_form.is_valid() and not isinstance(
        #         choice_form, EmptyChoiceForm
        #     ):  # Only save valid choices
        #         print("valid form")
        #         choice_model: Choice = choice_form.save(commit=False)
        #         choice_model.question = question
        #         choice_model.save()
        #         # choice_form.save_m2m()

        return redirect("polls:poll_index")  # Adjust this as per your URL
        # # else:
        # #     raise KeyError("Invalid Option!")
    else:
        poll_form = PollForm(data={"title": "", "date": "", "description": ""})
        # choice_forms = [
        #     EmptyChoiceForm(data={"choice-choice_text": "", "choice-description": ""})
        # ]  # Initialize with one empty choice

    # Render the form with existing data
    return render(
        request,
        "polls/poll/creat_poll.html",
        {
            "poll_form": poll_form,
            # "choice_forms": choice_forms,
            # "total_choices": len(choice_forms),
        },
    )
