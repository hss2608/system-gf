from flask import render_template, request
from backend.db_utils import create_session
from backend.models.estrutura_db import ModelType


def criar_tipo_modelo():
    session = None
    try:
        if request.method == 'POST':
            print(request.form)
            id = request.form['model_type_id']
            description = request.form['description']
            manufacturer_id = request.form['manufacturer_id']
            kva_group_id = request.form['kva_group_id']

            session = create_session()

            model_type = ModelType(
                model_type_id=id,
                description=description,
                manufacturer_id=manufacturer_id,
                kva_group_id=kva_group_id
            )

            session.add(model_type)
            session.commit()
            print("Debug: Form submitted successfully")

        return render_template('tipos_modelo.html')

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        if session:
            session.close()


def listar_todos_modelos():
    session = create_session()
    try:
        modelos = session.query(ModelType).all()
        modelos_dict = [modelo.to_dict() for modelo in modelos]
        print("Tipos de Modelos: ", modelos_dict)
        return modelos_dict

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()


def buscar_modelo_por_id(model_type_id):
    session = create_session()
    try:
        modelo = session.query(ModelType).filter(ModelType.id == model_type_id).one_or_none()

        modelo_dict = [modelo.to_dict()]
        print("Busca Tipo de Modelo por Id: ", modelo_dict)
        return modelo_dict

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()
