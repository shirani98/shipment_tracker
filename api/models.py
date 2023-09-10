from django.db import models
import re


class Shipment(models.Model):
    tracking_number = models.CharField(max_length=255)
    carrier = models.CharField(max_length=255)
    sender_address = models.TextField()
    receiver_address = models.TextField()
    article_name = models.CharField(max_length=255)
    article_quantity = models.PositiveIntegerField()
    article_price = models.DecimalField(max_digits=10, decimal_places=2)
    SKU = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    receiver_zip_code = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.tracking_number

    def save(self, *args, **kwargs):
        self.receiver_zip_code = self.extract_city_from_address(self.receiver_address)
        super(Shipment, self).save(*args, **kwargs)

    def extract_city_from_address(self, address: str):
        # Use regular expressions to extract the zip code
        match = re.search(r"\b(\d{4,5})\b", address)
        if match:
            return match.group(1)
        return None
