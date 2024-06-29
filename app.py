from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost:3306/comision_24169'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Servicios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(50))
    cuit=db.Column(db.Integer)
    fecha=db.Column(db.Integer)
    encargo=db.Column(db.String(400))
    
    def __init__(self,cliente,cuit,fecha,encargo):   #crea el  constructor de la clase
        self.cliente=cliente
        self.cuit=cuit
        self.fecha=fecha
        self.encargo=encargo
        
#Crear la tabla al ejecutarse la app     
with app.app_context():
    db.create_all()
    
# Crear ruta de acceso
# / es la ruta de inicio
@app.route("/")
def index():
    return f'App Web para registrar encargos de transporte'

# Crear un registro en la tabla Productos
@app.route("/registro", methods=['POST']) 
def registro():
    cliente_recibido = request.json["cliente"]
    cuit=request.json['cuit']
    fecha=request.json['fecha']
    encargo=request.json['encargo']

    nuevo_registro = Servicios(cliente=cliente_recibido,cuit=cuit,fecha=fecha,encargo=encargo)
    db.session.add(nuevo_registro)
    db.session.commit()

    return "Solicitud recibida"

# Retornar todos los registros en un Json
@app.route("/servicios",  methods=['GET'])
def servicios():
    # Consultar en la tabla todos los registros
    # all_registros -> lista de objetos
    all_registros = Servicios.query.all()

    # Lista de diccionarios
    data_serializada = []
    
    for objeto in all_registros:
        data_serializada.append({"id":objeto.id, "cliente":objeto.cliente, "cuit":objeto.cuit, "fecha":objeto.fecha, "encargo":objeto.encargo})

    return jsonify(data_serializada)

# Modificar un registro
@app.route('/update/<id>', methods=['PUT'])
def update(id):
    # Buscar el registro a modificar en la tabla por su id
    servicios = Servicios.query.get(id)

    
    cliente = request.json["cliente"]
    cuit=request.json['cuit']
    fecha=request.json['fecha']
    encargo=request.json['encargo']

    servicios.cliente=cliente
    servicios.cuit=cuit
    servicios.fecha=fecha
    servicios.encargo=encargo
    db.session.commit()

    data_serializada = [{"id":servicios.id, "cliente":servicios.cliente, "cuit":servicios.cuit, "fecha":servicios.fecha, "encargo":servicios.encargo}]
    
    return jsonify(data_serializada)

#metodo borrar
@app.route('/borrar/<id>', methods=['DELETE'])
def borrar(id):
    
    # Se busca a la productos por id en la DB
    servicios = Servicios.query.get(id)

    # Se elimina de la DB
    db.session.delete(servicios)
    db.session.commit()

    data_serializada = [{"id":servicios.id, "cliente":servicios.cliente, "cuit":servicios.cuit, "fecha":servicios.fecha, "encargo":servicios.encargo}]

    return jsonify(data_serializada)


if __name__ == "__main__":
    app.run(debug=True)