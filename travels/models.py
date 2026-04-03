from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def update_completion(self):
        self.is_completed = (
            self.places.count() >= 10 and
            all(place.visited for place in self.places.all())
        )
        self.save()

    def __str__(self):
        return self.name


class Place(models.Model):
    class Meta:
        unique_together = ('project', 'external_id')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='places')
    external_id = models.IntegerField()
    notes = models.TextField(blank=True)
    visited = models.BooleanField(default=False)

    def __str__(self):
        return f"Place {self.external_id} (Project {self.project.id})"