from django.shortcuts import render
from .models import Noticia
from django.core.paginator import Paginator

def noticias(request):
    noticias=Noticia.objects.all()
    paginator = Paginator(noticias, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "core/noticias.html", {"page_obj": page_obj})
