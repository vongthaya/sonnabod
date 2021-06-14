from django.shortcuts import render
from table.models import Table
from django.contrib.auth.decorators import login_required


@login_required
def index(req):
    tables = Table.objects.all()
    return render(req, 'home/index.html', {
        "tables": tables
    })