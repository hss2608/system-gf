from flask import render_template, request
from backend.db_utils import create_session
from backend.models.estrutura_db import AssetsFamily


def criar_familias():
    session = None
    try:
        if request.method == 'POST':
            print(request.form)
            id = request.form['family_id']
            description = request.form['family_description']

            session = create_session()

            assets_family = AssetsFamily(
                id=id,
                description=description
            )

            session.add(assets_family)
            session.commit()
            print("Debug: Form submitted successfully")

        return render_template('familia_bens.html')

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        if session:
            session.close()


def listar_todas_familias():
    session = create_session()
    try:
        familias = session.query(AssetsFamily).all()
        familias_dict = [familia.to_dict() for familia in familias]
        print("Familias: ", familias_dict)
        return familias_dict

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()


def buscar_familia_por_id(family_id):
    session = create_session()

    try:
        familia = session.query(AssetsFamily).filter(AssetsFamily.id == family_id).one_or_none()

        familia_dict = {
            'family_id': familia.id, 'family_description': familia.description
        }
        print("Busca família por IDs: ", familia_dict)
        return familia_dict

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()
