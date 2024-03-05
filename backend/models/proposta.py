from flask import jsonify
from backend.db_utils import create_connection, close_connection
from datetime import datetime
import logging


def analisar_data(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return None


def buscar_clientes(cpf_cnpj):
    connection, cursor = create_connection()
    try:
        cursor.execute("""
            SELECT client_id, company, cpf_cnpj, contact_name, phone, email, number_store
            FROM clients WHERE cpf_cnpj = %s
        """, (cpf_cnpj,))
        client_data = cursor.fetchone()
        if client_data:
            columns = ['client_id', 'company', 'cpf_cnpj', 'contact_name', 'phone', 'email', 'number_store']
            return dict(zip(columns, client_data))
        else:
            return {}
    except Exception as e:
        print(f"Error in buscar_clientes: {e}")
        return {}
    finally:
        close_connection(connection, cursor)


def buscar_produtos(product_code,):
    connection, cursor = create_connection()

    try:
        cursor.execute("""
            SELECT product_id, product_code, description, type, add_description
            FROM products WHERE product_code = %s
        """, (product_code,))
        product_data = cursor.fetchone()
        if product_data:
            columns = ['product_id', 'product_code', 'description', 'type', 'add_description']
            print(f"SQL Query: SELECT * FROM products WHERE product_code = '{product_code}'")
            return dict(zip(columns, product_data))
        else:
            return {}
    except Exception as e:
        print(f"Error in buscar_produtos: {e}")
        return {}
    finally:
        close_connection(connection, cursor)


def buscar_servicos(cod,):
    if not cod:
        return None

    connection, cursor = create_connection()

    try:
        cursor.execute("""
            SELECT cod, descript, refund_id
            FROM refund WHERE cod = %s
        """, (cod,))
        service_data = cursor.fetchone()
        if service_data:
            columns = ['cod', 'descript', 'refund_id']
            print(f"SQL Query: SELECT * FROM refund WHERE cod = '{cod}'")
            return dict(zip(columns, service_data))
        else:
            return {}
    except Exception as e:
        print(f"Error in buscar_servicos: {e}")
        return {}
    finally:
        close_connection(connection, cursor)


def proposta_comercial(form_data):
    try:
        required_fields = ['proposal_id', 'client_id', 'status', 'delivery_address',
                           'delivery_date', 'withdrawal_date', 'start_date', 'end_date',
                           'period_days', 'validity', 'product_id', 'cod', 'value']

        missing_fields = [field for field in required_fields if field not in form_data or not form_data[field]]
        if missing_fields:
            error_message = f"Missing required fields: {', '.join(missing_fields)}"
            print(f"Error: {error_message}")
            return jsonify(success=False, error=error_message)

        connection, cursor = create_connection()

        cursor.execute("""
                INSERT INTO proposal (proposal_id, client_id, status, delivery_address, delivery_date, withdrawal_date,
                                      start_date, end_date, period_days, validity, value)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING proposal_id;  
            """, (
                form_data['proposal_id'], form_data['client_id'], form_data['status'], form_data['delivery_address'],
                form_data['delivery_date'], form_data['withdrawal_date'], form_data['start_date'],
                form_data['end_date'], form_data['period_days'], form_data['validity'], form_data['value']
        ))
        connection.commit()

        proposal_id = cursor.fetchone()[0]
        print("Proposal ID:", proposal_id)

        for product_id in form_data.get('product_id', []):
            cursor.execute("""
                INSERT INTO proposal_product (proposal_id, product_id)
                VALUES (%s, %s);
            """, (proposal_id, product_id))

        for cod in form_data.get('cod', []):
            cursor.execute("""
                INSERT INTO proposal_refund (proposal_id, cod)
                VALUES (%s, %s);
            """, (proposal_id, cod))

        connection.commit()
        close_connection(connection, cursor)
        print("Debug: Form submitted successfully")
        return jsonify(success=True)

    except Exception as e:
        print(f"Error: {e}")
        # linha extra abaixo para tratar o erro JSON serializable
        return jsonify(success=False, error=str(e))


def proposal_number():
    connection, cursor = create_connection()

    try:
        cursor.execute("""
            SELECT MAX(proposal_id) AS last_id
            FROM proposal;
        """)

        result = cursor.fetchone()
        last_id = result[0] if result[0] is not None else 0
        logging.debug(f"Last Proposal Id: {last_id}")

        current_id = last_id + 1
        logging.debug(f"Current Id: {current_id}")

        connection.commit()
        close_connection(connection, cursor)

        return current_id

    except Exception as e:
        print(f"Error: {e}")
        # linha extra abaixo para tratar o erro JSON serializable
        return jsonify(success=False, error=str(e))
