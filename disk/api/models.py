from django.db import models


class Content(models.Model):
    TYPES = (
        ('FOLDER', 'FOLDER'),
        ('FILE', 'FILE'),
    )

    id = models.CharField(max_length=255, primary_key=True)
    url = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=6, choices=TYPES)
    parentId = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="children")
    date = models.DateTimeField()
    size = models.IntegerField()