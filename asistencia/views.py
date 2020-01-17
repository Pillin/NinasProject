from datetime import datetime
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from .models import Asistencia
from asistencia.forms import AsistenciaForm
from clases.models import Clase
from cursos.models import Curso
from usuarios.models import User


class Asistencia_GralView(LoginRequiredMixin, View):
    login_url = 'usuarios:login'
    redirect_field_name = ''


    ## Devuelve un lista compuesta ṕor listas, hay una sublista por alumna.
    ## Cada sublista contiene a la alumna, una lista de booleanos que indica si fue
    # o no a la clase, y el nro total de clases a las que la alumna asistio
    def get_asistencias(self, asistencias, alumnas):
        alum_por_nombre = alumnas.order_by('first_name')
        nro_alumnas = len(alumnas)
        lista_asistencias = []
        i = 0

        while (len(lista_asistencias) < nro_alumnas):
            name = alum_por_nombre[i].first_name
            alum = alumnas.filter(first_name=name).order_by('last_name')

            for alumna in alum:
                asist = asistencias.filter(alumna=alumna).order_by('clase_id')
                lista_a = []
                for asistencia in asist:
                    lista_a += [asistencia.asistio]
                total = len( asist.filter(asistio=True) )
                lista = [alumna, lista_a, total]
                lista_asistencias += [lista]
                i += 1

        return lista_asistencias


    def get(self, request, **kwargs):
        curso_id = kwargs['curso_id']
        curso = get_object_or_404(Curso, pk=curso_id)
        usuaria = User.objects.get(username=request.user.username)
        if usuaria.es_profesora:
            curso = Curso.objects.filter(profesoras__in=[usuaria], id=curso_id)
        elif usuaria.es_voluntaria:
            curso = Curso.objects.filter(voluntarias__in=[usuaria], id=curso_id)

        if len(curso) > 0:
            curso = curso[0]
            clases_totales = Clase.objects.filter(curso=curso).order_by('id')
            asistencias = Asistencia.objects.filter(clase__curso=curso).order_by('clase_id')
            lista_asistencias = list(self.get_asistencias(asistencias, curso.alumnas.all()))
            clases_asist = []             # clases que ya tienen asistencias hasta el momento
            total_por_clase = []    # total de alumnas por clase en clases

            for asistencia in asistencias:
                if not asistencia.clase in clases_asist:
                    clases_asist += [asistencia.clase]
            for clase in clases_asist:
                total_clase = len(asistencias.filter(clase=clase, asistio=True))
                total_por_clase += [total_clase]

            hay_clases = True
            if len(Clase.objects.filter(curso=curso)) == 0:
                hay_clases = not hay_clases
            hay_alumnas = True
            if len(curso.alumnas.all()) == 0:
                hay_alumnas = not hay_alumnas

            id_prox_clase = -1
            if len(clases_asist) < len(clases_totales):
                id_prox_clase = clases_totales[len(clases_asist)].id

            return render(request, 'asistencia/asistencia_gral.html', {
                'curso': curso,
                'clases': clases_asist,
                'lista_asistencias': lista_asistencias,
                'total_por_clase': total_por_clase,
                'hay_clases': hay_clases,
                'hay_alumnas': hay_alumnas,
                'id_prox_clase': id_prox_clase
            })

        return HttpResponseForbidden("No tienes permiso para acceder a la asistencia de este curso.")




class AsistenciaView(LoginRequiredMixin, View):
    login_url = 'usuarios:login'
    redirect_field_name = ''

    def get(self, request, **kwargs):
        curso_id = kwargs['curso_id']
        clase_id = kwargs['clase_id']
        curso = get_object_or_404(Curso, pk=curso_id)
        usuaria = User.objects.get(username=request.user.username)
        if usuaria.es_profesora:
            cursos = Curso.objects.filter(profesoras__in=[usuaria])
        elif usuaria.es_voluntaria:
            cursos = Curso.objects.filter(voluntarias__in=[usuaria])
        else:
            return HttpResponseForbidden("No tienes permiso para acceder a la asistencia de este curso.")

        clase = list(Clase.objects.filter(curso=curso, id=clase_id))[0]
        form = self.get_form(request)

        if curso in list(cursos):
            return render(request, 'asistencia/asistencia.html', {
                'curso': curso,
                'clase': clase,
                'form': form
        })

        return HttpResponseForbidden("No tienes permiso para acceder a la asistencia de este curso.")

    def get_form(self, request):
        if request.method == "POST":
            form = AsistenciaForm(request.POST)
            asistentes = form.save(commit=False)
            asistentes.author=request.user
            asistentes.guardarAsistencia()
        else:
            form = AsistenciaForm()
        return form









