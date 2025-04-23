from backend.db_utils import create_session
from backend.models.estrutura_db import (Proposal, Client, ProposalProduct, ProposalRefund, Product, Refund,
                                         PaymentCondition, SalesOrder)
from flask import render_template, jsonify
from sqlalchemy import func
from sqlalchemy.orm import aliased
import logging


def listar_todas_propostas():
    session = create_session()
    try:
        propostas = session.query(Proposal, Client.company, Client.contact_name, Client.phone, Client.email) \
            .join(Client, Proposal.client_id == Client.client_id).all()
        propostas_formatadas = []
        for proposta, company, contact_name, phone, email in propostas:
            proposta.date_issue = proposta.date_issue.strftime('%d/%m/%Y')

            mes_emissao = proposta.date_issue.split('/')[1]
            ano_emissao = proposta.date_issue.split('/')[2]

            proposal_id_formatado = f"{proposta.proposal_id:05d}/{mes_emissao}/{ano_emissao}"
            proposta.proposal_id = proposal_id_formatado

            propostas_formatadas.append((proposta, company, contact_name, phone, email))
        return propostas_formatadas

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()


def buscar_proposta_por_id(proposal_id):
    session = create_session()

    proposal_alias = aliased(Proposal)
    client_alias = aliased(Client)
    product_alias = aliased(Product)
    refund_alias = aliased(Refund)
    cond_pag_alias = aliased(PaymentCondition)
    proposal_product_alias = aliased(ProposalProduct)
    proposal_refund_alias = aliased(ProposalRefund)

    try:
        proposta_info = session.query(proposal_alias, client_alias).join(
            client_alias, proposal_alias.client_id == client_alias.client_id
        ).filter(proposal_alias.proposal_id == proposal_id).one_or_none()

        if not proposta_info:
            return None

        proposta, cliente = proposta_info

        produtos = session.query(product_alias, proposal_product_alias).join(
            proposal_product_alias, proposal_product_alias.product_id == product_alias.product_id
        ).filter(proposal_product_alias.proposal_id == proposal_id).all()

        ressarcimentos = session.query(refund_alias, proposal_refund_alias).join(
            proposal_refund_alias, proposal_refund_alias.cod == refund_alias.cod
        ).filter(proposal_refund_alias.proposal_id == proposal_id).all()

        cond_pagamento = session.query(cond_pag_alias, proposal_alias).join(
            cond_pag_alias, proposal_alias.payment_condition_id == cond_pag_alias.cod
        ).filter(proposal_alias.proposal_id == proposal_id).scalar()

        cod_formatado = str(cond_pagamento.cod).zfill(3)
        cond_pagamento_formatado = f"{cod_formatado} - {cond_pagamento.description}"

        proposta_date_issue = proposta.date_issue.strftime('%d/%m/%Y')
        mes_emissao = proposta_date_issue.split('/')[1]
        ano_emissao = proposta_date_issue.split('/')[2]
        proposal_id_formatado = f"{proposta.proposal_id:05d}/{mes_emissao}/{ano_emissao}"

        proposta_dict = {
            'proposta': {
                'proposal_id': proposal_id_formatado, 'client_id': proposta.client_id, 'status': proposta.status,
                'delivery_address': proposta.delivery_address, 'delivery_bairro': proposta.delivery_bairro,
                'delivery_municipio': proposta.delivery_municipio, 'delivery_cep': proposta.delivery_cep,
                'delivery_uf': proposta.delivery_uf,
                'delivery_date': proposta.delivery_date.strftime("%d/%m/%Y"),
                'withdrawal_date': proposta.withdrawal_date.strftime("%d/%m/%Y"),
                'start_date': proposta.start_date.strftime("%d/%m/%Y"),
                'end_date': proposta.end_date.strftime("%d/%m/%Y"), 'period_days': proposta.period_days,
                'observations': proposta.observations, 'oenf_obs': proposta.oenf_obs, 'validity': proposta.validity,
                'value': proposta.value, 'date_issue': proposta_date_issue
            },
            'company': cliente.company,
            'number_store': cliente.number_store,
            'contact_name': cliente.contact_name,
            'phone': cliente.phone,
            'email': cliente.email,
            'cpf_cnpj': cliente.cpf_cnpj,
            'corporate_name': cliente.corporate_name,
            'state_registration': cliente.state_registration,
            'billing_address': cliente.billing_address,
            'billing_municipio': cliente.billing_municipio,
            'billing_uf': cliente.billing_uf,
            'billing_cep': cliente.billing_cep,
            'billing_bairro': cliente.billing_bairro,
            'company_address': cliente.company_address,
            'municipio': cliente.municipio,
            'uf': cliente.uf,
            'cep': cliente.cep,
            'bairro': cliente.bairro,
            'payment_condition': cond_pagamento_formatado,
            'products': [
                {
                    'product_id': product.product_id,
                    'product_code': product.product_code,
                    'description': product.description,
                    'quantity': proposal_product.quantity,
                    'unit_price': proposal_product.unit_price,
                    'price': proposal_product.price,
                    'extra_hours': proposal_product.extra_hours,
                    'rental_hours': proposal_product.rental_hours
                }
                for product, proposal_product in produtos
            ],
            'services': [
                {
                    'cod': proposal_refund.cod,
                    'descript': refund.descript,
                    'service_quantity': proposal_refund.service_quantity,
                    'service_unit_price': proposal_refund.service_unit_price,
                    'service_price': proposal_refund.service_price
                }
                for refund, proposal_refund in ressarcimentos
            ]
        }

        return [proposta_dict]

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()


def atualizar_proposta(proposal_id, dados_atualizados):
    session = create_session()
    try:
        if not isinstance(dados_atualizados, dict):
            raise ValueError("Os dados passados para atualizar_proposta devem ser um dicionário.")
        print("Atualizando a proposta com os dados:", dados_atualizados)
        proposal = session.query(Proposal).filter_by(proposal_id=proposal_id).first()
        if not proposal:
            raise ValueError(f"Proposta com ID {proposal_id} não encontrada.")

        proposal.status = dados_atualizados.get('status', proposal.status)
        proposal.observations = dados_atualizados.get('observations', proposal.observations)
        proposal.oenf_obs = dados_atualizados.get('oenf_obs', proposal.oenf_obs)
        proposal.value = dados_atualizados.get('value', proposal.value)

        for product_data in dados_atualizados.get('products', []):
            product = session.query(ProposalProduct).filter_by(proposal_id=proposal_id,
                                                               product_id=product_data['product_id']).first()
            if not product:
                product = ProposalProduct(proposal_id=proposal_id)
                session.add(product)
            product.product_id = product_data.get('product_id')
            product.product_code = product_data.get('product_code')
            product.description = product_data.get('description')
            product.quantity = product_data.get('quantity', product.quantity)
            product.unit_price = product_data.get('unit_price', product.unit_price)
            product.price = product_data.get('price', product.price)
            product.extra_hours = product_data.get('extra_hours', product.extra_hours)
            product.rental_hours = product_data.get('rental_hours', product.rental_hours)

        for service_data in dados_atualizados.get('services', []):
            service = session.query(ProposalRefund).filter_by(proposal_id=proposal_id,
                                                              cod=service_data['cod']).first()
            if not service:
                service = ProposalRefund(proposal_id=proposal_id)
                session.add(service)
            service.cod = service_data.get('cod')
            service.descript = service_data.get('descript')
            service.service_quantity = service_data.get('service_quantity', service.service_quantity)
            service.service_unit_price = service_data.get('service_unit_price', service.service_unit_price)
            service.service_price = service_data.get('service_price', service.service_price)

        session.commit()
        return {'success': True, 'proposta': proposal_to_dict(proposal)}

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def proposal_to_dict(proposal):
    session = create_session()
    try:
        proposal_dict = {
            'proposal_id': proposal.proposal_id,
            'status': proposal.status,
            'delivery_address': proposal.delivery_address, 'delivery_bairro': proposal.delivery_bairro,
            'delivery_cep': proposal.delivery_cep, 'delivery_municipio': proposal.delivery_municipio,
            'delivery_uf': proposal.delivery_uf,
            'delivery_date': proposal.delivery_date.strftime("%d/%m/%Y") if proposal.delivery_date else None,
            'withdrawal_date': proposal.withdrawal_date.strftime("%d/%m/%Y") if proposal.withdrawal_date else None,
            'start_date': proposal.start_date.strftime("%d/%m/%Y") if proposal.start_date else None,
            'end_date': proposal.end_date.strftime("%d/%m/%Y") if proposal.end_date else None,
            'period_days': proposal.period_days,
            'observations': proposal.observations,
            'oenf_obs': proposal.oenf_obs,
            'value': proposal.value,
            'products': [
                {
                    'product_id': product.product_id,
                    'product_code': product.product_code,
                    'description': product.description,
                    'quantity': product.quantity,
                    'unit_price': product.unit_price,
                    'price': product.price,
                    'extra_hours': product.extra_hours,
                    'rental_hours': product.rental_hours
                } for product in proposal.products
            ],
            'services': [
                {
                    'service_id': service.service_id,
                    'cod': service.cod,
                    'description': service.description,
                    'service_quantity': service.service_quantity,
                    'service_unit_price': service.service_unit_price,
                    'service_price': service.service_price
                } for service in proposal.services
            ]
        }

        return proposal_dict

    except Exception as e:
        session.rollback()
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()
