from flask import Flask, render_template, request, jsonify
from backend.models.cadastro import Cadastro
from backend.models.proposta import (buscar_clientes, buscar_produtos, buscar_servicos, proposta_comercial,
                                     proposal_number, add_products, add_services)
from backend.models.contrato import buscar_proposta, buscar_clientes_proposta
import traceback
import logging
import json

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_route():
    return Cadastro()


@app.route('/proposta', methods=['GET', 'POST'])
def proposta():
    try:
        client_data = {}
        product_data = {}
        service_data = {}
        success_message = None
        error_message = None

        if request.method == 'POST':
            form_data = {
                'proposal_id': request.form['proposal_id'],
                'client_id': request.form['client_id'],
                'company': request.form['company'],
                'cpf_cnpj': request.form['cpf_cnpj'],
                'contact_name': request.form['contact_name'],
                'phone': request.form['phone'],
                'email': request.form['email'],
                'number_store': request.form['number_store'],
                'status': request.form['status'],
                'delivery_address': request.form['delivery_address'],
                'delivery_date': request.form['delivery_date'],
                'withdrawal_date': request.form['withdrawal_date'],
                'start_date': request.form['start_date'],
                'end_date': request.form['end_date'],
                'period_days': request.form['period_days'],
                'validity': request.form['validity'],
                'value': request.form['value'],
            }

            client_data = json.loads(request.form.get('client_data', '{}'))
            product_data = json.loads(request.form.get('product_data', '{}'))
            service_data = json.loads(request.form.get('service_data', '{}'))

            print(request.method)
            data = request.form
            app.logger.info('Response data: %s', data)
            result = proposta_comercial(form_data)
            if isinstance(result, dict) and result.get('success'):
                success_message = "Proposal submitted successfully!"
            else:
                error_message = "Failed to submit proposal form. Please try again."

        return render_template('proposta.html', client_data=client_data, product_data=product_data,
                               service_data=service_data, success_message=success_message, error_message=error_message)

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
        if not products_response.json['success']:
            return products_response

        services_response = add_services(proposal_id, data['services'])
        if not services_response.json['success']:
            return services_response

        return services_response

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


@app.route('/contrato', methods=['GET', 'POST'])
def contrato():
    return render_template('contrato.html')


@app.route('/get_proposal_data', methods=['POST'])
def get_proposal_data():
    try:
        proposal_id = request.form.get('proposal_id')
        proposal_data = buscar_proposta(proposal_id)

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


if __name__ == '__main__':
    app.run(debug=True)
