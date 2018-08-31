import base64
from lxml import etree
from pathlib import Path
import urllib
import getpass
import os
import pymssql
import subprocess
from urllib.request import urlretrieve
rutaLocal="/Users/cmiranda/Documents/almacenPython/imagenes/"
c_art=0
user= input("usuario de la base de datos: ")
password=getpass.getpass("password de la base de datos: ")
rutaURL="http://www.refriauto.com.mx/2015/img/Articulos/"
conn=pymssql.connect("192.168.10.5",user,password,"dbSIA")
cursor = conn.cursor()
query="select top 75 aen.encriptado,replace(art.DescripcionArticulo,',','') "
query+=",round(apv.PrecioVenta*(select top 1 TipoDeCambioVentas from tbSucursalesTiposDeCambio order by idSucursalTipoDeCambio desc)*art.factorDeOferta*1.16,2) "
query+="    ,'Producto almacenable',rtrim(agr.DescripcionGrupo),alm.Existencias,sys.fn_varbintohexsubstring(0, HashBytes('SHA1',rtrim(art.CodigoArticulo)), 1, 0)+'.jpg' "
query+="from tbarticulos art,tbarticulosencriptados aen,tbAlmacenes alm,tbArticulosPreciosVenta apv,tbarticulosgrupos agr "
query+="where art.idarticulo=alm.idarticulo and aen.idarticulo=art.idArticulo and apv.idArticulo=art.idArticulo and agr.idArticuloGrupo=art.idGrupo "
query+="    and alm.idSucursal=1 and alm.idAlmacenTipo=1 and apv.idTipoDePrecio=1 and art.idGrupo=43 and art.status='AC' "
query+="    and aen.encriptado>'VL9719' "
query+="     "
query+="order by aen.encriptado "
cursor.execute(query)
archivoCSV="/Users/cmiranda/Documents/Gpython/cosasParaOdoo/idGrupo43_9.csv"
if os.path.isfile(archivoCSV):
    os.remove(archivoCSV)
ar_csv=open(archivoCSV,"w")
ar_csv.write("Referencia interna,Nombre,Precio de venta,Tipo de producto,Categoria del producto,Cantidad a mano,Imagen\n")
row = cursor.fetchone()
while row:
    try:
        c_art+=1
        urllib.request.urlretrieve(rutaURL+row[6],rutaLocal+row[6])
        archivo = Path(rutaLocal+row[6])
        if archivo.is_file():
            print("procesando "+row[0]+' '+row[6]+' procesamiento numero '+str(c_art))
            with open(rutaLocal+row[6],"rb") as imagen:
                ar_csv.write(str(row[0])+','+str(row[1])+','+str(row[2])+','+str(row[3])+','+str(row[4])+','+str(row[5])+','+str(base64.b64encode(imagen.read()).decode("ascii"))+'\n')
        else:
            archivo=Path("/Users/cmiranda/Downloads/isotipo01.jpg")
            if archivo.is_file():
                print("no tengo foto de "+row[0]+' procesamiento numero '+str(c_art))
                with open("/Users/pohvak/Downloads/isotipo01.jpg","rb") as imagen:
                    ar_csv.write(str(row[0])+','+str(row[1])+','+str(row[2])+','+str(row[3])+','+str(row[4])+','+str(row[5])+','+str(base64.b64encode(imagen.read()).decode("ascii"))+'\n')
    except Exception:
        pass
    row = cursor.fetchone()
conn.close()
ar_csv.close()
print("he terminado")
