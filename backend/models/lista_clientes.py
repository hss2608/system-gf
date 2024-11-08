from backend.db_utils import create_session
from backend.models.estrutura_db import Client
from flask import render_template


def listar_todos_clientes():
    session = create_session()
    try:
        clientes = session.query(Client).all()
        return clientes

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()


def buscar_cliente_por_id(client_id):
    session = create_session()
    try:
        return session.query(Client).get(client_id)

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()


def atualizar_cliente(client_id, dados_atualizados):
    session = create_session()
    try:
        cliente = session.query(Client).get(client_id)
        if cliente:
            cliente.company = dados_atualizados.get('company')
            cliente.corporate_name = dados_atualizados.get('corporate_name')
            cliente.number_store = dados_atualizados.get('number_store')
            cliente.person_type = dados_atualizados.get('person_type')
            cliente.company_address = dados_atualizados.get('company_address')
            cliente.municipio = dados_atualizados.get('municipio')
            cliente.uf = dados_atualizados.get('uf')
            cliente.cep = dados_atualizados.get('cep')
            cliente.bairro = dados_atualizados.get('bairro')
            cliente.client_type = dados_atualizados.get('client_type')
            cliente.cpf_cnpj = dados_atualizados.get('cpf_cnpj')
            cliente.state_registration = dados_atualizados.get('state_registration')
            cliente.registration_date = dados_atualizados.get('registration_date')
            cliente.contact_name = dados_atualizados.get('contact_name')
            cliente.phone = dados_atualizados.get('phone')
            cliente.email = dados_atualizados.get('email')
            cliente.billing_address = dados_atualizados.get('billing_address')
            cliente.billing_municipio = dados_atualizados.get('billing_municipio')
            cliente.billing_uf = dados_atualizados.get('billing_uf')
            cliente.billing_cep = dados_atualizados.get('billing_cep')
            cliente.billing_bairro = dados_atualizados.get('billing_bairro')
            session.commit()
        return cliente
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
