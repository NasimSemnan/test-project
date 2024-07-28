# from django.views import View
from django.views.generic import TemplateView


# class MessageView(View):
class MessageView(TemplateView):
    # def get(self, request):
    # return render(request, "home.html")
    template_name = "home.html"
