def get_alumnas_en_orden(alumnas):
    alum_por_nombre = alumnas.order_by('first_name')
    nro_alumnas = len(alumnas)
    lista_alumnas = []
    i = 0

    while (len(lista_alumnas) < nro_alumnas):
        name = alum_por_nombre[i].first_name
        alum = alumnas.filter(first_name=name).order_by('last_name')

        for alumna in alum:
            lista_alumnas += [alumna]
            i += 1

    return lista_alumnas

"""def get_cursos(usuaria, curso_id):
    if usuaria.es_profesora:
        cursos = Curso.objects.filter(profesoras__in=[usuaria], id=curso_id)
    elif usuaria.es_voluntaria:
        cursos = Curso.objects.filter(voluntarias__in=[usuaria], id=curso_id)
    elif usuaria.es_alumna:
        cursos = Curso.objects.filter(alumnas__in=[usuaria], id=curso_id)

    if len(cursos) > 0:
        return cursos[0]
    return None"""

