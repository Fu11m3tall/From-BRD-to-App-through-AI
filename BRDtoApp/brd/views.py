from django.shortcuts import render
from .models import BRDVarity
from django.shortcuts import get_object_or_404
# Create your views here.
def brd(request):
    brd_varieties = BRDVarity.objects.all()
    return render(request, 'frontend/brd.html', {'brd_varieties': brd_varieties})

def brd_detail(request, pk):
    brd_variety = get_object_or_404(BRDVarity, pk=pk)
    return render(request, 'frontend/brd_detail.html', {'brd_variety': brd_variety})