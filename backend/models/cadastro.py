from flask import render_template, request
from backend.db_utils import create_session
from backend.models.estrutura_db import Client
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
            registration_date = request.form['registration_date']
            contact_name = request.form['contact_name']
            phone = request.form['phone']
            email = request.form['email']
            billing_address = request.form['billing_address']
            municipio = request.form['municipio']
            uf = request.form['uf']
            cep = request.form['cep']
            bairro = request.form['bairro']
            billing_municipio = request.form['billing_municipio']
            billing_uf = request.form['billing_uf']
            billing_cep = request.form['billing_cep']
            billing_bairro = request.form['billing_bairro']

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
                registration_date=registration_date,
                contact_name=contact_name,
                phone=phone,
                email=email,
                billing_address=billing_address,
                municipio=municipio,
                uf=uf,
                cep=cep,
                bairro=bairro,
                billing_municipio=billing_municipio,
                billing_uf=billing_uf,
                billing_cep=billing_cep,
                billing_bairro=billing_bairro
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
