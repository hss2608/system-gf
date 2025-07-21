from flask import jsonify
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from backend.db_utils import create_session
from backend.models.estrutura_db import *
from backend.models.lista_propostas import buscar_proposta_por_id
from datetime import datetime
import logging
from flask import render_template


def Contrato(form_data=None, auto_data=None):
    session = None
    try:
        session = create_session()

        data_source = form_data if form_data else auto_data

        required_fields = ['contract_id', 'proposal_id', 'start_contract', 'end_contract', 'contract_days', 'value']

        missing_fields = [field for field in required_fields if field not in data_source or not data_source[field]]
        if missing_fields:
            error_message = f"Missing required fields: {', '.join(missing_fields)}"
            print(f"Error: {error_message}")
            return jsonify(success=False, error=error_message)

        contract = Contract(
            date_issue=data_source['date_issue'],
            contract_id=data_source['contract_id'],
            proposal_id=data_source['proposal_id'],
            start_contract=data_source['start_contract'],
            end_contract=data_source['end_contract'],
            contract_days=data_source['contract_days'],
            contract_status=data_source['contract_status'],
            contract_type=data_source['contract_type'],
            value=data_source['value'],
            address_obs=data_source['address_obs'],
            observations=data_source['observations'],
            oenf_obs=data_source['oenf_obs'],
            contract_comments=data_source['contract_comments']
        )

        session.add(contract)
        session.commit()
        print("Debug: Form submitted successfully")

        return jsonify(success=True, contract_id=contract.contract_id)

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return jsonify(success=False, error=str(e))

    except Exception as e:
        print(f"Error: {e}")
        if form_data:
            return render_template('error.html', error_message=str(e))
        return jsonify(success=False, error=str(e))

    finally:
        if session:
            session.close()


def criar_contrato(proposal_id):
    session = None
    try:
        session = create_session()
        proposta_lista = buscar_proposta_por_id(proposal_id)
        if not proposta_lista or not isinstance(proposta_lista, list):
            print("Proposta não encontrada.")
            return None

        proposta_dict = proposta_lista[0]

        if not proposta_dict or 'proposta' not in proposta_dict:
            print("Proposta não encontrada ou no formato incorreto.")
            return None

        auto_data = {
            'date_issue': datetime.now().strftime("%d/%m/%Y"),
            'contract_id': contract_number().split('/')[0],
            'proposal_id': proposta_dict['proposta']['proposal_id'].split('/')[0],
            'start_contract': proposta_dict['proposta']['start_date'],
            'end_contract': proposta_dict['proposta']['end_date'],
            'contract_days': proposta_dict['proposta']['period_days'],
            'value': proposta_dict['proposta']['value'],
            'delivery_address': proposta_dict['proposta']['delivery_address'],
            'delivery_bairro': proposta_dict['proposta']['delivery_bairro'],
            'delivery_municipio': proposta_dict['proposta']['delivery_municipio'],
            'delivery_uf': proposta_dict['proposta']['delivery_uf'],
            'delivery_cep': proposta_dict['proposta']['delivery_cep'],
            'client_id': proposta_dict['proposta']['client_id'],
            'contact_name': proposta_dict['contact_name'],
            'phone': proposta_dict['phone'],
            'email': proposta_dict['email'],
            'cpf_cnpj': proposta_dict['cpf_cnpj'],
            'corporate_name': proposta_dict['corporate_name'],
            'company': proposta_dict['company'],
            'company_address': proposta_dict['company_address'],
            'municipio': proposta_dict['municipio'],
            'uf': proposta_dict['uf'],
            'cep': proposta_dict['cep'],
            'bairro': proposta_dict['bairro'],
            'state_registration': proposta_dict['state_registration'],
            'billing_address': proposta_dict['billing_address'],
            'billing_bairro': proposta_dict['billing_bairro'],
            'billing_municpio': proposta_dict['billing_municipio'],
            'billing_uf': proposta_dict['billing_uf'],
            'billing_cep': proposta_dict['billing_cep'],
            'observations': proposta_dict['proposta']['observations'],
            'oenf_obs': proposta_dict['proposta']['oenf_obs'],
            'products': [{
                'product_id': product['product_id'],
                'product_code': product['product_code'],
                'description': product['description'],
                'quantity': product['quantity'],
                'unit_price': product['unit_price'],
                'price': product['price'],
                'extra_hours': product['extra_hours'],
                'rental_hours': product['rental_hours'],
            } for product in proposta_dict['products']],
            'services': [{
                'cod': service['cod'],
                'descript': service['descript'],
                'service_quantity': service['service_quantity'],
                'service_unit_price': service['service_unit_price'],
                'service_price': service['service_price']
            } for service in proposta_dict['services']]
        }

        contract = Contract(
            date_issue=auto_data['date_issue'],
            contract_id=auto_data['contract_id'],
            proposal_id=auto_data['proposal_id'],
            start_contract=auto_data['start_contract'],
            end_contract=auto_data['end_contract'],
            contract_days=auto_data['contract_days'],
            value=auto_data['value'],
            observations=auto_data['observations'],
            oenf_obs=auto_data['oenf_obs'],
        )

        session.add(contract)
        session.commit()

        return auto_data

    except Exception as e:
        print(f"Error in criar_contrato: {e}")
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
                'company': client.company,
                'company_address': client.company_address,
                'municipio': client.municipio,
                'uf': client.uf,
                'cep': client.cep,
                'bairro': client.bairro,
                'cpf_cnpj': client.cpf_cnpj,
                'state_registration': client.state_registration,
                'contact_name': client.contact_name,
                'phone': client.phone,
                'billing_address': client.billing_address,
                'billing_bairro': client.billing_bairro,
                'billing_municipio': client.billing_municipio,
                'billing_uf': client.billing_uf,
                'billing_cep': client.billing_cep,
            }

    except Exception as e:
        print(f"Error in buscar_clientes_proposta: {e}")
        return {}

    finally:
        session.close()


def contract_number():
    try:
        session = create_session()
        max_id = session.query(func.max(Contract.contract_id)).scalar()
        last_id = max_id if max_id else 0
        logging.debug(f"Last Contract Id: {last_id}")
        current_id = last_id + 1
        logging.debug(f"Current Id: {current_id}")
        session.close()

        current_date = datetime.now()
        month = current_date.strftime("%m")
        year = current_date.strftime("%Y")

        formatted_contract_number = f"{current_id:05d}/{month}/{year}"
        logging.debug(f"Formatted Contract Number: {formatted_contract_number}")
        return formatted_contract_number
    
    except Exception as e:
        print(f"Error: {e}")
        # linha extra abaixo para tratar o erro JSON serializable
        return jsonify(success=False, error=str(e))


def listar_todos_contratos():
    session = create_session()
    try:
        contratos = session.query(Contract, Client.company, Client.phone) \
            .join(Proposal, Contract.proposal_id == Proposal.proposal_id) \
            .join(Client, Proposal.client_id == Client.client_id).all()

        contratos_formatados = []
        for contrato, company, phone in contratos:
            contrato.date_issue = contrato.date_issue.strftime('%d/%m/%Y')

            mes_emissao = contrato.date_issue.split('/')[1]
            ano_emissao = contrato.date_issue.split('/')[2]

            contract_id_formatado = f"{contrato.contract_id:05d}/{mes_emissao}/{ano_emissao}"
            contrato.contract_id = contract_id_formatado

            contratos_formatados.append((contrato, company, phone))
        return contratos_formatados

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()


def buscar_contrato_por_id(contract_id, proposal_id):
    session = create_session()

    contract_alias = aliased(Contract)
    proposal_alias = aliased(Proposal)
    client_alias = aliased(Client)
    product_alias = aliased(Product)
    refund_alias = aliased(Refund)
    proposal_product_alias = aliased(ProposalProduct)
    proposal_refund_alias = aliased(ProposalRefund)
    cond_pag_alias = aliased(PaymentCondition)
    accessories_alias = aliased(Accessories)

    try:
        contrato_info = session.query(contract_alias, proposal_alias, client_alias) \
                .join(proposal_alias, contract_alias.proposal_id == proposal_alias.proposal_id) \
                .join(client_alias, proposal_alias.client_id == client_alias.client_id) \
                .filter(contract_alias.contract_id == contract_id).one_or_none()

        if not contrato_info:
            return None

        contrato, proposta, cliente = contrato_info

        produtos = session.query(product_alias, proposal_product_alias).join(
            proposal_product_alias, proposal_product_alias.product_id == product_alias.product_id
        ).filter(proposal_product_alias.proposal_id == proposal_id).all()

        ressarcimentos = session.query(refund_alias, proposal_refund_alias).join(
            proposal_refund_alias, proposal_refund_alias.cod == refund_alias.cod
        ).filter(proposal_refund_alias.proposal_id == proposal_id).all()

        acessorios = session.query(accessories_alias).filter_by(proposal_id=proposal_id).all()

        cond_pagamento = session.query(cond_pag_alias, proposal_alias).join(
            cond_pag_alias, proposal_alias.payment_condition_id == cond_pag_alias.cod
        ).filter(proposal_alias.proposal_id == proposal_id).scalar()

        cond_pagamento_formatado = f"{cond_pagamento.description}"

        contrato_date_issue = contrato.date_issue.strftime('%d/%m/%Y')
        contrato_start_contract = contrato.start_contract.strftime("%d/%m/%Y")
        contrato_end_contract = contrato.end_contract.strftime("%d/%m/%Y")
        proposta_delivery_date = proposta.delivery_date.strftime("%d/%m/%Y")
        proposta_withdrawal_date = proposta.withdrawal_date.strftime("%d/%m/%Y")

        # Formatar o ID do contrato
        mes_emissao = contrato_date_issue.split('/')[1]
        ano_emissao = contrato_date_issue.split('/')[2]
        contract_id_formatado = f"{contrato.contract_id:05d}/{mes_emissao}/{ano_emissao}"

        contrato_dict = {
            'contrato': {
                'contract_id': contract_id_formatado, 'proposal_id': contrato.proposal_id,
                'date_issue': contrato_date_issue,
                'start_contract': contrato_start_contract,
                'end_contract': contrato_end_contract, 'contract_days': contrato.contract_days,
                'contract_type': contrato.contract_type, 'contract_status': contrato.contract_status,
                'address_obs': contrato.address_obs, 'observations': contrato.observations,
                'oenf_obs': contrato.oenf_obs, 'contract_comments': contrato.contract_comments, 'value': contrato.value
            },
            'client_id': proposta.client_id, 'delivery_address': proposta.delivery_address,
            'delivery_bairro': proposta.delivery_bairro, 'delivery_municipio': proposta.delivery_municipio,
            'delivery_uf': proposta.delivery_uf, 'delivery_cep': proposta.delivery_cep,
            'delivery_date': proposta_delivery_date,
            'withdrawal_date': proposta_withdrawal_date, 'company': cliente.company,
            'number_store': cliente.number_store, 'company_address': cliente.company_address,
            'municipio': cliente.municipio, 'uf': cliente.uf, 'cep': cliente.cep, 'bairro': cliente.bairro,
            'contact_name': cliente.contact_name, 'phone': cliente.phone, 'email': cliente.email,
            'cpf_cnpj': cliente.cpf_cnpj,
            'state_registration': cliente.state_registration, 'billing_address': cliente.billing_address,
            'billing_bairro': cliente.billing_bairro, 'billing_municipio': cliente.billing_municipio,
            'billing_uf': cliente.billing_uf, 'billing_cep': cliente.billing_cep,
            'payment_condition': cond_pagamento_formatado,
            'produtos': [
                {
                    'product_id': produto.product_id,
                    'product_code': produto.product_code,
                    'description': produto.description,
                    'quantity': produto_proposta.quantity,
                    'unit_price': produto_proposta.unit_price,
                    'price': produto_proposta.price,
                    'extra_hours': produto_proposta.extra_hours,
                    'rental_hours': produto_proposta.rental_hours,
                    'discount': produto_proposta.discount,
                    'volts': produto_proposta.volts
                }
                for produto, produto_proposta in produtos
            ],
            'servicos': [
                {
                    'cod': ressarcimento_proposta.cod,
                    'descript': ressarcimento.descript,
                    'service_quantity': ressarcimento_proposta.service_quantity,
                    'service_unit_price': ressarcimento_proposta.service_unit_price,
                    'service_price': ressarcimento_proposta.service_price,
                    'discount': ressarcimento_proposta.discount,
                    'km': ressarcimento_proposta.km
                }
                for ressarcimento, ressarcimento_proposta in ressarcimentos
            ],
            'accessories': [
                {
                    'accessories_id': accessories.accessories_id,
                    'accessories_description': accessories.accessories_description,
                    'accessories_quantity': accessories.accessories_quantity,
                    'meters': accessories.meters,
                    'accessories_unit_price': accessories.accessories_unit_price,
                    'accessories_days': accessories.accessories_days,
                    'items_meters': accessories.items_meters,
                    'accessories_discount': accessories.accessories_discount,
                    'accessories_price': accessories.accessories_price,
                }
                for accessories in acessorios
            ]
        }

        return [contrato_dict]

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()


def atualizar_contrato(contract_id, dados_atualizados):
    session = create_session()
    try:
        contrato = session.query(Contract).filter_by(contract_id=contract_id).first()
        contrato.contract_status = dados_atualizados.get('contract_status', contrato.contract_status)
        contrato.contract_type = dados_atualizados.get('contract_type', contrato.contract_type)
        contrato.address_obs = dados_atualizados.get('address_obs', contrato.address_obs)
        contrato.contract_comments = dados_atualizados.get('contract_comments', contrato.contract_comments)

        session.commit()
        return {'success': True, 'contrato': contrato}

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def contract_to_dict(contrato):
    session = create_session()
    try:
        contract_dict = {
            'contract_type': contrato.contract_type,
            'contract_status': contrato.contract_status,
            'address_obs': contrato.address_obs,
            'contract_comments': contrato.contract_comments
        }

        session.commit()
        return contract_dict

    except Exception as e:
        session.rollback()
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()


def buscar_contrato_por_proposta(proposal_id):
    session = create_session()

    try:
        contrato = session.query(Contract).filter_by(proposal_id=proposal_id).first()
        if contrato:
            return contrato.contract_id, contrato.date_issue
        return None

    except Exception as e:
        print(f"Erro ao buscar contrato por proposal_id: {e}")
        return None

    finally:
        session.close()


def add_custo_parada_sub(stop_cost_sub):
    session = create_session()
    try:
        last_id = session.query(func.max(StopCostSub.stop_cost_sub_id)).scalar() or 0

        for stop_cost in stop_cost_sub:
            current_id = stop_cost.get('stop_cost_sub_id')
            if current_id is None or current_id == "":
                last_id += 1
                current_id = last_id
            sub = StopCostSub(
                stop_cost_sub_id=current_id,
                contract_id=stop_cost.get('contract_id', ''),
                sub_description=stop_cost.get('sub_description', ''),
                sub_supplier=stop_cost.get('sub_supplier', ''),
                sub_note=stop_cost.get('sub_note', ''),
                sub_initial_period=stop_cost.get('sub_initial_period', ''),
                sub_final_period=stop_cost.get('sub_final_period', ''),
                sub_rental_days=stop_cost.get('sub_rental_days', ''),
                sub_daily_value=stop_cost.get('sub_daily_value', ''),
                sub_value_machine=stop_cost.get('sub_value_machine', ''),
                sub_value_accessory=stop_cost.get('sub_value_accessory', ''),
                sub_total_value_machines=stop_cost.get('sub_total_value_machines', ''),
                sub_total_value_accessories=stop_cost.get('sub_total_value_accessories', '')
            )
            print("Stop Cost Sub: ", sub)
            session.merge(sub)
            session.commit()

        return jsonify(success=True)

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return jsonify(success=False, error=str(e))

    finally:
        session.close()


def add_custo_parada_frete(stop_cost_freight):
    session = create_session()
    try:
        if not isinstance(stop_cost_freight, list):
            raise ValueError("Esperava-se uma lista de dados para frete")
        last_id = session.query(func.max(StopCostFreight.stop_cost_freight_id)).scalar() or 0

        for stop_cost in stop_cost_freight:
            current_id = stop_cost.get('stop_cost_freight_id')
            if current_id is None or current_id in ('', "None"):
                last_id += 1
                current_id = last_id
            freight = StopCostFreight(
                stop_cost_freight_id=current_id,
                contract_id=stop_cost.get('contract_id', ''),
                freight_day=stop_cost.get('freight_day', ''),
                freight_driver=stop_cost.get('freight_driver', ''),
                freight_finality=stop_cost.get('freight_finality', ''),
                freight_own_third=stop_cost.get('freight_own_third', ''),
                freight_initial_km=stop_cost.get('freight_initial_km', ''),
                freight_final_km=stop_cost.get('freight_final_km', ''),
                freight_total_km=stop_cost.get('freight_total_km', ''),
                freight_cost_km=stop_cost.get('freight_cost_km', ''),
                freight_value_third=stop_cost.get('freight_value_third', ''),
                freight_value=stop_cost.get('freight_value', ''),
                freight_total_value=stop_cost.get('freight_total_value', ''),
                freight_total_value_third=stop_cost.get('freight_total_value_third', '')
            )
            print("Stop Cost Freight: ", freight)
            session.merge(freight)
            session.commit()

        return jsonify(success=True)

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return jsonify(success=False, error=str(e))

    finally:
        session.close()


def add_custo_parada_custo_operacional(stop_cost_op_cost):
    session = create_session()
    try:
        last_id = session.query(func.max(StopCostOpCost.stop_cost_op_cost_id)).scalar() or 0

        for stop_cost in stop_cost_op_cost:
            current_id = stop_cost.get('stop_cost_op_cost_id')
            if current_id is None or current_id == "":
                last_id += 1
                current_id = last_id
            op_cost = StopCostOpCost(
                stop_cost_op_cost_id=current_id,
                contract_id=stop_cost.get('contract_id', ''),
                op_cost_day=stop_cost.get('op_cost_day', ''),
                op_cost_tec_driver=stop_cost.get('op_cost_tec_driver', ''),
                op_cost_initial_hours=stop_cost.get('op_cost_initial_hours', ''),
                op_cost_final_hours=stop_cost.get('op_cost_final_hours', ''),
                op_cost_hours=stop_cost.get('op_cost_hours', ''),
                op_cost_value_hours=stop_cost.get('op_cost_value_hours', ''),
                op_cost_total_value_hours=stop_cost.get('op_cost_total_value_hours', ''),
                op_cost_extra_hours=stop_cost.get('op_cost_extra_hours', ''),
                op_cost_value_ex_hours=stop_cost.get('op_cost_value_ex_hours', ''),
                op_cost_total_value_ex_hours=stop_cost.get('op_cost_total_value_ex_hours', ''),
                op_cost_food_stay=stop_cost.get('op_cost_food_stay', ''),
                op_cost_value=stop_cost.get('op_cost_value', ''),
                op_cost_total_value=stop_cost.get('op_cost_total_value', ''),
                op_cost_total_value_food_stay=stop_cost.get('op_cost_total_value_food_stay', '')
            )
            print("Stop Cost Op Cost: ", op_cost)
            session.merge(op_cost)
            session.commit()

        return jsonify(success=True)

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return jsonify(success=False, error=str(e))

    finally:
        session.close()


def buscar_custos_parada_por_id(contract_id):
    session = create_session()

    sub_alias = aliased(StopCostSub)
    freight_alias = aliased(StopCostFreight)
    op_cost_alias = aliased(StopCostOpCost)

    try:
        subs = session.query(sub_alias).filter_by(contract_id=contract_id).all()
        freights = session.query(freight_alias).filter_by(contract_id=contract_id).all()
        ops_cost = session.query(op_cost_alias).filter_by(contract_id=contract_id).all()

        stop_cost_dict = {
            'sub': [
                {
                    'stop_cost_sub_id': sub.stop_cost_sub_id, 'contract_id': contract_id,
                    'sub_description': sub.sub_description, 'sub_supplier': sub.sub_supplier, 'sub_note': sub.sub_note,
                    'sub_initial_period': sub.sub_initial_period, 'sub_final_period': sub.sub_final_period,
                    'sub_rental_days': sub.sub_rental_days, 'sub_daily_value': sub.sub_daily_value,
                    'sub_value_machine': sub.sub_value_machine, 'sub_value_accessory': sub.sub_value_accessory,
                    'sub_total_value_machines': sub.sub_total_value_machines,
                    'sub_total_value_accessories': sub.sub_total_value_accessories
                }
                for sub in subs
            ],
            'freight': [
                {
                    'stop_cost_freight_id': freight.stop_cost_freight_id, 'contract_id': contract_id,
                    'freight_day': freight.freight_day, 'freight_driver': freight.freight_driver,
                    'freight_finality': freight.freight_finality, 'freight_own_third': freight.freight_own_third,
                    'freight_initial_km': freight.freight_initial_km, 'freight_final_km': freight.freight_final_km,
                    'freight_total_km': freight.freight_total_km, 'freight_cost_km': freight.freight_cost_km,
                    'freight_value_third': freight.freight_value_third, 'freight_value': freight.freight_value,
                    'freight_total_value': freight.freight_total_value,
                    'freight_total_value_third': freight.freight_total_value_third
                }
                for freight in freights
            ],
            'op_cost': [
                {
                    'stop_cost_op_cost_id': op_cost.stop_cost_op_cost_id, 'contract_id': contract_id,
                    'op_cost_day': op_cost.op_cost_day, 'op_cost_tec_driver': op_cost.op_cost_tec_driver,
                    'op_cost_initial_hours': op_cost.op_cost_initial_hours,
                    'op_cost_final_hours': op_cost.op_cost_final_hours, 'op_cost_hours': op_cost.op_cost_hours,
                    'op_cost_value_hours': op_cost.op_cost_value_hours,
                    'op_cost_total_value_hours': op_cost.op_cost_total_value_hours,
                    'op_cost_extra_hours': op_cost.op_cost_extra_hours,
                    'op_cost_value_ex_hours': op_cost.op_cost_value_ex_hours,
                    'op_cost_total_value_ex_hours': op_cost.op_cost_total_value_ex_hours,
                    'op_cost_food_stay': op_cost.op_cost_food_stay, 'op_cost_value': op_cost.op_cost_value,
                    'op_cost_total_value': op_cost.op_cost_total_value,
                    'op_cost_total_value_food_stay': op_cost.op_cost_total_value_food_stay
                }
                for op_cost in ops_cost
            ]
        }
        return [stop_cost_dict]

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()


def add_dados_fatura_follow_up(invoice_follow_up):
    session = create_session()
    try:
        if not isinstance(invoice_follow_up, list):
            raise ValueError("Esperava-se uma lista de dados para Invoice Follow Up")

        last_invoice_id = session.query(func.max(FollowUpInvoice)).scalar() or 0

        for invoice in invoice_follow_up:
            current_id = invoice.get('invoice_id')
            if current_id is None or current_id in ('', "None"):
                last_invoice_id += 1
                current_id = last_invoice_id
            invoices = FollowUpInvoice(
                invoice_id=current_id,
                contract_id=invoice.get('contract_id', ''),
                number_invoice=invoice.get('number_invoice', ''),
                contract_value=invoice.get('contract_value', ''),
                invoice_description=invoice.get('invoice_description', ''),
                invoice_value=invoice.get('invoice_value', ''),
                initial_period=invoice.get('initial_period', ''),
                final_period=invoice.get('final_period', ''),
                invoice_days=invoice.get('invoice_days', ''),
                invoice_venc_date=invoice.get('invoice_venc_date', ''),
            )
            print("Invoice Follow Up: ", invoices)
            session.merge(invoices)
            session.commit()

        return jsonify(success=True)

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return jsonify(success=False, error=str(e))

    finally:
        session.close()


def buscar_dados_fatura_follow_up(contract_id):
    session = create_session()
    try:
        invoices = session.query(FollowUpInvoice).filter_by(contract_id=contract_id).all()

        invoice_dict = {
            'invoices': [
                {
                    'invoice_id': invoice.invoice_id, 'contract_id': invoice.contract_id,
                    'number_invoice': invoice.number_invoice, 'contract_value': invoice.contract_value,
                    'invoice_description': invoice.invoice_description, 'invoice_value': invoice.invoice_value,
                    'initial_period': invoice.initial_period, 'final_period': invoice.final_period,
                    'invoice_days': invoice.invoice_days, 'invoice_venc_date': invoice.invoice_venc_date
                }
                for invoice in invoices
            ]
        }
        return [invoice_dict]

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()
