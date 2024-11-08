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


class ProposalProduct(Base):
    __tablename__ = 'proposal_product'

    proposal_id = Column(Integer, ForeignKey('proposal.proposal_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    quantity = Column(Integer)
    unit_price = Column(String)
    price = Column(String)
    extra_hours = Column(String)
    rental_hours = Column(String)

    proposal = relationship('Proposal', back_populates='products')
    product = relationship('Product', back_populates='proposal_product')


class ProposalRefund(Base):
    __tablename__ = 'proposal_refund'

    proposal_id = Column(Integer, ForeignKey('proposal.proposal_id'), primary_key=True)
    cod = Column(Integer, ForeignKey('refund.cod'), primary_key=True)
    service_quantity = Column(Integer)
    service_unit_price = Column(String)
    service_price = Column(String)

    proposal = relationship('Proposal', back_populates='refunds')
    refund = relationship('Refund', back_populates='proposal_refund')


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
    # products = relationship('ProposalProduct', back_populates='contract')
    # refunds = relationship('ProposalRefund', back_populates='contract')
    products_contract = relationship('ContractProducts', back_populates='contract')
    refunds_contract = relationship('ContractRefund', back_populates='contract')
    order = relationship('SalesOrder', back_populates='contract')


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
    contract_id = Column(Integer, ForeignKey('contract.contract_id'))

    contract = relationship('Contract', back_populates='order')


class PaymentCondition(Base):
    __tablename__ = 'payment_condition'

    cod = Column(Integer, primary_key=True)
    description = Column(String)

    proposal = relationship('Proposal', back_populates='payment_condition')


# esquema que gera automaticamente campos a partir das colunas de um modelo ou tabela SQLAlchemy
class ProposalSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Proposal
        load_instance = True
