from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("questions/", views.IndexView.as_view(), name="index"),
    path("questions/<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("questions/<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("questions/<int:question_id>/vote/", views.vote, name="vote"),
    # path("questions/add_with_choice", views.add_question, name="add_with_choice"),
    # path(
    #     "questions/add_question_choice/<int:question_id>",
    #     views.add_question_choice,
    #     name="add_question_choice",
    # ),
    path("questions/add/", views.AddQuession.as_view(), name="add_question"),
    path("questions/<int:pk>/delete", views.DeleteQuestion.as_view(), name="delete_question"),
    path("questions/<int:pk>/update", views.UpdateQuestion.as_view(), name="update_question"),
    path("questions/<int:pk>/read", views.ReadQuestion.as_view(), name="read_question"),
    path(
        "questions/create_or_update/",
        views.create_or_update_question,
        name="create_or_update_question",
    ),
]
