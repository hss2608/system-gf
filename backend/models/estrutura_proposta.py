from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


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


class Refund(Base):
    __tablename__ = 'refund'

    cod = Column(Integer, primary_key=True)
    descript = Column(String)
    refund_id = Column(Integer)


class Proposal(Base):
    __tablename__ = 'proposal'

    proposal_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.client_id'))
    status = Column(String)
    delivery_address = Column(String)
    delivery_date = Column(Date)
    withdrawal_date = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date)
    period_days = Column(Integer)
    validity = Column(String)
    value = Column(String)

    client = relationship('Client', back_populates='proposals')
    products = relationship('ProposalProduct', back_populates='proposal')
    refunds = relationship('ProposalRefund', back_populates='proposal')


class ProposalProduct(Base):
    __tablename__ = 'proposal_product'

    proposal_id = Column(Integer, ForeignKey('proposal.proposal_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)

    proposal = relationship('Proposal', back_populates='products')


class ProposalRefund(Base):
    __tablename__ = 'proposal_refund'

    proposal_id = Column(Integer, ForeignKey('proposal.proposal_id'), primary_key=True)
    cod = Column(Integer, ForeignKey('refund.cod'), primary_key=True)

    proposal = relationship('Proposal', back_populates='refunds')
