import getpass
import xmlrpclib
url = 'http://refrigeracion-para-auto-sa-de-cv.odoo.com'
db = 'refrigeracion-para-auto-sa-de-cv'
username = 'miranda.carlos@gmail.com'
password = getpass.getpass("password para "+username+" en "+db+": ")
common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
output = common.version()
# print output
uid=common.authenticate(db,username,password,{})
models=xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

print models.execute_kw(db,uid,password,'res.partner','check_access_rights',['read'],{'raise_exception':False}) # para verificar si tengo acceso a 'read' en el modelo 'res.partner'

# print models.execute_kw(db,uid,password,'res.partner','search',[[["is_company","=",True],["customer","=",True]]]) # el metodo 'search' es como el where en SQL
                                                    # el siguiente parametro de la funcion execute_kw recibe lo que se pone en el where
                                                    # una clausula entre corchetes separadas por coma (de la forma [campo,operador,valor])

# print models.execute_kw(db,uid,password,'res.partner','search',[[]]) # esto es una busqueda sin where

# print models.execute_kw(db,uid,password,'res.partner','search',[[]],{"offset":3,"limit":3}) # no entiendo muy bien pero es para paginar los resultados

# print models.execute_kw(db,uid,password,'res.partner','search_count',[[]])  #sirve para contar los resultados como un count(*) en SQL

# ids=models.execute_kw(db,uid,password,'res.partner','search',[[]],{"limit":1}) #hago una busqueda que regresa solo un id y lo guardo en ids

# ids=models.execute_kw(db,uid,password,'res.partner','search',[[]]) #hago una busqueda que regresa todos los ids y lo guardo en ids

# [record]=models.execute_kw(db,uid,password,'res.partner','read',[ids])
# print record #guardo en [record] la lectura de ese id y lo imprimo

# print models.execute_kw(db,uid,password,'res.partner','read',[ids],{"fields":["name","country_id","comment"]}) # obtengo solo esos 3 campos (columnas) de los ids agarrados antes

# print models.execute_kw(db,uid,password,'res.partner','fields_get',[],{"attributes":["string","help","type"]}) # fields_get obtiene los nombres de los campos del modelo en cuestion,
                                                                    # como regresa mucha informacion se recomienda filtrar
                                                                    # y obtener solo los atributos del campo mas interesantes para el humano, que pudieran ser:
                                                                    # string (el nombre del campo)
                                                                    # help (algunas veces viene texto de ayuda (descripcion))
                                                                    # type (el tipo de dato, para saber que esperar al leer o que enviar al actualizar un registro)

# print models.execute_kw(db,uid,password,"res.partner","search_read",[[]],{"fields":["name","country_id","comment"],"limit":25}) # esto es lo mismo que hacer un search() y luego read()
                                                                                                                                    # de los ids obtenidos en el search()

# id_nuevo=models.execute_kw(db,uid,password,"res.partner","create",[{"name":"Nuevo Partner"}]) # el metodo create() crea un registro nuevo en el modelo y regresa el id nuevo creado
# print id_nuevo

# models.execute_kw(db,uid,password,"res.partner","write",[[15],{"name":"Nuevo actualizado desde API"}]) # esto hace un update al id=15 le cambia el nombre le pone "Nuevo actualizado desde API"
# print models.execute_kw(db,uid,password,"res.partner","search_read",[[["id","=","15"]]],{"fields":["name"]}) # imprimo el campo nombre del id=15

# models.execute_kw(db,uid,password,"res.partner","unlink",[[15]]) # borro el registro con el id=15
# print models.execute_kw(db,uid,password,"res.partner","search_read",[[["id","=","15"]]],{"fields":["name"]}) # imprimo el campo nombre del id=15

# models.execute_kw(db,uid,password,"ir.model","create",[{"name":"Modelo creado desde api 2","model":"x_custom_model2","state":"manual",}]) # creo un modelo nuevo haciendo un create al
                                                                                                                                            # modelo ir.model dado que ir.model es como un
                                                                                                                                            # meta-modelo
# print "\ncampos del modelo product.product:\n"
# print models.execute_kw(db,uid,password,'ir.model',"search_read",[[]],{"fields":["name","model"]})
# print models.execute_kw(db,uid,password,"product.product","fields_get",[],{})
# print models.execute_kw(db,uid,password,"product.product","search_read",[[['list_price','>=','3'],['list_price','<=','9']]],{"fields":["code","list_price"]})
# models.execute_kw(db,uid,password,"product.product","write",[[4424],{"website_public_price":"5.64"}])
# print models.execute_kw(db,uid,password,"product.product","search_read",[[["website_public_price","<",6]]],{"fields":["code","website_public_price","display_name"],"limit":10})
# print models.execute_kw(db,uid,password,"product.product","search_read",[[["website_public_price","<","3"]]],{"fields":["code","website_public_price"],"limit":5})
# print models.execute_kw(db,uid,password,'product.product','search_count',[[["website_public_price","<",2]]])
# id=models.execute_kw(db,uid,password,'product.product','search',[["code"]],{"limit":1})
# id=models.execute_kw(db,uid,password,"product.product","search",[[]])
# print (id)
# models.execute_kw(db,uid,password,"product.product","write",[id,{"website_size_y":2}])
# print models.execute_kw(db,uid,password,"product.product","search_read",[[["default_code","=","CP9966"]]])
id=models.execute_kw(db,uid,password,"product.product","search",[[["default_code","=","AC17580"]]])
print(id)
if id==[]:
    print("agarraste al maldito!!")
