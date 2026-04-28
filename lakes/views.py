from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from .models import Lake


def lake_info(request):
    """
    Displays a paginated list of lakes, optionally filtered by a search query.
    
    Supports:
    - GET parameter 'q' for case-insensitive filtering by name or country
    - Pagination (20 lakes per page)
    - HTMX requests to update just the table without full page reload
    """

    # Get search query from GET parameters (default is empty string)
    query = request.GET.get('q','')
    lakes = Lake.objects.all().order_by('name')

    # Filter lakes by name or country if query is provided
    if query:
        lakes = lakes.filter(
            Q(name__icontains=query) |
            Q(country__icontains=query)
        )

    # Paginate results (20 lakes per page)
    p = Paginator(lakes, 20)
    page_num = request.GET.get('page', 1)
    
    # Try to get requested page; fallback to page 1 if invalid
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    context = {
        'lakes': page,
        'query': query 
    }

    # Return only the table for HTMX requests (partial update)
    if request.htmx:
        return render(request, "lakes/partials/lake_table.html", context)

    return render(request, 'lakes/lake_info.html', context)
