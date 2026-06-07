from django.shortcuts import get_object_or_404, render

from .models import Watch


def home(request):
    watches = Watch.objects.all().order_by("-created_at")[:3]
    context = {"watches": watches}

    return render(request, "catalog/home.html", context)


def watch_list(request):
    watches = (
        Watch.objects.select_related("brand", "category")
        .prefetch_related("tags")
        .order_by("name")
    )

    context = {
        "watches": watches,
    }

    return render(request, "catalog/watch_list.html", context)


def watch_detail(request, watch_id):
    watch = get_object_or_404(
        Watch.objects.select_related(
            "brand", "category", "watchdetail"
        ).prefetch_related("tags"),
        id=watch_id,
    )

    context = {
        "watch": watch,
    }

    return render(request, "catalog/watch_detail.html", context)
