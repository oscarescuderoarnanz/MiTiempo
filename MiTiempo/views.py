from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Usuario, Municipio, Comentario
from django.views.decorators.csrf import csrf_exempt
# MODULOS PARSEO JSON Y XML
from . import parserjson
from . import parserxml
from . import obtenerdatosmunicipio
# Es necesario instalarla -> pip install unidecode
from unidecode import unidecode
import time

# VARIABLES GLOBALES
datos_no_variantes_pueblos = parserjson.main()
valor_boton = 1
tiempo_reload_page = 0


def actualizardatos(municipios):
    global tiempo_reload_page
    tiempo = time.time()
    if((tiempo - tiempo_reload_page) > 3600):
        tiempo_reload_page = time.time()
        for m in municipios:
            datos_variantes_pueblos = obtenerdatosmunicipio.datos_municipio(str(m.nombre_municipio))
            prob_pre = str(datos_variantes_pueblos[0]) # precipitacion
            descr = str(datos_variantes_pueblos[1])# descripcion
            tmax = str(datos_variantes_pueblos[2]) #tmax
            tmin = str(datos_variantes_pueblos[3]) #tmin
            m.precipitaion = prob_pre
            m.descripcion = descr
            m.tmax = tmax
            m.tmin = tmin
            m.save()

def listamunicipiosordenados(municipios):
    lista_munis = []

    for m in municipios:
        if m.numcom >= 1:
            lista_munis.append(m)

    for i in range(1,len(lista_munis)):
        for j in range(0,len(lista_munis)-i):
            if(lista_munis[j+1].numcom < lista_munis[j].numcom):
                aux = lista_munis[j];
                lista_munis[j] = lista_munis[j+1];
                lista_munis[j+1] = aux;

    n = 0
    if len(lista_munis) > 10:
        n = len(lista_munis) - 10
        for i in range(0, n):
            lista_munis.pop(i)

    for i in range(1,len(lista_munis)):
        for j in range(0,len(lista_munis)-i):
            if(lista_munis[j+1].numcom > lista_munis[j].numcom):
                aux = lista_munis[j];
                lista_munis[j] = lista_munis[j+1];
                lista_munis[j+1] = aux;

    return lista_munis


def paginaprincipal(request):
    empty_users = False
    global valor_boton
    municipios = Municipio.objects.all()
    actualizardatos(municipios)
    usuarios = Usuario.objects.all()
    if Usuario.objects.count() == 0:
        empty_users = True
    lista_munis = []
    lista_munis = listamunicipiosordenados(municipios)

    if request.user.username != "":
        try:
            superuser = Usuario.objects.get(username=request.user.username)
        except Usuario.DoesNotExist:
            titulo = "Página de "+request.user.username
            user_register_Usuario = Usuario(username=request.user.username, titulo=titulo)
            user_register_Usuario.save()

    if request.method == "POST":
        if 'botton' in request.POST:
            valor = int(request.POST['botton'])
            if valor == 1:
                texto = "Municipios con probabilidad de precipitacion > 0:"
                dicc_mun_prec = []
                for i in municipios:
                    municipio_prec = int(i.precipitaion)
                    if municipio_prec > 0:
                        dicc_mun_prec += [i]
                valor_boton = valor_boton + 1
                content = "Ver Prob. precipitacion = 0"
                return render(request, 'MiTiempo/base.html', {'municipios': dicc_mun_prec,
                    'usuarios': usuarios, 'value': valor_boton, 'content': content, 'texto': texto})
            elif valor == 2:
                texto = "Municipios con probabilidad de precipitacion = 0:"
                dicc_mun_prec = []
                for i in municipios:
                    municipio_prec = int(i.precipitaion)
                    if municipio_prec == 0:
                        dicc_mun_prec += [i]
                valor_boton = valor_boton + 1
                content = "Ver todos los municipios "
                return render(request, 'MiTiempo/base.html', {'municipios': dicc_mun_prec,
                    'usuarios': usuarios, 'value': valor_boton, 'content': content, 'texto': texto})
            elif valor == 3:
                valor_boton = 1
        elif 'puntuacion' in request.POST:
            name = request.POST['puntuacion']
            mun = Municipio.objects.get(nombre_municipio = name)
            mun.puntuacion = mun.puntuacion + 1
            mun.save()

    texto = "Hasta 10 municipios con más comentarios:"
    format = request.GET.get('format')
    if format == "xml":
        response = render(request, 'MiTiempo/pagprincipal.xml', {'municipios':lista_munis}, content_type = "text/xml")
        return HttpResponse(response, "text/xml")

    content = "Ver Prob. precipitacion > 0"
    return render(request, 'MiTiempo/base.html', {'municipios': lista_munis,
        'usuarios': usuarios, 'value': valor_boton, 'content': content, 'empty_users': empty_users, 'texto': texto})


def informacion(request):
    if request.user.username != "":
        try:
            superuser = Usuario.objects.get(username=request.user.username)
        except Usuario.DoesNotExist:
            titulo = "Página de "+request.user.username
            user_register_Usuario = Usuario(username=request.user.username, titulo=titulo)
            user_register_Usuario.save()
    return render(request, 'MiTiempo/info.html')


def mostrarinfmunicipio(request, id):
    municipio = Municipio.objects.get(municipio_id = id)
    datos_variantes_pueblos = obtenerdatosmunicipio.datos_municipio(str(municipio))
    prob_pre = str(datos_variantes_pueblos[0]) # precipitacion
    descr = str(datos_variantes_pueblos[1])# descripcion
    tmax = str(datos_variantes_pueblos[2]) #tmax
    tmin = str(datos_variantes_pueblos[3]) #tmin
    municipio.precipitaion = prob_pre
    municipio.descripcion = descr
    municipio.tmax = tmax
    municipio.tmin = tmin
    municipio.save()
    if request.user.is_authenticated:
        if request.method == "POST":
            comentario = request.POST['cmd']
            autor = request.user.username
            cms = Comentario(autor = autor, texto = comentario, municipio = municipio )
            cms.save()
            municipio.numcom = municipio.numcom + 1
            municipio.save()

    cms_munis = Comentario.objects.all().filter(municipio = municipio)

    return render(request, 'MiTiempo/infomunicipio.html', {'mun': municipio, 'cms_munis': cms_munis})


def colorfondo(color):
    if int(color) == 1:
        colorfondo = "aqua"
    elif int(color) == 2:
        colorfondo = "red"
    elif int(color) == 3:
        colorfondo = "lime"
    else:
        colorfondo = "http://f1.panorama.com.ve/__export/1460131996960/sites/panorama/img/pitoquito/2016/04/08/cieloprin.jpg_1740910061.jpg"
    return colorfondo


def colorletras(color):
    if int(color) == 1:
        colorletras = "black"
    elif int(color) == 2:
        colorletras = "#0a11f6"
    elif int(color) == 3:
        colorletras = "maroon"
    else:
        colorletras = "purple"
    return colorletras


def tamanoletras(tamano):
    if int(tamano) == 1:
        tamanoletras = 10
    elif int(tamano) == 2:
        tamanoletras = 15
    else:
        tamanoletras = 20
    return tamanoletras


def crearmunicipio(municipio, us):
    name = datos_no_variantes_pueblos[municipio]['nombre']
    lat = datos_no_variantes_pueblos[municipio]['latitud']
    alt = datos_no_variantes_pueblos[municipio]['altitud']
    long = datos_no_variantes_pueblos[municipio]['longitud']
    id = datos_no_variantes_pueblos[municipio]['id']
    id_new = id.split('d')[1]
    n = name.lower()
    n = unidecode(n)
    n = n.split()
    nombre_municipio = ""
    for i in n:
        nombre_municipio += i +"-"
    nombre_municipio = nombre_municipio[0:-1]
    enlace = "http://www.aemet.es/es/eltiempo/prediccion/municipios/"+ nombre_municipio +"-"+ id
    datos_variantes_pueblos = obtenerdatosmunicipio.datos_municipio(str(municipio))
    prob_pre = str(datos_variantes_pueblos[0]) # precipitacion
    descr = str(datos_variantes_pueblos[1])# descripcion
    tmax = str(datos_variantes_pueblos[2]) #tmax
    tmin = str(datos_variantes_pueblos[3]) #tmin

    mun = Municipio(nombre_municipio = name, municipio_id = id ,
                    altitud = alt, latitud = lat, longitud = long, enlace = enlace,
                    precipitaion = prob_pre,descripcion = descr, tmax=tmax, tmin= tmin, id_split = id_new )
    mun.save()
    us.municipios.add(mun)


@csrf_exempt
def pagusuario(request, usuario):
    muni_not_found = False
    municipio = ""
    see_munis = []

    format = request.GET.get('format')
    if format == "xml":
        us = Usuario.objects.get(username = usuario)
        munis = us.municipios.all()
        response = render(request, 'MiTiempo/pagusuario.xml', {'municipios':munis, 'us': us}, content_type = "text/xml")
        return HttpResponse(response, "text/xml")

    if request.user.is_authenticated and request.user.username == usuario:
        us = Usuario.objects.get(username = usuario)
        if request.method == "POST":
            if 'titulo' in request.POST:
                titulo = request.POST['titulo']
                us.titulo = titulo
                us.save()
                return HttpResponseRedirect(str(usuario))
            elif 'municipio' in request.POST:
                municipio = request.POST['municipio']
                try:
                    muni = Municipio.objects.get(nombre_municipio = municipio)
                    boolean_muni = Usuario.objects.filter(username = usuario, municipios__nombre_municipio = muni).exists()
                    if not boolean_muni:
                        us.municipios.add(muni)

                except Municipio.DoesNotExist:
                    ### SI EL MUNICIPIO NO EXSITE LO AÑADO ###
                    if (obtenerdatosmunicipio.datos_municipio(municipio) is None):
                        muni_not_found = True
                        return render(request, 'MiTiempo/pagusuario.html',{'muni_not_found': muni_not_found, 'mun': municipio, 'user': us})
                    else:
                        crearmunicipio(municipio, us)
                        muni_not_found = False

            elif 'quitar_muni' in request.POST:
                muni = request.POST['quitar_muni']
                muni = Municipio.objects.get(nombre_municipio = muni)
                us.municipios.remove(muni)
            elif 'bgcolor' in request.POST:
                bgcolor = request.POST['bgcolor']
                bgcolor = colorfondo(bgcolor)
                user = Usuario.objects.get(username = usuario)
                user.colorfondo = bgcolor
                user.save()
            elif 'cletras' in request.POST:
                cletras = request.POST['cletras']
                cletras = colorletras(cletras)
                user = Usuario.objects.get(username = usuario)
                user.colorletras = cletras
                user.save()
            elif 'tletras' in request.POST:
                tletras = request.POST['tletras']
                tletras = tamanoletras(tletras)
                user = Usuario.objects.get(username = usuario)
                user.tamanoletras = tletras
                user.save()

        if request.method == "GET" or request.method == "POST":
            vacio = False
            municipios = Municipio.objects.all()
            actualizardatos(municipios)
            usu = Usuario.objects.get(username = usuario)
            munis = us.municipios.all()
            for i in reversed(munis):
                see_munis.append(i)
            if munis.count() == 0:
                vacio = True
            return render(request, 'MiTiempo/pagusuario.html',{'username': usuario,
                            'municipios': see_munis, 'user': usu, 'vacio': vacio})
    else:
        try:
            vacio = False
            municipios = Municipio.objects.all()
            actualizardatos(municipios)
            us = Usuario.objects.get(username = usuario)
            munis = us.municipios.all()
            for i in reversed(munis):
                see_munis.append(i)
            if munis.count() == 0:
                vacio = True
            return render(request, 'MiTiempo/pagusuario_no_log.html', {'municipios': see_munis,
                            'username': usuario, 'user': us, 'vacio': vacio})
        except Usuario.DoesNotExist:
            return render(request, 'MiTiempo/pagusuario.html', {'username': usuario})


def changecssuser(request):
    image_url = ""
    us = Usuario.objects.get(username = request.user.username)
    background_color = us.colorfondo
    if background_color != "aqua" and  background_color != "red" and  background_color != "lime":
        image_url = background_color
    color_text = us.colorletras
    font_size = us.tamanoletras
    return render(request, 'MiTiempo/usercss.css', {'background_color':background_color, 'color_text': color_text,
                    'font_size': font_size, 'image_url': image_url},content_type = "text/css")


def listausuarios(request):
    vacio =  False
    if request.user.username != "":
        try:
            superuser = Usuario.objects.get(username=request.user.username)
        except Usuario.DoesNotExist:
            titulo = "Página de "+request.user.username
            user_register_Usuario = Usuario(username=request.user.username, titulo=titulo)
            user_register_Usuario.save()

    usuarios = Usuario.objects.all()
    if Usuario.objects.count() == 0:
        vacio = True
    return render(request, 'MiTiempo/listausuarios.html', {'usuarios': usuarios, 'vacio': vacio})


@csrf_exempt
def listamunicipios(request):
    vacio = False
    mun = Municipio.objects.all()
    dicc_mun_temp = []

    format = request.GET.get('format')
    if format == "xml":
        response = render(request, 'MiTiempo/pagmunicipios.xml', {'municipios':mun}, content_type = "text/xml")
        return HttpResponse(response, "text/xml")

    if request.method == "POST":
        empty = False
        numeromin = request.POST['numeromin']
        numeromax = request.POST['numeromax']
        for i in mun:
            municipio = i.nombre_municipio
            tmax =  obtenerdatosmunicipio.datos_municipio(municipio)
            tmax = tmax[2]
            if tmax <= numeromax and tmax >= numeromin:
                dicc_mun_temp += [i]
        if len(dicc_mun_temp) == 0:
            empty = True
        return render(request, 'MiTiempo/listamunsentretemp.html', {'tmax': numeromax, 'tmin': numeromin,
                    'mun': dicc_mun_temp, 'empty': empty})

    if Municipio.objects.count() == 0:
        vacio = True
    return render(request, 'MiTiempo/listamunicipios.html', {'mun': mun, 'vacio': vacio})


def register(request):
    if request.method == 'GET':
        return render(request, 'MiTiempo/register.html', {})

    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        mail = request.POST.get('email', None)
        if username == "municipios" or username == "info" or username == "usuarios":
            return HttpResponse('<h3>No puede registrarse con este nombre de usuario. Pruebe otro. </h3>'+'<p>Return initial page:\
                                <a href="/register">Página de registro</a></p>')
        try:
            usuario_existente_super_user = User.objects.get(username=username)
            return HttpResponse('<h3>Nombre de usuario existente. Pruebe otro. </h3>'+'<p>Return initial page:\
                                <a href="/register">Página de registro</a></p>')
        except User.DoesNotExist:
            try:
                usuario_existente = Usuario.objects.get(username=username)
                return HttpResponse('<h3>Nombre de usuario existente. Pruebe otro.</h3>'+'<p>Return\
                                        initial page: <a href="/register">Página de registro</a></p>')
            except Usuario.DoesNotExist:
                titulo = "Página de "+username
                user_register_Usuario = Usuario(username = username, email = mail, password = password, titulo = titulo)
                user_register_User = User.objects.create_user(username = username, email = mail, password = password)
                user_register_User.save()
                user_register_Usuario.save()

        return HttpResponse('<h3>Usuario creado</h3>'+'<p>Return initial page: <a href="/">Inicio</a></p>')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
