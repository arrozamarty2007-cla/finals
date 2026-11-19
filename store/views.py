from pathlib import Path

from django.http import HttpResponse


def storefront(request):
    html_path = Path(r"C:\Users\student\Downloads\storefront.html")
    if not html_path.exists():
        return HttpResponse("<h1>Storefront HTML file not found.</h1>", status=404)
    return HttpResponse(html_path.read_text(encoding='utf-8'), content_type='text/html')