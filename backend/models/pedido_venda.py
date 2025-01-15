from flask import jsonify, render_template
from sqlalchemy import func
from backend.db_utils import create_session
from backend.models.estrutura_db import *
from sqlalchemy.orm import aliased
import logging


def criar_pedido(proposal_id, order_id):
    session = None
    try:
        session = create_session()

        new_order = SalesOrder(
            proposal_id=proposal_id,
            order_id=order_id
        )
        session.add(new_order)
        session.commit()

        pedido_dict = {
            "proposal_id": new_order.proposal_id,
            "order_id": new_order.order_id
        }
        return pedido_dict

    except Exception as e:
        session.rollback()
        print(f"Error in criar_pedido: {e}")
        raise e

    finally:
        session.close()


def sales_order_number():
    try:
        session = create_session()
        max_id = session.query(func.max(SalesOrder.order_id)).scalar()
        last_id = max_id if max_id else 0
        logging.debug(f"Last Sales Order Id: {last_id}")
        current_id = last_id + 1
        logging.debug(f"Current Id: {current_id}")
        session.close()
        return current_id

    except Exception as e:
        print(f"Error: {e}")
        # linha extra abaixo para tratar o erro JSON serializable
        return jsonify(success=False, error=str(e))


def buscar_pedido_por_id(proposal_id):
    session = create_session()

    proposal_alias = aliased(Proposal)
    sales_order_alias = aliased(SalesOrder)

    try:
        sales_order_info = session.query(proposal_alias, sales_order_alias).join(
            sales_order_alias, proposal_alias.proposal_id == sales_order_alias.proposal_id
        ).filter(proposal_alias.proposal_id == proposal_id).one_or_none()

        if not sales_order_info:
            return None

        proposta, pedido = sales_order_info

        proposal_id_formatado = f"{proposta.proposal_id:05d}"
        order_id_formatado = f"{pedido.order_id:05d}"

        pedido_dict = {
            'proposta': {
                "proposal_id": proposal_id_formatado
            },
            'order_id': order_id_formatado
        }

        return pedido_dict

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message=str(e))

    finally:
        session.close()
