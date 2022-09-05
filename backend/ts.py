from webbrowser import open_new_tab


class Simbolo():

    def __init__(self, id, valor,  tipoSimbolo, tipoDato, ambito, mutable, linea, columna):
        self.id = id
        self.valor = valor
        self.tipoSimbolo = tipoSimbolo
        self.tipoDato = tipoDato
        self.ambito = ambito
        self.mutable = mutable
        self.linea = linea
        self.columna = columna
        self.capacidad = None
        self.modulo = []

class TablaSimbolos():
    def __init__(self):
        self.simbolos = []
        self.nombre = "Local"
        self.isFuncion = False
        self.isMetodo = False
        self.isWhile = False
        self.isFor = False
        self.retorno = None
        self.isContinue = False
        self.isReturn = False
        self.isBreak = False
        self.isLoop = False

    def ingresar(self, simbolo):
        self.simbolos.append(simbolo)

    def limpiar(self):
        self.simbolos = []

    def modificar(self, tsimbolo):
        res = 0
        for simbolo in self.simbolos:
            if(simbolo.id == tsimbolo.id):
                simbolo.valor = tsimbolo.valor
                res = True
        return res

    def obtener(self, id):
        res = 0
        if len(self.simbolos) == 0:
            return res
        else:
            for simbolo in self.simbolos:
                if(simbolo.id == id):
                    res=simbolo
            return res
    
    def longitud(self):
        return len(self.simbolos)
    
    def eliminar(self, id):
        for i in range(len(self.simbolos)):
            if(self.simbolos[i].id == id):
                self.simbolos.pop(i)
    
    def generarHTML(self):
        if(len(self.simbolos) == 0):
            print("no se ha analizado el archivo o no hay variables a mostrar")
        else:
            parte1 ='''<!DOCTYPE html>
                <html>
                <head>
                <style>
                body {
                background-image: url('https://www.wallpapertip.com/wmimgs/40-405583_high-resolution-white-background-hd.jpg');
                background-repeat: no-repeat;
                background-attachment: fixed;  
                background-size: cover;
                }
                .footer {
                position: absolute;
                left: 0;
                bottom: 1;
                width: 100%;
                background-color: #D0D0D0;
                color: black;
                text-align: left ;
                }
                table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 40%;
                margin: auto;
                }
                h2 {
                    text-align: center;
                }
                h1 {
                    text-align: center;
                }

                td, th {
                border: 1px solid #dddddd;
                text-align: center;
                padding: 8px;
                }

                tr:nth-child(even) {
                background-color: #dddddd;
                }
                </style>
                </head>
                <body>

                <h1>Tabla de Simbolos</h1>

                <table >
                <tr>
                    <th>No.</th>
                    <th>Identificador</th>
                    <th> Valor </th>
                    <th>Tipo Simbolo</th>
                    <th>Tipo Dato</th>
                    <th>Mutable</th>
                    <th>Ambito</th>
                    <th>Linea</th>
                    <th>Columna</th>
                </tr>'''
            parte2 = ""
            conteo=1;

            for simbolo in self.simbolos:
                parte2+="<tr>\n"
                parte2+="<td>"+str(conteo)+"</td>\n";
                parte2+="<td>"+simbolo.id+"</td>\n";
                parte2+="<td>"+str(simbolo.valor)+"</td>\n";
                parte2+="<td>"+simbolo.tipoSimbolo+"</td>\n";
                parte2+="<td>"+str(simbolo.tipoDato)+"</td>\n";
                parte2+="<td>"+str(simbolo.mutable)+"</td>\n";
                parte2+="<td>"+simbolo.ambito+"</td>\n";
                parte2+="<td>"+str(simbolo.linea)+"</td>\n";
                parte2+="<td>"+str(simbolo.columna)+"</td>\n";
                parte2+="</tr>";
                conteo+=1

            parte3="</table>\n</body>\n</html>";

            file = open("reporteTS.html", "w")
            file.write(parte1+parte2+parte3)
            file.close()
            open_new_tab("reporteTS.html")

