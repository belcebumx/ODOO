import getpass
import xmlrpclib
import pymssql
def syncProduct(product,price,username,password):
    url = 'http://refrigeracion-para-auto-sa-de-cv.odoo.com'
    db = 'refrigeracion-para-auto-sa-de-cv'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    output = common.version()
    uid=common.authenticate(db,username,password,{})
    models=xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    if models.execute_kw(db,uid,password,'res.partner','check_access_rights',['read'],{'raise_exception':False}):
        id=models.execute_kw(db,uid,password,"product.product","search",[[["default_code","=",product]]])
        if id==[]:
            print("product "+product+" dont exists")
        else:
            models.execute_kw(db,uid,password,"product.product","write",[id[0],{"list_price":price}])
def syncGroup():
    server=raw_input("SQL server: ")
    user=raw_input("SQL user: ")
    dbSQL=raw_input("SQL database: ")
    passSQL=getpass.getpass("SQL password: ")
    username = raw_input("ODOO user: ")
    passODOO = getpass.getpass("ODOO "+username+" password: ")
    d_Group=raw_input("group to sync: ")
    conn=pymssql.connect(server,user,passSQL,dbSQL)
    c_art=0
    cursor = conn.cursor()
    query="select aen.encriptado,round(apv.PrecioVenta*stc.TipoDeCambioVentas*1.16*art.factorDeOferta,2) precio "
    query+="from tbarticulos art,tbarticulospreciosventa apv,tbarticulosgrupos agr,tbtiposdeprecios tdp,tbarticulosencriptados aen,tbSucursalesTiposDeCambio stc "
    query+="where art.idarticulo=apv.idarticulo and agr.idArticuloGrupo=art.idGrupo and aen.idarticulo=art.idArticulo and apv.idtipodeprecio=tdp.idTipoDePrecio and tdp.DescripcionTipoDePrecio='CONTADO PUBLICO' and agr.DescripcionGrupo='"+d_Group+"' and art.status='AC' "
    query+="    and stc.idSucursalTipoDeCambio=(select top 1 idSucursalTipoDeCambio from tbSucursalesTiposDeCambio order by Fecha_UltimaModificacionANSI desc,Hora_UltimaModificacion desc) "
    query+="order by aen.encriptado "
    cursor.execute(query)
    row = cursor.fetchone()
    while row:
        c_art+=1
        print("synchronizing "+row[0]+" "+str(c_art))
        syncProduct(row[0],row[1],username,passODOO)
        row = cursor.fetchone()
    conn.close()
    print("sync complete")
