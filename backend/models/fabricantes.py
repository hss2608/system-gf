from flask import render_template, request
from backend.db_utils import create_session
from backend.models.estrutura_db import AssetsManufacturer


def criar_fabricante():
    session = None
    try:
        if request.method == 'POST':
            print(request.form)
            manufacturer_id = request.form['id']
            acronym = request.form['acronym']
            description = request.form['description']

            session = create_session()

            assets_manufacturer = AssetsManufacturer(
                manufacturer_id=manufacturer_id,
                acronym=acronym,
                description=description
            )

            session.add(assets_manufacturer)
            session.commit()
            print("Debug: Form submitted successfully")

        return render_template('fabricante.html')

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        if session:
            session.close()


def listar_todos_fabricantes():
    session = create_session()

    try:
        fabricantes = session.query(AssetsManufacturer).all()
        fabricantes_dict = [fabricante.to_dict() for fabricante in fabricantes]
        print("Fabricantes: ", fabricantes_dict)
        return fabricantes_dict

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()


def buscar_fabricantes_por_id(manufacturer_id):
    session = create_session()

    try:
        fabricante = session.query(AssetsManufacturer).filter(AssetsManufacturer.id == manufacturer_id).one_or_none()

        fabricante_dict = {
            'manufacturer_id': fabricante.id, 'acronym': fabricante.acronym, 'description': fabricante.description
        }
        print("Busca fabricante por Id: ", fabricante_dict)
        return fabricante_dict

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()
