from flask import Flask, render_template, request, jsonify
from backend.models.cadastro import Cadastro
from backend.models.proposta import buscar_clientes, buscar_produtos, buscar_servicos, proposta_comercial, proposal_number
import traceback
import logging

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
                'product_id': request.form['product_id'],
                'product_code': request.form['product_code'],
                'description': request.form['description'],
                'type': request.form['type'],
                'unit_price': request.form['unit_price'],
                'price': request.form['price'],
                'add_description': request.form['add_description'],
                'refund_id': request.form['refund_id'],
                'cod': request.form['cod'],
                'descript': request.form['descript'],
                'value': request.form['value'],
            }
            print(request.method)

            client_data = buscar_clientes(form_data['cpf_cnpj'])
            print(f"Debug: Client Data - {client_data}")

            if client_data:
                form_data['client_id'] = client_data.get('client_id')
                form_data.update({
                    'company': client_data.get('company', ''),
                    'contact_name': client_data.get('contact_name', ''),
                    'phone': client_data.get('phone', ''),
                    'email': client_data.get('email', ''),
                    'number_store': client_data.get('number_store', ''),
                })

                product_data = buscar_produtos(form_data['product_code'])
                print(f"Debug: Product Data - {product_data}")
                if product_data:
                    form_data['product_id'] = product_data.get('product_id')
                    form_data.update({
                        'product_code': product_data.get('product_code', ''),
                        'description': product_data.get('description', ''),
                        'add_description': product_data.get('add_description', ''),
                        'type': product_data.get('type', ''),
                    })

                service_data = buscar_servicos(form_data['cod'])
                print(f"Debug: Service Data - {service_data}")
                if service_data:
                    form_data['refund_id'] = service_data.get('refund_id')
                    form_data.update({
                        'cod': service_data.get('cod', ''),
                        'descript': service_data.get('descript', ''),
                    })

            result = proposta_comercial(form_data)
            if isinstance(result, dict) and result.get('success'):
                success_message = "Proposal submitted successfully!"
            else:
                error_message = "Failed to submit proposal form. Please try again."

            try:
                error_data = result.json()
                if error_data and error_data.get('error'):
                    error_message += " " + error_data.get('error')
            except Exception as e:
                print(f"Error extracting error message: {e}")
            print(error_message)
        proposal_data = {'key': 'value'}
        return render_template('proposta.html',
                               client_data=client_data, product_data=product_data,
                               service_data=service_data, proposal_data=proposal_data, success_message=success_message)

    except Exception as e:
        error_message = str(e)
        traceback_info = traceback.format_exc()
        print(f"Error: {error_message}")
        print(f"Traceback: {traceback_info}")
        return render_template('error.html', error=error_message)


@app.route('/get_client_data', methods=['POST'])
def get_client_data():
    try:
        cpf_cnpj = request.form.get('cpf_cnpj')
        client_data = buscar_clientes(cpf_cnpj)
        data = request.form
        app.logger.info('Received data from client: %s', data)

        return jsonify(success=True, client_data=client_data)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(success=False, error=str(e))


@app.route('/get_product_data', methods=['POST'])
def get_product_data():
    try:
        product_code = request.form.get('product_code')
        product_data = buscar_produtos(product_code)
        data = request.form
        app.logger.info('Received data from product: %s', data)

        return jsonify(success=True, product_data=product_data)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(success=False, error=str(e))


@app.route('/get_service_data', methods=['POST'])
def get_service_data():
    try:
        cod = request.form.get('cod')
        service_data = buscar_servicos(cod)
        data = request.form
        app.logger.info('Received data from service: %s', data)

        return jsonify(success=True, service_data=service_data)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(success=False, error=str(e))


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


if __name__ == '__main__':
    app.run(debug=True)
