from flask import render_template, request, jsonify
from backend.db_utils import create_session
from backend.models.estrutura_db import Assets, ModelType, AssetsManufacturer, CostCenter, AssetsFamily, AssetsFollowUp
from datetime import datetime
from sqlalchemy import func


def buscar_tipo_modelo(id):
    session = create_session()
    try:
        model_type = session.query(ModelType).filter(ModelType.id == id).first()
        if model_type:
            return {
                'model_type_id': model_type.id,
                'model_type_description': model_type.description
            }
        else:
            return {}
    except Exception as e:
        print(f"Error in buscar_tipo_modelo: {e}")
        return {}
    finally:
        session.close()


def buscar_fabricantes(id):
    session = create_session()
    try:
        assets_manufacturer = session.query(AssetsManufacturer).filter(AssetsManufacturer.id == id).first()
        if assets_manufacturer:
            return {
                'manufacturer_id': assets_manufacturer.id,
                'manufacturer_acronym': assets_manufacturer.acronym,
                'manufacturer_description': assets_manufacturer.description
            }
        else:
            return {}
    except Exception as e:
        print(f"Error in buscar_fabricantes: {e}")
        return {}
    finally:
        session.close()


def buscar_familia_bens(id):
    session = create_session()
    try:
        assets_family = session.query(AssetsFamily).filter(AssetsFamily.id == id).first()
        if assets_family:
            return {
                'family_id': assets_family.id,
                'manufacturer_description': assets_family.description
            }
        else:
            return {}
    except Exception as e:
        print(f"Error in buscar_familia_bens: {e}")
        return {}
    finally:
        session.close()


def buscar_centro_custo(id):
    session = create_session()
    try:
        cost_center = session.query(CostCenter).filter(CostCenter.id == id).first()
        if cost_center:
            return {
                'model_type_id': cost_center.id,
                'model_type_description': cost_center.description
            }
        else:
            return {}
    except Exception as e:
        print(f"Error in buscar_centro_custo: {e}")
        return {}
    finally:
        session.close()


def add_assets():
    session = None
    try:
        current_date = datetime.now().strftime("%d/%m/%Y")
        if request.method == 'POST':
            print(request.form)
            id = request.form['id']
            family_id = request.form['family_id']
            model_type_id = request.form['model_type_id']
            manufacturer_id = request.form['manufacturer_id']
            model_unit = request.form['model_unit']
            serial_unit = request.form['serial_unit']
            cost_center_id = request.form['cost_center_id']
            purchase_value = request.form['purchase_value']
            purchase_date = request.form['purchase_date']
            purchase_nf = request.form['purchase_nf']
            year_manufacture = request.form['year_manufacture']
            age = request.form['age']
            engine_manufacturer_id = request.form['engine_manufacturer_id']
            engine_model = request.form['engine_model']
            characteristics = request.form['characteristics']
            tank = request.form['tank']
            metrics = request.form['metrics']
            tank_property = request.form['tank_property']
            voltage = request.form['voltage']
            date_issue = current_date
            current = request.form['current']
            average = request.form['average']
            weight = request.form['weight']
            situation = request.form['situation']
            product_id = request.form['product_id']
            meter = request.form['meter']
            meter_type = request.form['meter_type']
            meter_position = request.form['meter_position']
            accumulated_meter = request.form['accumulated_meter']
            meter_limit = request.form['meter_limit']
            date_followup = request.form['date_followup']
            print(f"Debug: current_date={current_date}")

            session = create_session()

            bens = Assets(
                id=id,
                model_type_id=model_type_id,
                family_id=family_id,
                manufacturer_id=manufacturer_id,
                model_unit=model_unit,
                serial_unit=serial_unit,
                cost_center_id=cost_center_id,
                purchase_value=purchase_value,
                purchase_date=purchase_date,
                purchase_nf=purchase_nf,
                year_manufacture=year_manufacture,
                age=age,
                engine_manufacturer_id=engine_manufacturer_id,
                engine_model=engine_model,
                characteristics=characteristics,
                tank=tank,
                metrics=metrics,
                tank_property=tank_property,
                voltage=voltage,
                date_issue=date_issue,
                current=current,
                average=average,
                weight=weight,
                situation=situation,
                product_id=product_id,
                meter=meter,
                meter_type=meter_type,
                meter_position=meter_position,
                accumulated_meter=accumulated_meter,
                meter_limit=meter_limit,
                date_followup=date_followup
            )

            session.add(bens)
            session.commit()

            print("Debug: Form submitted successfully")

        return render_template('bens.html', current_date=current_date)

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        if session:
            session.close()


def buscar_assets():
    session = create_session()
    try:
        
        return

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        if session:
            session.close()


def add_assets_follow_up(assets_follow_up):
    session = create_session()
    try:
        if not isinstance(assets_follow_up, list):
            raise ValueError("Esperava-se uma lista de dados para Assets Follow Up")

        last_assets_id = session.query(func.max(AssetsFollowUp.id)).scalar() or 0

        for asset in assets_follow_up:
            current_id = asset.get('follow_up_id')
            if current_id is None or current_id in ('', "None"):
                last_assets_id += 1
                current_id = last_assets_id
            assets = AssetsFollowUp(
                id=current_id,
                contract_id=asset.get('contract_id', ''),
                dt_start=asset.get('dt_start', ''),
                dt_end=asset.get('dt_end', ''),
                diesel_sent=asset.get('diesel_sent', ''),
                diesel_used=asset.get('diesel_used', ''),
                diesel_returned=asset.get('diesel_returned', ''),
                franchise=asset.get('franchise', ''),
                initial_horimeter=asset.get('initial_horimeter', ''),
                final_horimeter=asset.get('final_horimeter', ''),
                total_hours=asset.get('total_hours', ''),
                extra_hours=asset.get('assets_id', ''),
                value_extra_hours=asset.get('value_extra_hours', ''),
                nf_rem=asset.get('nf_rem', ''),
                dt_rem=asset.get('det_rem', ''),
                nf_ret=asset.get('nf_ret', ''),
                dt_ret=asset.get('dt_ret', ''),
                vr_day_loc=asset.get('vr_day_loc', ''),
                description=asset.get('description', ''),
                asset_cod=asset.get('asset_cod', ''),
                value_nf=asset.get('value_nf', ''),
                obs=asset.get('obs', '')
            )
            print("Assets Follow Up: ", assets)
            session.merge(assets)
            session.commit()

        return jsonify(success=True)

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return jsonify(success=False, error=str(e))

    finally:
        session.close()


def buscar_assets_follow_up(contract_id):
    session = create_session()

    try:
        assets = session.query(AssetsFollowUp).filter_by(contract_id=contract_id).all()

        follow_up_dict = {
            'assets': [
                {
                    'follow_up_id': asset.id, 'contract_id': asset.contract_id, 'asset_cod': asset.asset_cod,
                    'dt_start': asset.dt_start, 'dt_end': asset.dt_end, 'diesel_sent': asset.diesel_sent,
                    'diesel_used': asset.diesel_used, 'diesel_returned': asset.diesel_returned,
                    'franchise': asset.franchise, 'initial_horimeter': asset.initial_horimeter,
                    'final_horimeter': asset.final_horimeter, 'total_hours': asset.total_hours, 'obs': asset.obs,
                    'extra_hours': asset.extra_hours, 'value_extra_hours': asset.value_extra_hours,
                    'nf_rem': asset.nf_rem, 'dt_rem': asset.dt_rem, 'nf_ret': asset.nf_ret, 'dt_ret': asset.dt_ret,
                    'vr_day_loc': asset.vr_day_loc, 'description': asset.description, 'value_nf': asset.value_nf
                }
                for asset in assets
            ]
        }
        return [follow_up_dict]

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()
