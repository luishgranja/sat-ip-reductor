import glob

output = ''

# Funcion que se encarga de verificar como empieza cada linea
def header_reader(line):
    comments = ''
    clausoles_aux = ''
    aux = line[0] # Primer caracter de la linea
    if(len(line) > 2):
	    car = line.split()[-1]
	    if(aux == 'c'):# Se verifica si la linea es un comentario
	        aux_comment = line.split('c')[1]
	        comments += f'% {aux_comment}\n'
	        s.write(comments)
	    elif(aux == 'p'): # Se verifica si la linea es 'p', que describe el problema
	        literals_and_constraints(int(line.split()[2])) # Se envia el numero de literales para construir las variables de los literales
	        s.write('\n% Clausulas\n')
	    elif(car == '0' and len(line)>1):
	        clausoles_aux += clausoles(line)
	        s.write(clausoles_aux)

# Funcion para transformar las clausulas (escribe una clausula a la vez)
def clausoles(line):
    c = 'constraint '
    line_aux = line.split()
    for x in range(0, len(line_aux)-1):
        if int(line_aux[x]) > 0: # Verificar si el numero es positivo para asignar nombre de variable
            var = str(line_aux[x])
            c += f'v{var} >= 1;\n' if x == len(line_aux)-2 else f'v{var} + ' # Verificar si es la ultima clausula para poner el ; y >=1               
        else:
            var = str(int(line_aux[x]) * -1)
            c += f'n_v{var} >= 1;\n' if x == len(line_aux)-2 else f'n_v{var} + '
    return c

# Construir literales y constraints
def literals_and_constraints(n_literals):
    literals = '' # Variable para almacenar los literales
    constraints = '\n% Valores asociados a los literales\n' # Variable para almacenar los constraints, valor: header
    global output
    output = 'output [' # Variable para guardar el output del resultado en la conversion de minizinc
    for x in range(1, n_literals+1): # Ciclo para construir los literales, sus negaciones y los constraints de cada literal
        var = str(x)
        literals += f'var 0..1: v{var}; var 0..1: n_v{var};\n'
        constraints += f'constraint v{var} + n_v{var} = 1;\n'
        if x == n_literals: # Verificar si es la ultima iteracion para delar de poner las comas y poner un ]
            output += f'"\\nv{var}=" ,show(v{var}), "\\t-v{var}=", show(n_v{var})]'
            break
        output += f'"v{var}=" ,show(v{var}), "\\t-v{var}=", show(n_v{var}),' if x == 0 else f'"\\nv{var}=" ,show(v{var}), "\\t-v{var}=", show(n_v{var}),'



    s.write(literals) # Se escribe en el archivo los literales
    s.write(constraints) # Se escribe en el archivo los constraints


instances = glob.glob('../InstanciasSAT/*.cnf') # Lista con las rutas de las instancias

for instance in instances:
    
    f = open(instance, "r") # buffer para archivo de entrada
    s = open('../InstanciasMiniZinc/' + instance.strip('../InstanciasSAT/') + '.mzn',"w+") # buffer para archivo de salida

    # Ciclo donde se lleva a cabo la lectura del archivo
    for line in f:
        header_reader(line)


    s.write('\nsolve satisfy;\n')
    s.write('\n' + output + '\n')

    s.close()
    f.close()
