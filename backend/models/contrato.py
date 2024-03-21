from flask import jsonify
from sqlalchemy import func
from backend.db_utils import create_session
from backend.models.estrutura_db import *
from datetime import datetime
import logging


def buscar_proposta(proposal_id):
    session = create_session()
    try:
        proposal = session.query(Proposal).filter(Proposal.proposal_id == proposal_id).first()
        if proposal:
            return {
                'proposal_id': proposal.proposal_id,
                'client_id': proposal.client_id,
                'delivery_address': proposal.delivery_address,
                'value': proposal.value
            }
        else:
            return {}

    except Exception as e:
        print(f"Error in buscar_proposta: {e}")
        return {}

    finally:
        session.close()


def buscar_clientes_proposta(client_id):
    session = create_session()
    try:
        client = session.query(Client).filter(Client.client_id == client_id).first()
        if client:
            return {
                'client_id': client.client_id,
                'corporate_name': client.corporate_name,
                'company_address': client.company_address,
                'cpf_cnpj': client.cpf_cnpj,
                'state_registration': client.state_registration,
                'contact_name': client.contact_name,
                'phone': client.phone,
                'billing_address': client.billing_address
            }

    except Exception as e:
        print(f"Error in buscar_clientes_proposta: {e}")
        return {}

    finally:
        session.close()
