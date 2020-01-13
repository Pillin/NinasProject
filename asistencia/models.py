from datetime import timezone
from django.db import models

from usuarios.models import User


class Asistencia(models.Model):
    alumna = models.ForeignKey('usuarios.User', related_name='alumna' ,on_delete=models.CASCADE)
    clase = models.ForeignKey('clases.Clase', on_delete=models.CASCADE)
    author = models.ForeignKey('usuarios.User', related_name='profesora' ,on_delete=models.CASCADE)  # quien paso la asistencia

    def __str__(self):
        return "{0} asistió a la clase {1}".format(self.alumna.username, self.clase.nombre)


"""
    def get_asistencia_data(self, **kwargs):
        context = super(UserPreferences, self).get_context_data(**kwargs)
        context['form1'] = Preferences.objects.all()
        return context
"""

class Asistentes(models.Model):
    asistentes = models.ManyToManyField(User, related_name="asistentes", blank=True)
    clase = models.ForeignKey('clases.Clase', on_delete=models.CASCADE)
    author = models.ForeignKey('usuarios.User', related_name='autora', on_delete=models.CASCADE)  # quien paso la asistencia

    def guardarAsistencia(self):
        for asistente in self.asistentes:
            Asistencia.objects.create(alumna=asistente, clase=self.clase, author=self.author)
