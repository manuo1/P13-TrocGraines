from django.core.paginator import Paginator
from django.shortcuts import render

from seeds.forms import SeedSearchForm
from seeds.models import SeedManager

seed_manger = SeedManager()


def homepage(request):
    """ display homepage / search seed form / seed results """
    if request.method == 'POST':
        search_form = SeedSearchForm(request.POST)
        if search_form.is_valid():
            searched_seed = search_form.cleaned_data.get('search')
            matching_list = seed_manger.find_matching_seeds_to(searched_seed)
    else:
        searched_seed = ''
        matching_list = seed_manger.get_last_seeds_added()

    """ add paginator """
    paginator = Paginator(matching_list, 8)  # Show 8 seeds per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'searched_seed': searched_seed,
        'page_obj': page_obj,
        'search_form': SeedSearchForm(),
    }
    return render(request, 'homepage.html', context)


def legal_disclaimers(request):
    return render(request, 'legal_disclaimers.html')
