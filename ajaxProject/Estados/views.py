from django.shortcuts import render
from .models import Estado, Municipio
from django.http import JsonResponse


def index(request):
    estados = Estado.objects.all()
    return render(request, 'Estados/index.html', {'estados': estados})

def load_municipios(request):
    estado_id = request.GET.get('estado_id')
    municipios = Municipio.objects.filter(estado_id = estado_id).values('id', 'nombre')
    return JsonResponse(list(municipios), safe=False)

