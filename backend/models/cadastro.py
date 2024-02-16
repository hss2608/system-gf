from flask import render_template, request
from backend.db_utils import create_connection, close_connection
from datetime import datetime


def Cadastro():
    connection = None
    cursor = None

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

            connection, cursor = create_connection()

            cursor.execute("""
                INSERT INTO clients (company, corporate_name, number_store, person_type, company_address, client_type, cpf_cnpj, state_registration, registration_date, contact_name, phone, email, billing_address)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s, %s)  
            """, (
                company, corporate_name, number_store, person_type, company_address, client_type, cpf_cnpj, state_registration, contact_name, phone, email, billing_address
            ))
            connection.commit()
            print("Debug: Form submitted successfully")

        return render_template('cadastro.html', current_date=current_date)

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        close_connection(connection, cursor)
