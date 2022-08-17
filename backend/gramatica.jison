

    sentencia:  declaracionVector TK_PUNTOYCOMA  {$$=$1}
                |if                             {$$=$1}
                |switch                         {$$=$1}
                |while                          {$$=$1}
                |do_while                       {$$=$1}
                |for                            {$$=$1}
                |funcion                        {$$=$1}
                |metodo                         {$$=$1}
                |llamada                        {$$=$1}
                |incremento TK_PUNTOYCOMA       {$$=$1}
                |decremento TK_PUNTOYCOMA       {$$=$1}
                |return                         {$$=$1}
                |pps TK_PUNTOYCOMA                           {$$=$1}
                |modificarVector TK_PUNTOYCOMA  {$$=$1}       
                |ternario TK_PUNTOYCOMA         {$$=$1}
                |graficar TK_PUNTOYCOMA         {$$=$1}
                |TK_BREAK TK_PUNTOYCOMA         {$$=new Nodo_AST("Break", "break", this._$.first_line, @1.first_column)}
                |TK_CONTINUE TK_PUNTOYCOMA      {$$=new Nodo_AST("Continue", "continue", this._$.first_line, @1.first_column)}
                | error TK_PUNTOYCOMA {console.log("aqui hay un error")};

    
    ternario: expresion TK_TERNARIO ei TK_DOSPUNTOS ei {$$= new Nodo_AST("Ternario", "Ternario", this._$.first_line, @1.first_column); $$.agregarHijo($1, $3, $5)};

    ei: expresion   {$$=$1}
        |print      {$$=$1}
        |asignacion {$$=$1};
    
    pps:    TK_ID TK_PUNTO TK_POP TK_PARENTESISA TK_PARENTESISC {$$ = new Nodo_AST("Pop", "pop", this._$.first_line, @1.first_column); $$.agregarHijo(new Nodo_AST("ID", $1, this._$.first_line, @1.first_column))}
            | TK_ID TK_PUNTO TK_PUSH TK_PARENTESISA expresion TK_PARENTESISC {$$ = new Nodo_AST("Push", "push", this._$.first_line, @1.first_column); $$.agregarHijo(new Nodo_AST("ID", $1, this._$.first_line, @1.first_column), $5)}
            |TK_ID TK_PUNTO TK_SPLICE TK_PARENTESISA expresion TK_COMA expresion TK_PARENTESISC {{$$ = new Nodo_AST("Splice", "splice", this._$.first_line, @1.first_column); $$.agregarHijo(new Nodo_AST("ID", $1, this._$.first_line, @1.first_column), $5 , $7)}};

    declaracionVector:  tipo_dato TK_ID TK_CORCHETEA TK_CORCHETEC TK_ASIGNACION TK_NEW tipo_dato TK_CORCHETEA TK_NUMERO TK_CORCHETEC {$$= new Nodo_AST("DeclaracionV", "DeclaracionV", this._$.first_line, @1.first_column); $$.agregarHijo($1, new Nodo_AST("ID",$2, this._$.first_line, @2.first_column), $7, new Nodo_AST("Numero", $9, this._$.first_line, @9.first_column))}
                        |tipo_dato TK_ID TK_CORCHETEA TK_CORCHETEC TK_ASIGNACION TK_CORCHETEA lista_expresiones TK_CORCHETEC {$$= new Nodo_AST("DeclaracionV", "DeclaracionV", this._$.first_line, @1.first_column); $$.agregarHijo($1, new Nodo_AST("ID",$2, this._$.first_line, @2.first_column), $7)}
                        |tipo_dato TK_ID TK_CORCHETEA TK_CORCHETEC TK_ASIGNACION TK_CHARARRAY TK_PARENTESISA expresion TK_PARENTESISC {$$= new Nodo_AST("DeclaracionV", "DeclaracionV", this._$.first_line, @1.first_column); $$.agregarHijo($1, new Nodo_AST("ID",$2, this._$.first_line, @2.first_column), new Nodo_AST("CharArray",$6, this._$.first_line, @6.first_column), $8)}
                        |tipo_dato TK_ID TK_CORCHETEA TK_CORCHETEC TK_CORCHETEA TK_CORCHETEC TK_ASIGNACION TK_NEW tipo_dato TK_CORCHETEA TK_NUMERO TK_CORCHETEC TK_CORCHETEA TK_NUMERO TK_CORCHETEC {$$= new Nodo_AST("DeclaracionV2", "DeclaracionV2", this._$.first_line, @1.first_column); $$.agregarHijo($1, new Nodo_AST("ID",$2, this._$.first_line, @2.first_column), $9, new Nodo_AST("Filas", $11, this._$.first_line, @11.first_column), new Nodo_AST("Columnas", $14, this._$.first_line, @14.first_column))}
                        |tipo_dato TK_ID TK_CORCHETEA TK_CORCHETEC TK_CORCHETEA TK_CORCHETEC TK_ASIGNACION  TK_CORCHETEA lista_vectores TK_CORCHETEC {$$= new Nodo_AST("DeclaracionV2", "DeclaracionV2", this._$.first_line, @1.first_column); $$.agregarHijo($1, new Nodo_AST("ID",$2, this._$.first_line, @2.first_column), $9)};

                    |TK_CONST tipo_dato lista_variables declaracionAsignacion TK_PUNTOYCOMA {$$= new Nodo_AST("Declaracion", "Declaracion", this._$.first_line, @1.first_column); $$.agregarHijo(new Nodo_AST("Constante", "const", this._$.first_line, @1.first_column),$2,$3,$4)};

    lista_vectores:     lista_vectores TK_COMA TK_CORCHETEA lista_expresiones TK_CORCHETEC {$1.agregarHijo($4);$$=$1}
                        |TK_CORCHETEA lista_expresiones TK_CORCHETEC  {$$=new Nodo_AST("ExpresionesV","ExpresionesV",this._$.first_line,@1.last_column); $$.agregarHijo($2)}; 

    accesoVector:   TK_ID TK_CORCHETEA expresion TK_CORCHETEC {$$=new Nodo_AST("Vector", "Vector", this._$.first_line,@2.last_column); $$.agregarHijo(new Nodo_AST("ID", $1, this._$.first_line,@1.last_column), $3)}
                    |TK_ID TK_CORCHETEA expresion TK_CORCHETEC TK_CORCHETEA expresion TK_CORCHETEC {$$=new Nodo_AST("Vector2D", "Vector2D", this._$.first_line,@2.last_column); $$.agregarHijo(new Nodo_AST("ID", $1, this._$.first_line,@1.last_column), $3, $6)};

    modificarVector:    accesoVector TK_ASIGNACION expresion {$$= new Nodo_AST("Modificar Vector", "Modificar Vector", this._$.first_line,@2.last_column); $$.agregarHijo($1, $3)};

    graficar: TK_GRAFICAR TK_PARENTESISA TK_PARENTESISC {$$ = new Nodo_AST("Graficar", "graficar_ts", this._$.first_line, @1.first_column); };

   
    if: TK_IF TK_PARENTESISA expresion TK_PARENTESISC encapsulado {$$= new Nodo_AST("If","If",this._$.first_line,@1.last_column);$$.agregarHijo($3,$5)}
        |TK_IF TK_PARENTESISA expresion TK_PARENTESISC encapsulado TK_ELSE else {$$= new Nodo_AST("If","If",this._$.first_line,@1.first_column); $$.agregarHijo($3,$5,$7)}
        | TK_IF TK_PARENTESISA expresion TK_PARENTESISC sentencia {$$= new Nodo_AST("If","If",this._$.first_line,@1.last_column);$$.agregarHijo($3,$5)}
        | TK_IF TK_PARENTESISA expresion TK_PARENTESISC sentencia TK_ELSE else{$$= new Nodo_AST("If","If",this._$.first_line,@1.first_column);$$.agregarHijo($3,$5,$7)};

    else:   if {$$= new Nodo_AST("Else","Else",this._$.first_line,@1.last_column); $$.agregarHijo($1)}
            |encapsulado {$$= new Nodo_AST("Else","Else",this._$.first_line,@1.last_column); $$.agregarHijo($1)}
            | sentencia {$$= new Nodo_AST("Else","Else",this._$.first_line,@1.last_column); $$.agregarHijo($1)};

    switch: TK_SWITCH TK_PARENTESISA expresion TK_PARENTESISC TK_LLAVEA casos TK_LLAVEC {$$= new Nodo_AST("Switch","Switch",this._$.first_line,@1.last_column); $$.agregarHijo($3,$6)};

    casos:  casos TK_CASE expresion TK_DOSPUNTOS sentencias TK_BREAK TK_PUNTOYCOMA {var temp = new Nodo_AST("Caso","Caso",this._$.first_line,@1.last_column); temp.agregarHijo($3,$5,new Nodo_AST("Break", "Break", this._$.first_line, @6.first_column)); $1.agregarHijo(temp);$$=$1;}
            |casos TK_DEFAULT TK_DOSPUNTOS sentencias TK_BREAK TK_PUNTOYCOMA {var temp = new Nodo_AST("Caso","Caso",this._$.first_line,@1.last_column); temp.agregarHijo(new Nodo_AST("Default", "Default", this._$.first_line,@1.last_column),$4, new Nodo_AST("Break", "Break", this._$.first_line, @5.first_column)); $1.agregarHijo(temp);$$=$1;}
            |casos TK_CASE expresion TK_DOSPUNTOS sentencias {var temp = new Nodo_AST("Caso","Caso",this._$.first_line,@1.last_column); temp.agregarHijo($3,$5); $1.agregarHijo(temp);$$=$1;}
            |casos TK_DEFAULT TK_DOSPUNTOS sentencias {var temp = new Nodo_AST("Caso","Caso",this._$.first_line,@1.last_column); temp.agregarHijo(new Nodo_AST("Default", "Default", this._$.first_line,@1.last_column),$4); $1.agregarHijo(temp);$$=$1;}
            |TK_CASE expresion TK_DOSPUNTOS sentencias TK_BREAK TK_PUNTOYCOMA {$$=new Nodo_AST("Casos","Casos");var temp = new Nodo_AST("Caso","Caso",this._$.first_line,@1.last_column); temp.agregarHijo($2,$4, new Nodo_AST("Break", "Break", this._$.first_line, @5.first_column));$$.agregarHijo(temp)}
            |TK_DEFAULT TK_DOSPUNTOS sentencias TK_BREAK TK_PUNTOYCOMA {$$=new Nodo_AST("Casos","Casos"); var temp = new Nodo_AST("Caso","Caso",this._$.first_line,@1.last_column); temp.agregarHijo(new Nodo_AST("Default", "Default", this._$.first_line,@1.last_column),$3), $$.agregarHijo(temp)};
            

    while:  TK_WHILE TK_PARENTESISA expresion TK_PARENTESISC encapsulado {$$=new Nodo_AST("While","While",this._$.first_line,@1.last_column); $$.agregarHijo($3,$5)};

    do_while:   TK_DO encapsulado TK_WHILE TK_PARENTESISA expresion TK_PARENTESISC TK_PUNTOYCOMA {$$=new Nodo_AST("Do-While","Do-While",this._$.first_line,@1.last_column); $$.agregarHijo($2,$5)};

    for:    TK_FOR TK_PARENTESISA da TK_PUNTOYCOMA expresion TK_PUNTOYCOMA actualizacion TK_PARENTESISC encapsulado {$$=new Nodo_AST("For","For",this._$.first_line,@1.last_column); $$.agregarHijo($3,$5,$7,$9)};

    da: tipo_dato TK_ID TK_ASIGNACION expresion {$$=new Nodo_AST("Declaracion","Declaracion",this._$.first_line,@1.last_column);$$.agregarHijo($1, new Nodo_AST("ID", $2,this._$.first_line,@2.last_column),$4)}
        | TK_ID TK_ASIGNACION expresion{$$=new Nodo_AST("Asignacion","Asignacion",this._$.first_line,@1.last_column);$$.agregarHijo(new Nodo_AST("ID", $1,this._$.first_line,@1.last_column),$3)};

    actualizacion:  TK_ID TK_ASIGNACION expresion {$$=new Nodo_AST("Asignacion","Paso",this._$.first_line,@1.last_column);$$.agregarHijo(new Nodo_AST("ID", $1,this._$.first_line,@1.last_column),$3)}
                    | TK_ID TK_INCREMENTO {$$=new Nodo_AST("Incremento", "Incremento");$$.agregarHijo(new Nodo_AST("ID", $1, this._$.first_line, @1.first_column))}
                    | TK_ID TK_INCREMENTO {$$=new Nodo_AST("Decremento", "Decremento");$$.agregarHijo(new Nodo_AST("ID", $1, this._$.first_line, @1.first_column))};

    funcion:    tipo_dato TK_ID conjunto encapsulado {$$=new Nodo_AST("Funcion", "Funcion"); $$.agregarHijo($1,new Nodo_AST("ID", $2, this._$.first_line,@2.last_column),$3,$4)};

    conjunto:   TK_PARENTESISA parametros TK_PARENTESISC {$$=$2}
                |TK_PARENTESISA TK_PARENTESISC {$$=new Nodo_AST("Parametros","Parametros",this._$.first_line,@1.last_column)};

    parametros: parametros TK_COMA tipo_dato TK_ID {$1.agregarHijo($3, new Nodo_AST("ID", $4, this._$.first_line,@4.last_column));$$=$1}
                | tipo_dato TK_ID  {$$=new Nodo_AST("Parametros","Parametros",this._$.first_line,@1.last_column); $$.agregarHijo($1, new Nodo_AST("ID", $2, this._$.first_line,@2.last_column))};

    metodo: TK_VOID TK_ID conjunto encapsulado {$$=new Nodo_AST("Metodo", "Metodo"); $$.agregarHijo(new Nodo_AST("Void", "void", this._$.first_line,@1.last_column),new Nodo_AST("ID", $2, this._$.first_line,@2.last_column),$3,$4)};

    print:  TK_IMPRIMIR TK_PARENTESISA expresion TK_PARENTESISC  {$$=new Nodo_AST("Print", "Print", this._$.first_line,@1.last_column);$$.agregarHijo($3)}
            |TK_IMPRIMIRLN TK_PARENTESISA expresion TK_PARENTESISC {$$=new Nodo_AST("Println", "Println", this._$.first_line,@1.last_column);$$.agregarHijo($3)};

    llamada: TK_CALL TK_ID conjunto_llamada TK_PUNTOYCOMA {$$=new Nodo_AST("Llamada", "Llamada", this._$.first_line,@1.last_column);$$.agregarHijo(new Nodo_AST("ID", $2, this._$.first_line,@1.last_column),$3)};

    conjunto_llamada:   TK_PARENTESISA parametros_llamada TK_PARENTESISC {$$=$2}
                        |TK_PARENTESISA TK_PARENTESISC {$$=new Nodo_AST("Parametros", "Parametros",this._$.first_line,@1.last_column)};

    parametros_llamada: parametros_llamada TK_COMA expresion {$1.agregarHijo($3), $$=$1}
                |expresion  {$$=new Nodo_AST("Parametros", "Parametros",this._$.first_line,@1.last_column);$$.agregarHijo($1)};

    return: TK_RETURN expresion TK_PUNTOYCOMA {$$=new Nodo_AST("Return", "Return", this._$.first_line,@1.last_column); $$.agregarHijo($2)}
            | TK_RETURN TK_PUNTOYCOMA {$$=new Nodo_AST("Return", "Return", this._$.first_line,@1.last_column)};

    expresion:  |accesoVector                               {$$=new Nodo_AST("Expresion","Expresion",this._$.first_line,@1.last_column); $$.agregarHijo($1)}
                |TK_ID TK_PUNTO TK_INDEXOF TK_PARENTESISA expresion TK_PARENTESISC  {$$=new Nodo_AST("Expresion","Expresion",this._$.first_line,@1.last_column); $$.agregarHijo(new Nodo_AST("ID",$1, this._$.first_line, @1.first_column), new Nodo_AST("indexof",$3, this._$.first_line, @2.first_column), $5)}
                |TK_ID conjunto_llamada             {$$= new Nodo_AST("Expresion","Expresion",this._$.first_line,@1.first_column); var temp =  new Nodo_AST("Llamada", "Llamada", this._$.first_line,@1.last_column); temp.agregarHijo(new Nodo_AST("ID", $1, this._$.first_line,@1.last_column),$2); $$.agregarHijo(temp)}
                |incremento                         {$$=new Nodo_AST("Expresion","Expresion",this._$.first_line,@1.last_column); $$.agregarHijo($1)}
                |decremento                         {$$=new Nodo_AST("Expresion","Expresion",this._$.first_line,@1.last_column); $$.agregarHijo($1)}
                |ternario                           {$$=new Nodo_AST("Expresion","Expresion",this._$.first_line,@1.last_column); $$.agregarHijo($1)}
                