import sys

#-------------------------------
#      Simbolos importantes
#-------------------------------
izquierda = "L"
derecha = "R"
go = {izquierda:"L", derecha:"R"}
acepta = "qacc"
rechaza = "qrej"
blanco = "B"


#-------------------------------
#      Archivo de entrada
#-------------------------------
#filename = "suma.csv"
filename = sys.argv[1]

# abrir archivo
f = open(filename)
# leer todas las lineas y guardarlas en t
t = f.readlines()
# cerrar archivo
f.close()


#-------------------------------
#      Construccion de tabla
#-------------------------------

# parametros = lo que hay en la cinta
parametros = t[0].strip("\n").split(",")
#Quitar elementos vacios producidos por las comas extra
parametros = list(filter(None, parametros))
#cantidad de parametros
p = len(parametros)
#cantidad de estados e = estados
e = len(t) - 1

tabla = []
#el primer renglon de la tabla son los parametros
tabla.append(parametros)


for i in range(e):
    #cada renglon tiene un estado y varias "tripletas" que representan una transición
    renglon = []
    #para cada renglon (exepto el primero) del archivo de lectura, se separan todos los elementos
    aux = t[i+1].strip("\n").split(",")
    #se desea hacer grupos (celdas), en la celda 1 siempre habra un solo elemento que es el estado
    #aux[0] es el estado
    renglon.append(aux[0])
    #recorrer el renglon leido del archivo original, no se toma en cuenta el primer renglon y se avanza de 3 en
    # 3 para generar las trancisiones
    for k in range(1,len(aux),3):
        #agrupar en una celda lo que se escribe, movimiento y estado destino
        celda = []
        celda.append(aux[k+0])
        celda.append(aux[k+1])
        celda.append(aux[k+2])
        #se agrega la celda a el renglon correspondiente a cada estado
        renglon.append(celda)
    #se agrega un renglon por estado a la tabla
    tabla.append(renglon)

#eliminar variable t, ganar algo de memoria
del t


#-------------------------------
# Diccionario de trancisiones
#-------------------------------

#Estado inicial = q0
estado_inicial = tabla[1][0]
#Convertir la tabla en un diccionario
dicc_tabla = {}


#acceder a cada celda de la tabla, saltandose los parametros y los nombres de los estados
# i = renglones ; j = columnas
for i in range(len(tabla)):
    for j in range(len(tabla[0])+1):
        #saltarse parametros y estados
        if i == 0 or j == 0:
            continue
        elif tabla[i][j] == "":
            continue
        #acomodar
        tabla[i][j][0], tabla[i][j][2] = tabla[i][j][2], tabla[i][j][0]
        tabla[i][j][1], tabla[i][j][2] = tabla[i][j][2], tabla[i][j][1]
        #llave nueva para el diccionario
        clave = (tabla[i][0],tabla[0][j-1])
        #argumento  para cada clave
        contenido = ""
        contenido += tabla[i][j][1] + " "
        contenido += tabla[i][j][0] + " "
        contenido += go[tabla[i][j][2]] + " "
        #nuevo elemento en el diccionario
        dicc_tabla[clave] = contenido

# liberar memoria
del tabla


#-------------------------------
#      Cadena a leer
#-------------------------------

cad = sys.argv[2]
#cad = "1111B1111BB"
print("Cadena original: ",cad)
#separar la cadena en caracteres/simbolos de cinta
cadena = list(cad)
#ordenar para trabajar con la cinta
cadena.reverse()
l = []


#----------------------------------------------------------------
#-------------------------------
#            Cinta
#-------------------------------


def imprimir_cinta(l, cadena):
    #se debe invertir la cadena o parte "derecha"
    cadena.reverse()

    ss = []
    ss.extend(l)
    ss.extend('*')
    ss.extend(cadena)
    #convertir todos los elementos de la lista ss a un string
    str1 = ''
    ss = (str1.join(ss))
    print(ss)

def imprimir_cinta_rechazo(l, cadena):

    cadena.reverse()
    #se debe invertir la cadena o parte "derecha"
    ss = []
    ss.extend(l)
    ss.extend('*')
    ss.extend(cadena)
    #convertir todos los elementos de la lista ss a un string
    str1 = ''
    ss = (str1.join(ss))
    return ss



#imprimir_cinta(l.copy(), cadena.copy())
#-----------------------------------------------------------------

#-------------------------------
#      Interprete
#-------------------------------


#estado inicial
estado = estado_inicial

while True:
    #si no hay ningun simbolo de cinta, entonces se esta leyendo un espacio en blanco
    if len(cadena) == 0:
        caracter = blanco
    else:
        #se saca el ultimo caracter de la lista cadena, como la lista esta volteada, se esta
        #trabajando con el primer caracter de la cinta
        caracter = cadena.pop()
    #existe una trancision valida con el estado en que se esta y el caracter leido?
    try:
        #si existe; obtener las "acciones" (lo que se escribe, destino, movimiento)
        trancision = dicc_tabla[(estado, caracter)].split(" ")
    except:
        #no existe una trancision valida
        print("\nreject")
        print("No existe una trancisión valida, Pozo")
        #parar ciclo while
        exit(0)
    #se escribe, segun trancision(puede ser un reemplazo)
    caracter = trancision[0]
    #estado destino será el nuevo estado
    nuevo_estado = trancision[1]
    #Movimiento en la cinta
    if trancision[2] == "R":
        l.append(caracter)
    else:
        cadena.append(caracter)
        if len(l) == 0:
            caracter = blanco
        else:
            caracter = l.pop()
        cadena.append(caracter)
#    imprimir_cinta(l.copy(), cadena.copy())
    #actualizar estado
    estado = nuevo_estado

    #se llego a un estado de parada y aceptacion
    if estado == acepta:
        imprimir_cinta(l, cadena)
        print("accept")
        #parar ciclo while
        exit(0)
    #se llego a un estado de parada y rechazo
    elif estado == rechaza:
        #si se rechaza la cadena, es posible que existan simbolos auxiliares
        resultado_aux1 = imprimir_cinta_rechazo(l, cadena)
        #cambiar el simbolo auxiliar "d" por "1"
        resultado_aux2 = resultado_aux1.replace("d", "1")
        #cambiar el simbolo auxiliar "e" por "0"
        resultado = resultado_aux2.replace("e", "0")
        print(resultado)
        print("reject")
        #parar ciclo while
        exit(0)
