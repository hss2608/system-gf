from flask import jsonify
from sqlalchemy import func
from backend.db_utils import create_session
from backend.models.estrutura_db import (Client, Proposal, Product, Refund, ProposalProduct, ProposalRefund,
                                         PaymentCondition)
from datetime import datetime
import logging


def analisar_data(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return None


def buscar_clientes(cpf_cnpj):
    session = create_session()
    try:
        client = session.query(Client).filter(Client.cpf_cnpj == cpf_cnpj).first()
        if client:
            return {
                'client_id': client.client_id,
                'company': client.company,
                'cpf_cnpj': client.cpf_cnpj,
                'contact_name': client.contact_name,
                'phone': client.phone,
                'email': client.email,
                'number_store': client.number_store
            }
        else:
            return {}
    except Exception as e:
        print(f"Error in buscar_clientes: {e}")
        return {}
    finally:
        session.close()


def buscar_produtos(product_code):
    session = create_session()

    try:
        product = session.query(Product).filter(Product.product_code == product_code).first()
        if product:
            return {
                'product_id': product.product_id,
                'product_code': product.product_code,
                'description': product.description,
                'type': product.type,
                'add_description': product.add_description
            }
        else:
            return {}
    except Exception as e:
        print(f"Error in buscar_produtos: {e}")
        return {}
    finally:
        session.close()


def buscar_servicos(cod):
    if not cod:
        return {}

    session = create_session()
    try:
        service = session.query(Refund).filter(Refund.cod == cod).first()
        if service:
            return {
                'cod': service.cod,
                'descript': service.descript,
                'refund_id': service.refund_id
            }
        else:
            return {}
    except Exception as e:
        print(f"Error in buscar_servicos: {e}")
        return {}
    finally:
        session.close()


def proposta_comercial(form_data):
    session = create_session()
    try:
        current_date = datetime.now().strftime("%d/%m/%Y")
        required_fields = ['proposal_id', 'client_id', 'status', 'delivery_address', 'delivery_bairro', 'delivery_cep',
                           'delivery_municipio', 'delivery_uf', 'delivery_date', 'withdrawal_date', 'start_date',
                           'end_date', 'period_days', 'validity', 'observations', 'oenf_obs', 'value']

        missing_fields = [field for field in required_fields if field not in form_data or not form_data[field]]
        if missing_fields:
            error_message = f"Missing required fields: {', '.join(missing_fields)}"
            print(f"Error: {error_message}")
            return jsonify(success=False, error=error_message)

        proposal = Proposal(
            proposal_id=form_data['proposal_id'],
            client_id=form_data['client_id'],
            date_issue=current_date,
            status=form_data['status'],
            delivery_address=form_data['delivery_address'],
            delivery_bairro=form_data['delivery_bairro'],
            delivery_municipio=form_data['delivery_municipio'],
            delivery_cep=form_data['delivery_cep'],
            delivery_uf=form_data['delivery_uf'],
            delivery_date=form_data['delivery_date'],
            withdrawal_date=form_data['withdrawal_date'],
            start_date=form_data['start_date'],
            end_date=form_data['end_date'],
            period_days=form_data['period_days'],
            validity=form_data['validity'],
            observations=form_data['observations'],
            oenf_obs=form_data['oenf_obs'],
            value=form_data['value'],
            payment_condition_id=form_data['payment_condition']
        )
        session.add(proposal)
        session.commit()

        proposal_id = proposal.proposal_id
        print("Proposal ID:", proposal_id)

        print("Debug: Form submitted successfully")
        return jsonify(success=True, proposal_id=proposal_id)

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        # linha extra abaixo para tratar o erro JSON serializable
        return jsonify(success=False, error=str(e))

    finally:
        session.close()


def add_products(proposal_id, products):
    session = create_session()
    try:
        for product in products:
            proposal_product = ProposalProduct(
                proposal_id=proposal_id,
                product_id=product['product_id'],
                quantity=product['quantity'],
                unit_price=product['unit_price'],
                price=product['price'],
                extra_hours=product['extra_hours'],
                rental_hours=product['rental_hours']
            )
            session.add(proposal_product)

        session.commit()
        return jsonify(success=True)
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        # linha extra abaixo para tratar o erro JSON serializable
        return jsonify(success=False, error=str(e))

    finally:
        session.close()


def add_services(proposal_id, services):
    session = create_session()
    try:

        for service in services:
            proposal_refund = ProposalRefund(
                proposal_id=proposal_id,
                cod=service['cod'],
                service_quantity=service['service_quantity'],
                service_unit_price=service['service_unit_price'],
                service_price=service['service_price']
            )
            session.add(proposal_refund)

        session.commit()

        return jsonify(success=True)
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return jsonify(success=False, error=str(e))

    finally:
        session.close()


def proposal_number():
    try:
        session = create_session()
        max_id = session.query(func.max(Proposal.proposal_id)).scalar()
        last_id = max_id if max_id else 0
        logging.debug(f"Last Proposal Id: {last_id}")
        current_id = last_id + 1
        logging.debug(f"Current Id: {current_id}")
        session.close()
        return current_id

    except Exception as e:
        print(f"Error: {e}")
        # linha extra abaixo para tratar o erro JSON serializable
        return jsonify(success=False, error=str(e))


def buscar_cond_pagamentos():
    session = create_session()

    try:
        payment_conditions = session.query(PaymentCondition).all()
        return payment_conditions

    except Exception as e:
        print(f"Erro ao recuperar condições de pagamento: {e}")
        return []

    finally:
        session.close()



