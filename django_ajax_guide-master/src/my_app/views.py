from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .forms import FriendForm
from .models import Friend

from django.views import View

def indexView(request):
    form = FriendForm()
    friends = Friend.objects.all()
    return render(request, "index.html", {"form": form, "friends": friends})


def postFriend(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        form = FriendForm(request.POST)
        
        if form.is_valid():
            instance = form.save()
            ser_instance = serializers.serialize('json', [instance])
            return JsonResponse({"instance": ser_instance}, status=200)
        else:

            error_messages = form.errors.as_json()
            print("Errores del formulario:", error_messages)
            return JsonResponse({"error": error_messages}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

# BONUS CBV
def checkNickName(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "GET":
        nick_name = request.GET.get("nick_name", None)
        
        if nick_name is None:
            return JsonResponse({"error": "No nick_name provided"}, status=400)

        print(f"Received nick_name: {nick_name}")

        if Friend.objects.filter(nick_name=nick_name).exists():
            return JsonResponse({"valid": False}, status=200)
        else:
            return JsonResponse({"valid": True}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)

    



class FriendView(View):
    form_class = FriendForm
    template_name = "index.html"

    def get(self, *args, **kwargs):
        form = self.form_class()
        friends = Friend.objects.all()
        return render(self.request, self.template_name, 
            {"form": form, "friends": friends})

    def post(self, *args, **kwargs):
        # request should be ajax and method should be POST.
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest' and self.request.method == "POST":
            # get the form data
            form = self.form_class(self.request.POST)
            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
                # serialize in new friend object in json
                ser_instance = serializers.serialize('json', [ instance, ])
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        # some error occured
        return JsonResponse({"error": ""}, status=400)
