from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from .models import Lake

# Create your views here.
def lake_info(request):
    query = request.GET.get('q','')
    lakes = Lake.objects.all()

    if query:
        lakes = lakes.filter(
            Q(name__icontains=query) |
            Q(country__icontains=query)
        )

    p = Paginator(lakes, 20)
    page_num = request.GET.get('page', 1)
    
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    context = {
        'lakes': page,
        'query': query 
    }
    if request.htmx:
        return render(request, "lakes/partials/lake_table.html", context)

    return render(request, 'lakes/lake_info.html', context)
