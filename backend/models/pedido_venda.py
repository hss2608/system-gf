from flask import jsonify
from sqlalchemy import func
from backend.db_utils import create_session
from backend.models.estrutura_db import *
import logging
from flask import render_template


def criar_pedido(contract_id):
    session = None
    try:
        session = create_session()

        new_order = SalesOrder(contract_id=contract_id)
        session.add(new_order)
        session.commit()
        return new_order

    except Exception as e:
        session.rollback()
        print(f"Error in criar_pedido: {e}")
        raise e

    finally:
        session.close()
 