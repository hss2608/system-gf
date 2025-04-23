from flask import render_template, request
from backend.db_utils import create_session
from backend.models.estrutura_db import KvaGroup


def criar_kva_group():
    session = None
    try:
        if request.method == 'POST':
            print(request.form)
            id = request.form['kva_group_id']
            description = request.form['kva_group_description']
            family_id = request.form['family_id']
            quantity = float(request.form['quantity'])
            unit_value = float(request.form['unit_value'])

            session = create_session()

            kva_group = KvaGroup(
                id=id,
                description=description,
                family_id=family_id,
                quantity=quantity,
                unit_value=unit_value
            )

            session.add(kva_group)
            session.commit()
            print("Debug: Form submitted successfully")

        return render_template('grupo_kva.html')

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        if session:
            session.close()


def listar_todos_grupo_kva():
    session = create_session()
    try:
        grupos = session.query(KvaGroup).all()
        grupos_dict = [grupo.to_dict() for grupo in grupos]
        print("Grupos: ", grupos_dict)
        return grupos_dict

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()


def buscar_grupo_por_id(kva_group_id):
    session = create_session()

    try:
        grupo = session.query(KvaGroup).filter(KvaGroup.id == kva_group_id).one_or_none()

        grupo_dict = {
            'kva_group_id': grupo.id, 'kva_group_description': grupo.description, 'family_id': grupo.family_id,
            'quantity': grupo.quantity, 'unit_value': grupo.unit_value
        }
        print("Busca grupo por ID: ", grupo_dict)
        return grupo_dict

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()
