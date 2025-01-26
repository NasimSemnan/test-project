from django.urls import path

from . import poll_views, views

app_name = "polls"
urlpatterns = [
    path("questions/", views.IndexView.as_view(), name="index"),
    path("questions/<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("questions/<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("questions/<int:question_id>/vote/", views.vote, name="vote"),
    path("questions/<int:pk>/delete", views.DeleteQuestion.as_view(), name="delete_question"),
    path("questions/<int:pk>/read", views.ReadQuestion.as_view(), name="read_question"),
    path(
        "questions/create/",
        views.create_question,
        name="create_question",
    ),
    path(
        "questions/<int:pk>/update/",
        views.update_question,
        name="update_question",
    ),
    ####polls
    path("polls/", poll_views.PollIndexView.as_view(), name="poll_index"),
    path(
        "polls/create/",
        poll_views.create_poll,
        name="create_poll",
    ),
    path("polls/<int:pk>/delete", poll_views.DeletePoll.as_view(), name="delete_poll"),
]
