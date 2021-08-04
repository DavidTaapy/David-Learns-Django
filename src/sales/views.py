from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from.forms import SalesSearchForm
import pandas as pd

# Create your views here.


def home_view(request):
    # Initializing dataframe
    sales_df = None
    positions_df = None
    # Both with and without inputs
    form = SalesSearchForm(request.POST or None)

    # When information is given
    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        sales_qs = Sale.objects.filter(created__date__lte=date_to,
                                       created__date__gte=date_from)
        if len(sales_qs) > 0:
            sales_df = pd.DataFrame(sales_qs.values())
            # Getting Positions
            positions_data = []
            for sale in sales_qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price
                    }
                    positions_data.append(obj)
            positions_df = pd.DataFrame(positions_data)
            # Converting DataFrames To HTML
            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
        else:
            print('No data')

    context = {
        'form': form,
        'sales_df': sales_df,
        'positions_df': positions_df
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
