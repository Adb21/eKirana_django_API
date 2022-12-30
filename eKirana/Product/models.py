from sre_constants import CHCODES
from django.db import models

# Create your models here.
QTY_TYPE = (
    (0, "Kg"), (1, "Litre"), (3, "Piece")
)

CATEGORY = (
    (0, "Grains"), (1, "Masala"), (3, "Oils"), (4, "Flour"), (5, "Eateries"), (6, "Soap & Detergents"), (7, "Cosmetics"), (8, "Others")

)
class Product(models.Model):
    Title = models.CharField(max_length=100) 
    Description = models.TextField(max_length=500)
    Price = models.IntegerField()
    Category = models.IntegerField(choices=CATEGORY)
    Qty_Type = models.IntegerField(choices=QTY_TYPE)
    Image = models.ImageField(upload_to="product/images",default='product/images/sample.jpeg')
    Stock = models.IntegerField(default=0)
    Shop = models.ForeignKey("Shop.Shopkeeper", on_delete=models.PROTECT)
    
    def __str__(self):
        return str(self.Title)