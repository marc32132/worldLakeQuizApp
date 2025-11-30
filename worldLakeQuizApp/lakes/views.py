from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from .models import Lake

# Create your views here.
def lake_info(request):
    lakes = Lake.objects.all()
    p = Paginator(lakes, 20)
    page_num = request.GET.get('page', 1)
    
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    return render(request, 'lakes/lake_info.html', {'lakes': page })
