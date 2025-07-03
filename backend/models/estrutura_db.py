from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'

    client_id = Column(Integer, primary_key=True)
    company = Column(String)
    corporate_name = Column(String)
    cpf_cnpj = Column(String)
    contact_name = Column(String)
    phone = Column(String)
    email = Column(String)
    number_store = Column(Integer)
    person_type = Column(String)
    company_address = Column(String)
    client_type = Column(String)
    state_registration = Column(String)
    registration_date = Column(Date)
    billing_address = Column(String)
    municipio = Column(String)
    uf = Column(String)
    cep = Column(String)
    bairro = Column(String)
    billing_municipio = Column(String)
    billing_uf = Column(String)
    billing_cep = Column(String)
    billing_bairro = Column(String)

    proposals = relationship('Proposal', back_populates='client')


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    product_code = Column(String)
    description = Column(String)
    type = Column(String)
    add_description = Column(String)
    storage = Column(String)
    price = Column(Integer)
    weigth = Column(Integer)

    proposal_product = relationship('ProposalProduct', back_populates='product')
    assets = relationship('Assets', back_populates='product')


class Refund(Base):
    __tablename__ = 'refund'

    cod = Column(Integer, primary_key=True)
    descript = Column(String)
    refund_id = Column(Integer)

    proposal_refund = relationship('ProposalRefund', back_populates='refund')


class Proposal(Base):
    __tablename__ = 'proposal'

    proposal_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.client_id'))
    date_issue = Column(Date)
    status = Column(String)
    delivery_address = Column(String)
    delivery_bairro = Column(String)
    delivery_municipio = Column(String)
    delivery_cep = Column(String)
    delivery_uf = Column(String)
    delivery_date = Column(Date)
    withdrawal_date = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date)
    period_days = Column(Integer)
    validity = Column(String)
    observations = Column(Text)
    oenf_obs = Column(Text)
    value = Column(String)
    payment_condition_id = Column(Integer, ForeignKey('payment_condition.cod'))

    client = relationship('Client', back_populates='proposals')
    products = relationship('ProposalProduct', back_populates='proposal')
    refunds = relationship('ProposalRefund', back_populates='proposal')
    contract = relationship('Contract', back_populates='proposal')
    payment_condition = relationship('PaymentCondition', back_populates='proposal')
    order = relationship('SalesOrder', back_populates='proposal')
    accessories = relationship('Accessories', back_populates='proposal')


class ProposalProduct(Base):
    __tablename__ = 'proposal_product'

    proposal_id = Column(Integer, ForeignKey('proposal.proposal_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    quantity = Column(Integer)
    unit_price = Column(String)
    price = Column(String)
    extra_hours = Column(String)
    rental_hours = Column(String)
    discount = Column(String)
    volts = Column(Integer)

    proposal = relationship('Proposal', back_populates='products')
    product = relationship('Product', back_populates='proposal_product')


class ProposalRefund(Base):
    __tablename__ = 'proposal_refund'

    proposal_id = Column(Integer, ForeignKey('proposal.proposal_id'), primary_key=True)
    cod = Column(Integer, ForeignKey('refund.cod'), primary_key=True)
    service_quantity = Column(Integer)
    service_unit_price = Column(String)
    service_price = Column(String)
    discount = Column(String)
    km = Column(String)

    proposal = relationship('Proposal', back_populates='refunds')
    refund = relationship('Refund', back_populates='proposal_refund')


class Accessories(Base):
    __tablename__ = 'accessories'

    proposal_id = Column(Integer, ForeignKey('proposal.proposal_id'), primary_key=True)
    accessories_id = Column(Integer, primary_key=True)
    accessories_description = Column(String)
    accessories_quantity = Column(String)
    meters = Column(Integer)
    accessories_unit_price = Column(String)
    accessories_days = Column(Integer)
    items_meters = Column(Integer)
    accessories_discount = Column(String)
    accessories_price = Column(String)

    proposal = relationship('Proposal', back_populates='accessories')


class Contract(Base):
    __tablename__ = 'contract'

    contract_id = Column(Integer, primary_key=True)
    proposal_id = Column(Integer, ForeignKey('proposal.proposal_id'))
    date_issue = Column(Date)
    start_contract = Column(Date)
    end_contract = Column(Date)
    contract_days = Column(Integer)
    contract_type = Column(String)
    contract_status = Column(String)
    value = Column(String)
    address_obs = Column(Text)
    observations = Column(Text)
    oenf_obs = Column(Text)
    contract_comments = Column(Text)

    proposal = relationship('Proposal', back_populates='contract')
    products_contract = relationship('ContractProducts', back_populates='contract')
    refunds_contract = relationship('ContractRefund', back_populates='contract')
    stop_cost_sub = relationship('StopCostSub', back_populates='contract')
    stop_cost_freight = relationship('StopCostFreight', back_populates='contract')
    stop_cost_op_cost = relationship('StopCostOpCost', back_populates='contract')
    rental_invoice = relationship('RentalInvoice', back_populates='contract')
    assets_follow_up = relationship('AssetsFollowUp', back_populates='contract')


class ContractProducts(Base):
    __tablename__ = 'contract_product'

    contract_id = Column(Integer, ForeignKey('contract.contract_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)

    contract = relationship('Contract', back_populates='products_contract')


class ContractRefund(Base):
    __tablename__ = 'contract_refund'

    contract_id = Column(Integer, ForeignKey('contract.contract_id'), primary_key=True)
    cod = Column(Integer, ForeignKey('refund.cod'), primary_key=True)

    contract = relationship('Contract', back_populates='refunds_contract')


class SalesOrder(Base):
    __tablename__ = 'sales_order'

    order_id = Column(Integer, primary_key=True)
    proposal_id = Column(Integer, ForeignKey('proposal.proposal_id'))

    proposal = relationship('Proposal', back_populates='order')

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "proposal_id": self.proposal_id
        }


class PaymentCondition(Base):
    __tablename__ = 'payment_condition'

    cod = Column(Integer, primary_key=True)
    description = Column(String)

    proposal = relationship('Proposal', back_populates='payment_condition')


class CostCenter(Base):
    __tablename__ = 'cost_center'

    id = Column(Integer, primary_key=True)
    description = Column(String)

    assets = relationship('Assets', back_populates='cost_center')


class AssetsFamily(Base):
    __tablename__ = 'assets_family'

    id = Column(Integer, primary_key=True)
    description = Column(String)

    def to_dict(self):
        return {
            'family_id': self.id,
            'family_description': self.description
        }

    kva_group = relationship('KvaGroup', back_populates='assets_family')
    assets = relationship('Assets', back_populates='assets_family')


class AssetsManufacturer(Base):
    __tablename__ = 'assets_manufacturer'

    id = Column(Integer, primary_key=True)
    acronym = Column(String)
    description = Column(String)

    def to_dict(self):
        return {
            'manufacturer_id': self.id,
            'acronym': self.acronym,
            'description': self.description
        }

    model_type = relationship('ModelType', back_populates='assets_manufacturer')
    manufacturer_assets = relationship(
        'Assets', back_populates='assets_manufacturer', foreign_keys='Assets.manufacturer_id'
    )
    engine_assets = relationship(
        'Assets', back_populates='engine_manufacturer', foreign_keys='Assets.engine_manufacturer_id'
    )


class KvaGroup(Base):
    __tablename__ = 'kva_group'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    family_id = Column(Integer, ForeignKey('assets_family.id'))
    quantity = Column(String)
    unit_value = Column(String)

    def to_dict(self):
        return {
            'kva_group_id': self.id,
            'kva_group_description': self.description,
            'family_id': self.family_id,
            'quantity': self.quantity,
            'unit_value': self.unit_value
        }

    assets_family = relationship('AssetsFamily', back_populates='kva_group')
    model_type = relationship('ModelType', back_populates='kva_group')


class ModelType(Base):
    __tablename__ = 'model_type'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    manufacturer_id = Column(Integer, ForeignKey('assets_manufacturer.id'))
    kva_group_id = Column(Integer, ForeignKey('kva_group.id'))
    model = Column(String)

    assets_manufacturer = relationship('AssetsManufacturer', back_populates='model_type')
    kva_group = relationship('KvaGroup', back_populates='model_type')
    assets = relationship('Assets', back_populates='model_type')

    def to_dict(self):
        return {
            'model_type_id': self.id,
            'description': self.description,
            'manufacturer_id': self.manufacturer_id,
            'acronym': self.assets_manufacturer.acronym if self.assets_manufacturer else None,
            'manufacturer_description': self.assets_manufacturer.description if self.assets_manufacturer else None,
            'kva_group_id': self.kva_group_id,
            'kva_group_description': self.kva_group.description if self.kva_group else None,
            'model': self.model
        }


class Assets(Base):
    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True)
    model_type_id = Column(Integer, ForeignKey('model_type.id'))
    family_id = Column(Integer, ForeignKey('assets_family.id'))
    manufacturer_id = Column(Integer, ForeignKey('assets_manufacturer.id'))
    model_unit = Column(String)
    serial_unit = Column(String)
    cost_center_id = Column(Integer, ForeignKey('cost_center.id'))
    purchase_value = Column(String)
    purchase_date = Column(Date)
    purchase_nf = Column(String)
    year_manufacturer = Column(Integer)
    age = Column(Integer)
    engine_manufacturer_id = Column(Integer, ForeignKey('assets_manufacturer.id'))
    engine_model = Column(String)
    characteristics = Column(String)
    tank = Column(String)
    metrics = Column(String)
    tank_property = Column(String)
    voltage = Column(String)
    date_issue = Column(Date)
    current = Column(String)
    average = Column(String)
    weight = Column(String)
    situation = Column(String)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    meter = Column(String)
    meter_type = Column(String)
    meter_position = Column(Integer)
    accumulated_meter = Column(Integer)
    meter_limit = Column(Integer)
    date_followup = Column(Date)
    cod = Column(String)

    cost_center = relationship('CostCenter', back_populates='assets')
    assets_manufacturer = relationship(
        'AssetsManufacturer', foreign_keys=[manufacturer_id], back_populates='manufacturer_assets'
    )
    engine_manufacturer = relationship(
        'AssetsManufacturer', foreign_keys=[engine_manufacturer_id], back_populates='engine_assets'
    )
    model_type = relationship('ModelType', back_populates='assets')
    assets_family = relationship('AssetsFamily', back_populates='assets')
    product = relationship('Product', back_populates='assets')
    assets_follow_up = relationship('AssetsFollowUp', back_populates='assets')


class AssetsFollowUp(Base):
    __tablename__ = 'assets_follow_up'

    id = Column(Integer, primary_key=True)
    assets_id = Column(Integer, ForeignKey('assets.id'))
    contract_id = Column(Integer, ForeignKey('contract.contract_id'))
    dt_start = Column(Date)
    dt_end = Column(Date)
    diesel_sent = Column(Integer)
    diesel_used = Column(Integer)
    diesel_returned = Column(Integer)
    franchise = Column(Integer)
    initial_horimeter = Column(Integer)
    final_horimeter = Column(Integer)
    total_hours = Column(Integer)
    extra_hours = Column(Integer)
    value_extra_hours = Column(String)
    nf_rem = Column(String)
    dt_rem = Column(Date)
    nf_ret = Column(String)
    dt_ret = Column(Date)
    vr_day_loc = Column(String)
    description = Column(String)

    assets = relationship('Assets', back_populates='assets_follow_up')
    contract = relationship('Assets', back_populates='assets_follow_up')


class StopCostSub(Base):
    __tablename__ = 'stop_cost_sub'

    stop_cost_sub_id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey('contract.contract_id'))
    sub_description = Column(String)
    sub_supplier = Column(String)
    sub_note = Column(String)
    sub_initial_period = Column(Date)
    sub_final_period = Column(Date)
    sub_rental_days = Column(Integer)
    sub_daily_value = Column(String)
    sub_value_machine = Column(String)
    sub_value_accessory = Column(String)
    sub_total_value_machines = Column(String)
    sub_total_value_accessories = Column(String)

    contract = relationship('Contract', back_populates='stop_cost_sub')


class StopCostFreight(Base):
    __tablename__ = 'stop_cost_freight'

    stop_cost_freight_id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey('contract.contract_id'))
    freight_day = Column(Date)
    freight_driver = Column(String)
    freight_finality = Column(String)
    freight_own_third = Column(String)
    freight_initial_km = Column(Integer)
    freight_final_km = Column(Integer)
    freight_total_km = Column(Integer)
    freight_cost_km = Column(String)
    freight_value_third = Column(String)
    freight_value = Column(String)
    freight_total_value = Column(String)
    freight_total_value_third = Column(String)

    contract = relationship('Contract', back_populates='stop_cost_freight')


class StopCostOpCost(Base):
    __tablename__ = 'stop_cost_op_cost'

    stop_cost_op_cost_id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey('contract.contract_id'))
    op_cost_day = Column(Date)
    op_cost_tec_driver = Column(String)
    op_cost_initial_hours = Column(String)
    op_cost_final_hours = Column(String)
    op_cost_hours = Column(String)
    op_cost_value_hours = Column(String)
    op_cost_total_value_hours = Column(String)
    op_cost_extra_hours = Column(String)
    op_cost_value_ex_hours = Column(String)
    op_cost_total_value_ex_hours = Column(String)
    op_cost_food_stay = Column(String)
    op_cost_value = Column(String)
    op_cost_total_value = Column(String)
    op_cost_total_value_food_stay = Column(String)

    contract = relationship('Contract', back_populates='stop_cost_op_cost')


class FollowUpInvoice(Base):
    __tablename__ = 'rental_invoce'

    invoice_id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey('contract.contract_id'))
    number_invoice = Column(String)
    contract_value = Column(String)
    invoice_description = Column(String)
    invoice_value = Column(String)
    initial_period = Column(Date)
    final_period = Column(Date)
    invoice_days = Column(Integer)
    invoice_venc_date = Column(Date)

    contract = relationship('Contract', back_populates='rental_invoice')


# esquema que gera automaticamente campos a partir das colunas de um modelo ou tabela SQLAlchemy
class ProposalSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Proposal
        load_instance = True
