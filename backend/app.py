from flask import Flask, render_template, request, jsonify, send_file, flash, redirect
from backend.models.cadastro import Cadastro
from backend.models.proposta import (buscar_clientes, buscar_produtos, buscar_servicos, proposta_comercial,
                                     proposal_number, add_products, add_services, buscar_cond_pagamentos,
                                     add_accessories)
from backend.models.contrato import (Contrato, criar_contrato, contract_number, buscar_clientes_proposta,
                                     listar_todos_contratos, buscar_contrato_por_id, atualizar_contrato,
                                     contract_to_dict, add_custo_parada_sub, add_custo_parada_frete,
                                     add_custo_parada_custo_operacional, buscar_custos_parada_por_id,
                                     add_dados_fatura_follow_up, buscar_dados_fatura_follow_up)
from backend.models.lista_clientes import listar_todos_clientes, buscar_cliente_por_id, atualizar_cliente
from backend.models.lista_propostas import (listar_todas_propostas, buscar_proposta_por_id, atualizar_proposta,
                                            proposal_to_dict)
from backend.models.pedido_venda import (criar_pedido, sales_order_number, buscar_pedido_por_id)
from backend.models.pdf_proposta import gerar_pdf
from backend.models.pdf_contrato import gerar_pdf_contrato
from backend.models.pdf_pedido_venda import gerar_pdf_pedido_venda
from backend.models.familia_bens import criar_familias, listar_todas_familias, buscar_familia_por_id
from backend.models.grupo_kva import criar_kva_group, listar_todos_grupo_kva, buscar_grupo_por_id
from backend.models.fabricantes import criar_fabricante, listar_todos_fabricantes, buscar_fabricantes_por_id
from backend.models.tipo_modelos_bens import criar_tipo_modelo, listar_todos_modelos, buscar_modelo_por_id
from backend.models.bens import (buscar_assets, buscar_familia_bens, buscar_fabricantes, buscar_tipo_modelo,
                                 buscar_centro_custo, add_assets_follow_up, buscar_assets_follow_up)
import traceback
import logging
import json
import secrets
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.config['SECRET_KEY'] = '08dadb28a0ee217bff1205fcbe867674'


@app.route('/')
def home():
    return render_template('index.html')


# cadastro clientes
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_route():
    return Cadastro()


@app.route('/proposta', methods=['GET', 'POST'])
def proposta():
    try:
        client_data = json.loads(request.form.get('client_data', '{}'))
        product_data = json.loads(request.form.get('product_data', '{}'))
        service_data = json.loads(request.form.get('service_data', '{}'))
        return render_template('proposta.html', client_data=client_data, product_data=product_data,
                               service_data=service_data)

    except Exception as e:
        error_message = str(e)
        traceback_info = traceback.format_exc()
        print(f"Error: {error_message}")
        print(f"Traceback: {traceback_info}")
        return render_template('error.html', error=error_message)


@app.route('/submit_proposal', methods=['POST'])
def submit_proposal():
    try:
        data = request.get_json()
        response = proposta_comercial(data)
        if not response.json['success']:
            return response
        proposal_id = response.json['proposal_id']

        products_response = add_products(proposal_id, data['products'])
        print("Products response :", products_response)
        if not products_response.json['success']:
            return products_response

        services_response = add_services(proposal_id, data['services'])
        if not services_response.json['success']:
            return services_response

        accessories_response = add_accessories(proposal_id, data['accessories'])
        print("Accessories response :", accessories_response)
        if not accessories_response.json['success']:
            return accessories_response
        return jsonify(success=True, message="Proposta salva com sucesso!")
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/get_client_data', methods=['POST'])
def get_client_data():
    try:
        cpf_cnpj = request.form.get('cpf_cnpj')
        client_data = buscar_clientes(cpf_cnpj)

        if client_data:
            app.logger.info('Client data retrieved successfully: %s', client_data)
            return jsonify(success=True, client_data=client_data)
        else:
            app.logger.warning('Client data not found for Cpf/Cnpj: %s', cpf_cnpj)
            return jsonify(success=False, error='Client data not found')

    except Exception as e:
        app.logger.error('Error fetching client data: %s', e)
        return jsonify(success=False, error='Failed to fetch client data. Please try again.')


@app.route('/get_payment_condition', methods=['GET'])
def get_payment_condition():
    try:
        payment_condition = buscar_cond_pagamentos()
        if payment_condition:
            payment_condition_list = [
                {'cod': cond.cod, 'description': cond.description} for cond in payment_condition
            ]
            return jsonify(success=True, payment_condition=payment_condition_list)
        else:
            return jsonify(success=False, error="Nenhuma condição de pagamento encontrada.")

    except Exception as e:
        app.logger.error(f"Erro ao buscar condições de pagamento: {str(e)}")
        return jsonify(success=False, error="Erro ao buscar condições de pagamento.")


@app.route('/get_product_data', methods=['POST'])
def get_product_data():
    try:
        product_code = request.form.get('product_code')
        product_data = buscar_produtos(product_code)

        if product_data:
            app.logger.info('Product data retrieved successfully: %s', product_data)
            return jsonify(success=True, product_data=product_data)
        else:
            app.logger.warning('Product data not found for product code: %s', product_code)
            return jsonify(success=False, error='Product data not found')

    except Exception as e:
        app.logger.error('Error fetching product data: %s', e)
        return jsonify(success=False, error='Failed to fetch product data. Please try again.')


@app.route('/get_service_data', methods=['POST'])
def get_service_data():
    try:
        cod = request.form.get('cod')
        service_data = buscar_servicos(cod)

        if service_data:
            app.logger.info('Service data retrieved successfully: %s', service_data)
            return jsonify(success=True, service_data=service_data)
        else:
            app.logger.warning('Service data not found for cod: %s', cod)
            return jsonify(success=False, error='Service data not found')

    except Exception as e:
        app.logger.error('Error fetching service data: %s', e)
        return jsonify(success=False, error='Failed to fetch service data. Please try again.')


@app.route('/get_proposal_id', methods=['GET'])
def get_proposal_id():
    try:
        proposal_id = proposal_number()
        if proposal_id is not None:
            return jsonify({'proposal_id': proposal_id}), 200
        else:
            return jsonify({'error': 'Failed to generate proposal ID'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# rotas que manipulam a listagem dos clientes e edições dos mesmos
@app.route('/lista_clientes')
def listar_clientes():
    clientes = listar_todos_clientes()
    return render_template('lista_clientes.html', clientes=clientes)


@app.route('/cliente/visualizar/<int:client_id>')
def visualizar_cliente(client_id):
    cliente = buscar_cliente_por_id(client_id)
    return render_template('visualizar_cliente.html', cliente=cliente)


@app.route('/cliente/alterar/<int:client_id>', methods=['GET', 'POST'])
def editar_cliente(client_id):
    if request.method == 'POST':
        dados_atualizados = {
            'company': request.form['company'],
            'corporate_name': request.form['corporate_name'],
            'number_store': request.form['number_store'],
            'person_type': request.form['person_type'],
            'company_address': request.form['company_address'],
            'client_type': request.form['client_type'],
            'cpf_cnpj': request.form['cpf_cnpj'],
            'state_registration': request.form['state_registration'],
            'registration_date': request.form['registration_date'],
            'contact_name': request.form['contact_name'],
            'phone': request.form['phone'],
            'email': request.form['email'],
            'billing_address': request.form['billing_address'],
            'billing_municipio': request.form['billing_municipio'],
            'billing_uf': request.form['billing_uf'],
            'billing_cep': request.form['billing_cep'],
            'billing_bairro': request.form['billing_bairro']
        }
        atualizar_cliente(client_id, dados_atualizados)
        clientes = listar_todos_clientes()
        return render_template('lista_clientes.html', clientes=clientes)
    else:
        cliente = buscar_cliente_por_id(client_id)
        return render_template('editar_cliente.html', cliente=cliente)


# rotas que manipulam a listagem das propostas e edições das mesmas
@app.route('/lista_propostas')
def listar_propostas():
    propostas = listar_todas_propostas()
    return render_template('lista_propostas.html', propostas=propostas)


@app.route('/proposta/visualizar/<int:proposal_id>')
def visualizar_proposta(proposal_id):
    propostas = buscar_proposta_por_id(proposal_id)
    app.logger.info('Proposal data retrieved successfully: %s', propostas)
    return render_template('visualizar_proposta.html', propostas=propostas)


@app.route('/proposta/alterar/<int:proposal_id>', methods=['GET', 'POST'])
def editar_proposta(proposal_id):
    try:
        proposal_data = buscar_proposta_por_id(proposal_id)
        print("Proposal Data", proposal_data)
        if not proposal_data:
            return render_template('error.html', message="Proposta não encontrada.")

        status_proposta = proposal_data[0]['proposta']['status']
        print("Status:", status_proposta)

        print("Proposal ID:", proposal_id)

        if status_proposta in ['Aprovada', 'Reprovada']:
            flash(f"A proposta {proposal_data[0]['proposta']['proposal_id']} já foi {status_proposta.lower()} e não pode ser alterada.")
            return redirect(f'/proposta/visualizar/{proposal_id}')

        return render_template('editar_proposta.html', proposal_data=proposal_data)

    except Exception as e:
        error_message = str(e)
        traceback_info = traceback.format_exc()
        print(f"Error: {error_message}")
        print(f"Traceback: {traceback_info}")
        return render_template('error.html', error=error_message)


@app.route('/submit_edit_proposal', methods=['POST'])
def submit_edit_proposal():
    proposal_data = request.get_json()
    try:
        atualizar_proposta(proposal_data['proposal_id'], proposal_data)
        if proposal_data['status'] == 'Aprovada':
            responses = []
            try:
                contrato_response = criar_contrato(proposal_data['proposal_id'])
                responses.append({
                    "success": True,
                    "message": "Proposta aprovada e pronta para criar o contrato.",
                    "contrato": contrato_response
                })
            except Exception as contract_error:
                logging.error(f"Erro ao criar o contrato: {contract_error}", exc_info=True)
                responses.append({
                    "success": False,
                    "message": f"Erro ao preparar o contrato: {str(contract_error)}."
                })
            return jsonify({"success": True, "tarefas": responses}), 200

        return jsonify({"success": True, "message": "Proposta atualizada com sucesso."}), 200

    except Exception as e:
        logging.error(f"Erro ao atualizar a proposta: {e}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/proposta/imprimir/<int:proposal_id>')
def gerar_pdf_proposta(proposal_id):
    proposal_data = buscar_proposta_por_id(proposal_id)

    if not proposal_data:
        return "Proposta não encontrada", 404

    pdf_buffer = gerar_pdf(proposal_data)

    return send_file(pdf_buffer, as_attachment=True, download_name=f'proposta_{proposal_id}.pdf',
                     mimetype='application/pdf')


@app.route('/pedido/imprimir/<int:proposal_id>')
def gerar_pdf_pedido(proposal_id):
    proposal_data = buscar_proposta_por_id(proposal_id)
    pdf_buffer = gerar_pdf_pedido_venda(proposal_data)
    return send_file(pdf_buffer, as_attachment=True, download_name=f'pedido.pdf', mimetype='application/pdf')


# rotas que manipulam o contrato
@app.route('/get_proposal_data', methods=['POST'])
def get_proposal_data():
    try:
        proposal_id = request.form.get('proposal_id')
        proposal_data = buscar_proposta_por_id(proposal_id)

        if proposal_data:
            app.logger.info('Proposal data retrieved successfully: %s', proposal_data)
            return jsonify(success=True, proposal_data=proposal_data)
        else:
            app.logger.warning('Proposal data not found for cod: %s', proposal_id)
            return jsonify(success=False, error='Proposal data not found')

    except Exception as e:
        app.logger.error('Error fetching proposal data: %s', e)
        return jsonify(success=False, error='Failed to fetch proposal data. Please try again.')


@app.route('/get_client_proposal_data', methods=['GET', 'POST'])
def get_client_proposal_data():
    try:
        client_id = request.form.get('client_id')
        client_proposal_data = buscar_clientes_proposta(client_id)

        if client_proposal_data:
            app.logger.info('Client Proposal data retrieved successfully: %s', client_proposal_data)
            return jsonify(success=True, client_proposal_data=client_proposal_data)
        else:
            app.logger.warning('Client Proposal data not found for cod: %s', client_id)
            return jsonify(success=False, error='Client Proposal data not found')

    except Exception as e:
        app.logger.error('Error fetching client proposal data: %s', e)
        return jsonify(success=False, error='Failed to fetch client proposal data. Please try again.')


@app.route('/get_contract_id', methods=['GET'])
def get_contract_id():
    try:
        contract_id = contract_number()
        if contract_id is not None:
            return jsonify({'contract_id': contract_id}), 200
        else:
            return jsonify({'error': 'Failed to generate contract ID'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/lista_contratos')
def listar_contratos():
    contratos = listar_todos_contratos()
    return render_template('lista_contratos.html', contratos=contratos)


@app.route('/contrato/visualizar/<int:contract_id>/<int:proposal_id>')
def visualizar_contrato(contract_id, proposal_id):
    contratos = buscar_contrato_por_id(contract_id, proposal_id)
    app.logger.info('Contract data retrieved successfully: %s', contratos)
    return render_template('visualizar_contrato.html', contratos=contratos)


@app.route('/contrato/alterar/<int:contract_id>/<int:proposal_id>', methods=['GET', 'POST'])
def editar_contrato(contract_id, proposal_id):
    if request.method == 'POST':
        dados_atualizados = {
            'contract_status': request.form['contract_status'],
            'contract_type': request.form['contract_type'],
            'address_obs': request.form['address_obs'],
            'contract_comments': request.form['contract_comments']
        }
        atualizar_contrato(contract_id, dados_atualizados)
        contratos = listar_todos_contratos()
        return render_template('lista_contratos.html', contratos=contratos)
    else:
        contract = buscar_contrato_por_id(contract_id, proposal_id)
        app.logger.info('Contract data retrieved successfully: %s', contract)
        return render_template('editar_contrato.html', contract=contract)


@app.route('/submit_edit_contract', methods=['POST'])
def submit_edit_contract():
    contract_data = request.get_json()
    try:
        updated_contract = atualizar_contrato(contract_data['contract_id'], contract_data)
        if updated_contract['success']:
            contract_dict = contract_to_dict(updated_contract['contrato'])

            return jsonify({
                "success": True,
                "message": "Contrato atualizado com sucesso.",
                "contrato": contract_dict,
                "redirect_url": f"/lista_contratos"
            })
        else:
            return jsonify({"success": False, "message": updated_contract.get('message', 'Erro desconhecido')})
    except Exception as e:
        logging.error(f"Erro ao atualizar o contrato: {e}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/contrato/imprimir/<int:contract_id>/<int:proposal_id>')
def gerar_pdf_contrato_geraforca(contract_id, proposal_id):
    contract_data = buscar_contrato_por_id(contract_id, proposal_id)

    if not contract_data:
        return "Contrato não encontrado", 404

    pdf_buffer = gerar_pdf_contrato(contract_data)

    return send_file(pdf_buffer, as_attachment=True, download_name=f'contrato_{contract_id}.pdf',
                     mimetype='application/pdf')


@app.route('/custos_parada/<int:contract_id>/<int:proposal_id>', methods=['GET'])
def editar_custos_parada(contract_id, proposal_id):
    custos_parada_data = buscar_custos_parada_por_id(contract_id)
    contrato_data = buscar_contrato_por_id(contract_id, proposal_id)

    return render_template('custos_parada.html', custos_parada_data=custos_parada_data,
                           contrato_data=contrato_data, contract_id=contract_id)


@app.route('/submit_stop_cost', methods=['POST'])
def submit_stop_cost():
    try:
        data = request.get_json()
        print("Data sub: ", data['sub'])
        print("Data freight: ", data['freight'])
        print("Data Op Cost: ", data['op_cost'])

        sub_response = add_custo_parada_sub(data['sub'])
        if not sub_response.json['success']:
            return sub_response

        freight_response = add_custo_parada_frete(data['freight'])
        if not freight_response.json['success']:
            return freight_response

        op_cost_response = add_custo_parada_custo_operacional(data['op_cost'])
        if not op_cost_response.json['success']:
            return op_cost_response

        return jsonify(success=True)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/follow_up/<int:contract_id>/<int:proposal_id>', methods=['GET'])
def editar_follow_up(contract_id, proposal_id):
    contrato_data = buscar_contrato_por_id(contract_id, proposal_id)
    custos_parada_data = buscar_custos_parada_por_id(contract_id)
    assets_follow_up = buscar_assets_follow_up(contract_id)
    fatura_data = buscar_dados_fatura_follow_up(contract_id)

    return render_template('follow_up.html', contrato_data=contrato_data,
                           custos_parada_data=custos_parada_data, assets_follow_up=assets_follow_up,
                           fatura_data=fatura_data)


@app.route('/submit_follow_up', methods=['POST'])
def submit_follow_up():
    try:
        data = request.get_json()
        assets_response = add_assets_follow_up(data['assets'])
        if not assets_response.json['success']:
            return assets_response

        invoice_response = add_dados_fatura_follow_up(data['invoices'])
        if not invoice_response.json['success']:
            return invoice_response

        return jsonify(success=True)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/bens/familia', methods=['GET', 'POST'])
def criar_familia_bens():
    return criar_familias()


@app.route('/lista_familias')
def listar_familias():
    familias = listar_todas_familias()
    return render_template('lista_familias.html', familias=familias)


@app.route('/familia/visualizar/<int:family_id>')
def visualizar_familia(family_id):
    familia = buscar_familia_por_id(family_id)
    app.logger.info('assets Family data retrieved successfully: %s', familia)
    return render_template('visualizar_familias.html', familia=familia)


@app.route('/get_assets_family', methods=['GET'])
def get_assets_family():
    try:
        assets_family = listar_todas_familias()
        print("Família de bens: ", assets_family)
        if assets_family:
            assets_family_list = [
                {'family_id': family['family_id'], 'family_description': family['family_description']}
                for family in assets_family
            ]
            return jsonify(success=True, assets_family=assets_family_list)
        else:
            return jsonify(success=False, error="Nenhuma família de bens encontrada.")

    except Exception as e:
        app.logger.error(f"Erro ao buscar família de bens: {str(e)}")
        return jsonify(success=False, error="Erro ao buscar família de bens.")


@app.route('/grupo/kva', methods=['GET', 'POST'])
def criar_grupo_kva():
    return criar_kva_group()


@app.route('/lista_grupos_kva')
def listar_grupos():
    grupos = listar_todos_grupo_kva()
    return render_template('lista_grupos_kva.html', grupos=grupos)


@app.route('/grupo/visualizar/<int:kva_group_id>')
def visualizar_grupo(kva_group_id):
    grupo = buscar_grupo_por_id(kva_group_id)
    app.logger.info('Groups KVA data retrieved successfully: %s', grupo)
    return render_template('visualizar_grupo_kva.html', grupo=grupo)


@app.route('/get_kva_group', methods=['GET'])
def get_kva_group(kva_group_id):
    try:
        kva_group = buscar_grupo_por_id(kva_group_id)
        if kva_group:
            kva_group_list = [kva_group]
            return jsonify(success=True, kva_group=kva_group_list)
        else:
            return jsonify(success=False, error="Nenhum grupo de kva encontrado.")

    except Exception as e:
        app.logger.error(f"Erro ao buscar grupos de kva: {str(e)}")
        return jsonify(success=False, error="Erro ao grupos de kva.")


@app.route('/fabricante', methods=['GET', 'POST'])
def criar_fabricantes():
    return criar_fabricante()


@app.route('/lista_fabricantes')
def listar_fabricantes():
    fabricantes = listar_todos_fabricantes()
    return render_template('lista_fabricantes.html', fabricantes=fabricantes)


@app.route('/fabricante/visualizar/<int:manufacturer_id>')
def visualizar_fabricante(manufacturer_id):
    fabricante = buscar_fabricantes_por_id(manufacturer_id)
    app.logger.info('Assets Manufacturer data retrieved successfully: %s', fabricante)
    return render_template('visualizar_fabricante.html', fabricante=fabricante)


@app.route('/get_manufacturer', methods=['GET'])
def get_manufacturer(manufacturer_id):
    try:
        manufacturer = buscar_fabricantes_por_id(manufacturer_id)
        if manufacturer:
            manufacturer_list = [manufacturer]
            return jsonify(success=True, manufacturer=manufacturer_list)
        else:
            return jsonify(success=False, error="Nenhum fabricante encontrado.")

    except Exception as e:
        app.logger.error(f"Erro ao buscar fabricantes: {str(e)}")
        return jsonify(success=False, error="Erro ao buscar fabricantes.")


@app.route('/modelo', methods=['GET', 'POST'])
def criar_modelo():
    return criar_tipo_modelo()


@app.route('/lista_modelos')
def listar_modelos():
    modelos = listar_todos_modelos()
    return render_template('lista_modelos.html', modelos=modelos)


@app.route('/modelo/visualizar/<int:model_type_id>')
def visualizar_modelo(model_type_id):
    modelo = buscar_modelo_por_id(model_type_id)
    app.logger.info('Model Type data retrieved successfully: %s', modelo)
    return render_template('visualizar_modelo.html', modelo=modelo)


@app.route('/get_model_type', methods=['GET'])
def get_model_type(model_type_id):
    try:
        model_type = buscar_modelo_por_id(model_type_id)
        if model_type:
            model_list = [model_type]
            return jsonify(success=True, model_type=model_list)
        else:
            return jsonify(success=False, error="Nenhum fabricante encontrado.")

    except Exception as e:
        app.logger.error(f"Erro ao buscar modelos: {str(e)}")
        return jsonify(success=False, error="Erro ao buscar modelos.")


if __name__ == '__main__':
    app.run(debug=True)
