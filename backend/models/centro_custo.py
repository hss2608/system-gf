from flask import render_template, request
from backend.db_utils import create_session
from backend.models.estrutura_db import CostCenter


def costcenter():
    session = None
    try:
        if request.method == 'POST':
            print(request.form)
            id = request.form['id']
            description = request.form['description']

            session = create_session()

            cost_center = CostCenter(
                id=id,
                description=description
            )

            session.add(cost_center)
            session.commit()
            print("Debug: Form submitted successfully")

        return render_template('centro_custo.html')

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        if session:
            session.close()
