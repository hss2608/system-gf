from flask import render_template, request
from backend.db_utils import create_session
from backend.models.estrutura_proposta import Client
from datetime import datetime


def Cadastro():
    session = None
    try:
        current_date = datetime.now().strftime("%d/%m/%Y")
        if request.method == 'POST':
            print(request.form)
            company = request.form['company']
            corporate_name = request.form['corporate_name']
            number_store = request.form['number_store']
            person_type = request.form['person_type']
            company_address = request.form['company_address']
            client_type = request.form['client_type']
            cpf_cnpj = request.form['cpf_cnpj']
            state_registration = request.form['state_registration']
            contact_name = request.form['contact_name']
            phone = request.form['phone']
            email = request.form['email']
            billing_address = request.form['billing_address']

            print(f"Debug: current_date={current_date}")

            session = create_session()

            client = Client(
                company=company,
                corporate_name=corporate_name,
                number_store=number_store,
                person_type=person_type,
                company_address=company_address,
                client_type=client_type,
                cpf_cnpj=cpf_cnpj,
                state_registration=state_registration,
                contact_name=contact_name,
                phone=phone,
                email=email,
                billing_address=billing_address
            )

            session.add(client)
            session.commit()
            print("Debug: Form submitted successfully")

        return render_template('cadastro.html', current_date=current_date)

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        if session:
            session.close()
