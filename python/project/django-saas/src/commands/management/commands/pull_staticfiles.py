from typing import Any
from django.core.management.base import BaseCommand
from django.conf import settings
from utils.downloader import download_to_local

VENDOR_STATICFILES = {
    "flowbite.min.css": "https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.css",
    "flowbite.min.js": "https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.js",
    "flowbite.min.js.map": "https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.js.map",
}


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        self.stdout.write(self.style.NOTICE("Downloading Static Files!"))

        for name, url in VENDOR_STATICFILES.items():
            download_to_local(name, url, settings.STATICFILES_VENDOR_DIR)

        self.stdout.write(self.style.SUCCESS("All Static Files Downloaded!"))
