from django.db import models


class MovementType(models.TextChoices):
    AUTOMATIC = "AUTOMATIC", "Automatic"
    MANUAL = "MANUAL", "Manual"
    QUARTZ = "QUARTZ", "Quartz"
    SOLAR = "SOLAR", "Solar"
    SMART = "SMART", "Smart"


class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    founded_year = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Watch(models.Model):
    name = models.CharField(max_length=200)

    # One to Many
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    movement_type = models.CharField(max_length=20, choices=MovementType.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    is_in_collection = models.BooleanField(default=True)
    description = models.TextField()

    # Many to many
    tags = models.ManyToManyField(Tag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WatchDetail(models.Model):
    # One to one
    watch = models.OneToOneField(Watch, on_delete=models.CASCADE)
    case_size = models.FloatField()
    case_material = models.CharField(max_length=100)
    water_resistance = models.IntegerField()
    lug_width = models.FloatField()
    has_date = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.watch.name} Detail"
