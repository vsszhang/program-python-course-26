# Personal Watch Collection Catalog

This is a Django web project for a personal watch catalog. It lets users view a watch collection, open watch details, add new watches with a web form, and delete watches after confirmation.

## Project Structure

```text
homework_02_Django/
├── manage.py
├── db.sqlite3
├── watch_catalog/
│   ├── settings.py
│   └── urls.py
├── catalog/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
├── templates/catalog/
│   ├── base.html
│   ├── home.html
│   ├── watch_list.html
│   ├── watch_detail.html
│   ├── watch_form.html
│   └── watch_confirm_delete.html
└── static/catalog/css/
    └── style.css
```

Main Django parts:

| Part | Files | Purpose |
| --- | --- | --- |
| Model | `catalog/models.py` | Defines database tables and relationships |
| View | `catalog/views.py` | Handles requests and returns responses |
| Template | `templates/catalog/*.html` | Shows data on web pages |
| URL | `watch_catalog/urls.py`, `catalog/urls.py` | Connects URLs to views |
| Form | `catalog/forms.py` | Validates and saves form input |
| Static | `static/catalog/css/style.css` | Adds custom page styles |

## Module Flow

```mermaid
flowchart TD
    A["Browser request"] --> B["watch_catalog/urls.py"]
    B --> C["catalog/urls.py"]
    C --> D["catalog/views.py"]
    D --> E["catalog/models.py"]
    D --> F["catalog/forms.py"]
    E --> G["templates/catalog/*.html"]
    F --> G
    G --> H["base.html loads style.css"]
    H --> I["HTML response"]
```

Page flow:

```mermaid
flowchart LR
    Home["/ Home"] --> List["/watches/ Watch list"]
    Home --> Add["/watches/add/ Add watch"]
    List --> Detail["/watches/<id> Watch detail"]
    List --> Add
    Detail --> Delete["/watches/<id>/delete/ Delete confirmation"]
    Detail --> List
    Add --> Detail
    Delete --> List
    Delete --> Detail
```

Model relationships:

```mermaid
erDiagram
    Brand ||--o{ Watch : has
    Category ||--o{ Watch : groups
    Watch ||--|| WatchDetail : owns
    Watch }o--o{ Tag : uses
```

## Implemented Features

### Data Models

The project has 5 models:

| Model | Purpose |
| --- | --- |
| `Brand` | Watch brand information |
| `Category` | Watch category |
| `Tag` | Watch tags |
| `Watch` | Main catalog item |
| `WatchDetail` | Extra technical details for one watch |

The project includes all required relationship types:

| Relationship | Django field | Code example | Meaning |
| --- | --- | --- | --- |
| One-to-one | `OneToOneField` | `WatchDetail.watch` | One watch has one detail record |
| One-to-many | `ForeignKey` | `Watch.brand` | One brand has many watches |
| One-to-many | `ForeignKey` | `Watch.category` | One category has many watches |
| Many-to-many | `ManyToManyField` | `Watch.tags` | One watch can have many tags |

The models also use different field types:

- `CharField` for short text
- `TextField` for long text
- `IntegerField` for numbers
- `DecimalField` and `FloatField` for decimal values
- `DateField` for dates
- `BooleanField` for true or false values
- `TextChoices` for movement type choices
- `DateTimeField` for creation time

### Pages

| URL | View | Template | Purpose |
| --- | --- | --- | --- |
| `/` | `home` | `home.html` | Home page with latest watches |
| `/watches/` | `watch_list` | `watch_list.html` | List all watches |
| `/watches/<id>` | `watch_detail` | `watch_detail.html` | Show one watch in detail |
| `/watches/add/` | `watch_create` | `watch_form.html` | Add a new watch |
| `/watches/<id>/delete/` | `watch_delete` | `watch_confirm_delete.html` | Confirm and delete a watch |
| `/admin/` | Django Admin | Built-in admin | Manage all model data |

### Form and Database

The add page uses `WatchForm`, a Django `ModelForm`. The form validates input, saves valid data to SQLite, and redirects to the new watch detail page.

The form includes custom validation:

- Watch name must have at least 2 characters.
- Price cannot be negative.

### Delete Feature

Delete is implemented with a confirmation page. A GET request only shows the confirmation page. The watch is deleted only after a POST request.

### Styling

All pages use custom CSS from `static/catalog/css/style.css`. The stylesheet adds:

- custom font settings
- gradient page background
- navigation bar
- card grid layout
- form styles
- button styles
- error message styles
- detail information grid
- tag styles

## Important Code Explanations

### Project URL Routing

`watch_catalog/urls.py`

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalog.urls")),
]
```

This sends `/admin/` to Django Admin. All normal site pages are passed to `catalog.urls`.

### App URL Routing

`catalog/urls.py`

```python
urlpatterns = [
    path("", views.home, name="home"),
    path("watches/", views.watch_list, name="watch_list"),
    path("watches/add/", views.watch_create, name="watch_create"),
    path("watches/<int:watch_id>", views.watch_detail, name="watch_detail"),
    path("watches/<int:watch_id>/delete/", views.watch_delete, name="watch_delete"),
]
```

Each URL is connected to one view function. The `name` value is used in templates with `{% url %}`.

### Model Relationships

`catalog/models.py`

```python
class Watch(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)


class WatchDetail(models.Model):
    watch = models.OneToOneField(Watch, on_delete=models.CASCADE)
```

This code shows the three required database relationships: one-to-one, one-to-many, and many-to-many.

### Movement Type Choices

`catalog/models.py`

```python
class MovementType(models.TextChoices):
    AUTOMATIC = "AUTOMATIC", "Automatic"
    MANUAL = "MANUAL", "Manual"
    QUARTZ = "QUARTZ", "Quartz"
    SOLAR = "SOLAR", "Solar"
    SMART = "SMART", "Smart"
```

This gives fixed choices for the `movement_type` field. It shows how Django can store enum-like values.

### List View

`catalog/views.py`

```python
def watch_list(request):
    watches = (
        Watch.objects.select_related("brand", "category")
        .prefetch_related("tags")
        .order_by("name")
    )

    return render(request, "catalog/watch_list.html", {"watches": watches})
```

This view reads watches from the database and sends them to the list template. `select_related` and `prefetch_related` reduce extra database queries.

### Detail View

`catalog/views.py`

```python
def watch_detail(request, watch_id):
    watch = get_object_or_404(
        Watch.objects.select_related(
            "brand", "category", "watchdetail"
        ).prefetch_related("tags"),
        id=watch_id,
    )
```

`get_object_or_404` returns the watch if it exists. If the ID is wrong, Django returns a 404 page.

### Create View

`catalog/views.py`

```python
def watch_create(request):
    if request.method == "POST":
        form = WatchForm(request.POST)
        if form.is_valid():
            watch = form.save()
            return redirect("catalog:watch_detail", watch_id=watch.id)
    else:
        form = WatchForm()

    return render(request, "catalog/watch_form.html", {"form": form})
```

This view shows an empty form for GET requests. For POST requests, it validates the input, saves the watch, and redirects to the detail page.

### Form Validation

`catalog/forms.py`

```python
def clean_price(self):
    price = self.cleaned_data["price"]

    if price < 0:
        raise forms.ValidationError("Price cannot be negative.")

    return price
```

This is custom validation. If the user enters a negative price, Django shows an error instead of saving the data.

### Template Data Display

`templates/catalog/watch_list.html`

```django
{% for watch in watches %}
  <a href="{% url 'catalog:watch_detail' watch.id %}">
    {{ watch.name }}
  </a>
  {{ watch.brand.name }}
  {{ watch.category.name }}
{% empty %}
  <p>No watches found.</p>
{% endfor %}
```

The template loops through the `watches` data from the view and displays related brand and category fields.

### Static CSS

`templates/catalog/base.html`

```django
{% load static %}
<link rel="stylesheet" href="{% static 'catalog/css/style.css' %}" />
```

This loads the custom stylesheet for every page that extends `base.html`.

## Quick Demo Points

1. The project uses a normal Django structure.
2. The database has 5 models.
3. The models include one-to-one, one-to-many, and many-to-many relationships.
4. The project has home, list, detail, add, and delete pages.
5. The add page uses a `ModelForm`.
6. Form input is validated before saving.
7. New data appears immediately after saving.
8. The project uses custom CSS instead of browser default styles.
