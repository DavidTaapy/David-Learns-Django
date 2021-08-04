from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from.forms import SalesSearchForm
import pandas as pd

# Create your views here.


def home_view(request):
    # Initializing dataframe
    sales_df = None
    # Both with and without inputs
    form = SalesSearchForm(request.POST or None)

    # When information is given
    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        qs = Sale.objects.filter(created__date__lte=date_to,
                                 created__date__gte=date_from)

        if len(qs) > 0:
            sales_df = pd.DataFrame(qs.values())
            sales_df = sales_df.to_html()
        else:
            print('No data')

    context = {
        'form': form,
        'sales_df': sales_df
    }
    return render(request, 'sales/home.html', context)


class SaleListView(ListView):
    model = Sale
    template_name = 'sales/main.html'
    # context_object_name = 'salesItems' # Replace object_list with salesItems


# def sale_list_view(request):
#     qs = Sale.objects.all()
#     return render(request, 'sales/main.html', {'object_list': qs})


class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'

# def sale_detail_view(request, pk):
#     obj = Sale.objects.get(pk = pk)
#     # obj = get_object_or_404(Sale, pk=pk)
#     return render(request, 'sales/detail.html', {'object': obj})
