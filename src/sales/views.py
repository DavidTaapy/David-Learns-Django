from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearchForm
from reports.forms import ReportForm
from .utils import get_customer_from_id, get_salesman_from_id, get_chart
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


@login_required
def home_view(request):
    # Initializing variables
    no_data = None
    # Initializing dataframe
    sales_df = None
    positions_df = None
    merged_df = None
    df = None
    # Initializing chart
    chart = None
    # Both with and without inputs
    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()
    # When information is given
    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')
        sales_qs = Sale.objects.filter(created__date__lte=date_to,
                                       created__date__gte=date_from)
        if len(sales_qs) > 0:
            sales_df = pd.DataFrame(sales_qs.values())
            sales_df['customer_id'] = sales_df['customer_id'].apply(
                get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(
                get_salesman_from_id)
            sales_df['created'] = sales_df['created'].apply(
                lambda x: x.strftime('%Y-%m-%d'))
            sales_df.rename({
                'customer_id': 'customer',
                'salesman_id': 'salesman',
                'id': 'sales_id'
            }, axis=1, inplace=True)
            # Getting Positions
            positions_data = []
            for sale in sales_qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id': pos.get_sales_id()
                    }
                    positions_data.append(obj)
            positions_df = pd.DataFrame(positions_data)
            merged_df = pd.merge(sales_df, positions_df, on='sales_id')
            # Transforming Merged DataFrame
            df = merged_df.groupby('transaction_id', as_index=False)[
                'price'].agg('sum')
            # Generating charts
            chart = get_chart(chart_type, sales_df, results_by)
            # Converting DataFrames To HTML
            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            merged_df = merged_df.to_html()
            df = df.to_html()
        else:
            no_data = 'No data available in this date range!'

    context = {
        'search_form': search_form,
        'report_form': report_form,
        'sales_df': sales_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
        'df': df,
        'chart': chart,
        'no_data': no_data
    }
    return render(request, 'sales/home.html', context)


class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/main.html'
    # context_object_name = 'salesItems' # Replace object_list with salesItems


# def sale_list_view(request):
#     qs = Sale.objects.all()
#     return render(request, 'sales/main.html', {'object_list': qs})


class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'sales/detail.html'

# def sale_detail_view(request, pk):
#     obj = Sale.objects.get(pk = pk)
#     # obj = get_object_or_404(Sale, pk=pk)
#     return render(request, 'sales/detail.html', {'object': obj})
