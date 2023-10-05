from django.shortcuts import render
from django.core.paginator import Paginator
from database.models import Bug, ReporteBug, Proyecto

def index(request):
    bug_list = Bug.objects.order_by("-fecha_reporte")
    bug_paginator = Paginator(bug_list, 5)  # Paginación para la lista de bugs

    report_list = ReporteBug.objects.order_by("-fecha_reporte").select_related("id_proyecto")
    report_paginator = Paginator(report_list, 5)  # Paginación para los reportes

    bug_page_number = request.GET.get('bug_page')
    bug_page_obj = bug_paginator.get_page(bug_page_number)
    bug_page_obj.adjusted_elided_pages = bug_paginator.get_elided_page_range(bug_page_obj.number, on_each_side=1, on_ends=1)

    report_page_number = request.GET.get('report_page')
    report_page_obj = report_paginator.get_page(report_page_number)
    report_page_obj.adjusted_elided_pages = report_paginator.get_elided_page_range(report_page_obj.number, on_each_side=1, on_ends=1)

    context = {
        "bug_page_obj": bug_page_obj,
        "report_page_obj": report_page_obj
    }
    return render(request, "buglist/buglist.html", context)
