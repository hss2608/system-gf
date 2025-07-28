from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import io
from datetime import datetime


def gerar_pdf_pedido_venda(order_id, proposal_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=1 * cm,
        leftMargin=1 * cm,
        topMargin=1 * cm,
        bottomMargin=1 * cm
    )
    elementos = []

    caminho_logotipo = "C:\\Users\\Henrique.santos\\PycharmProjects\\sistemaGF\\backend\\logo_geraforca.png"
    logo = Image(caminho_logotipo, width=3 * cm, height=0.68 * cm)
    logo.hAlign = 'LEFT'
    elementos.append(logo)
    elementos.append(Spacer(1, 3))

    proposal_dict = proposal_data[0]
    numero_proposta = proposal_dict['proposta']['proposal_id']
    id_pedido = order_id

    # Cabeçalho
    header_data = [
        ["Hora..: " + datetime.now().strftime("%H:%M:%S"), "Emissão do Pedido de Venda - Televendas", "Emissão.: " + datetime.now().strftime("%d/%m/%Y")],
        ["Grupo de Empresa: GERAFORÇA / Filial: MATRIZ", '', ''],
        ['', '', '']
    ]

    cabecalho = Table(header_data, colWidths=[9.1 * cm, 9.1 * cm, 9.1 * cm], rowHeights=[0.5 * cm, 0.5 * cm, 0.4 * cm])
    cabecalho.setStyle(TableStyle([
        ('SPAN', (1, 0), (1, 1)),
        ('ALIGN', (1, 0), (1, 1), 'CENTER'),
        ('VALIGN', (1, 0), (1, 1), 'MIDDLE'),
        ('SPAN', (-1, 0), (-1, 1)),
        ('ALIGN', (2, 0), (2, 1), 'RIGHT'),
        ('VALIGN', (2, 0), (2, 1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
        ('LINEBELOW', (0, 1), (-1, 1), 1, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (0, 1), 'MIDDLE'),
    ]))

    elementos.append(cabecalho)
    elementos.append(Spacer(1, 12))

    # Informações principais
    cliente_dados = [
        ["|", f'EMPRESA: {proposal_dict['proposta']['client_id']}',  '|', 'LOCAL DE ENTREGA', '|', 'ENDEREÇO DE COBRANÇA', '|'],
        ['|', proposal_dict['company'], '|', '- - - - - - - - - - - - - - - - - - - - - - - - - - - -', '|', '- - - - - - - - - - - - - - - - - - - - - - - - - -', '|'],
        ['|', proposal_dict['company_address'], '|', proposal_dict['proposta']['delivery_address'], '|', proposal_dict['billing_address'], '|'],
        ['|', proposal_dict['state_registration'], '|', f'{proposal_dict['proposta']['delivery_cep']} ' + f' {proposal_dict['proposta']['delivery_bairro']}', '|', f'{proposal_dict['billing_cep']} ' + f' {proposal_dict['billing_bairro']}', '|'],
        ['|', proposal_dict['cpf_cnpj'], '|', f'{proposal_dict['proposta']['delivery_municipio']}' + '/' + f'{proposal_dict['proposta']['delivery_uf']}', '|', f'{proposal_dict['billing_municipio']}' + '/' + f'{proposal_dict['billing_uf']}', '|'],
    ]

    tabela_cliente = Table(cliente_dados, colWidths=[0.3 * cm, 8.8 * cm, 0.3 * cm, 8.65 * cm, 0.3 * cm, 8.65 * cm, 0.3 * cm])
    tabela_cliente.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('FONTSIZE', (3, 1), (3, 1), 8),
        ('FONTSIZE', (5, 1), (5, 1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEADING', (0, 0), (-1, -1), 8),
    ]))
    elementos.append(tabela_cliente)
    elementos.append(Spacer(1, 0.5 * cm))

    info_proposta = [
        ['Atendimento :', numero_proposta, 'Pedido      :', id_pedido],
        ['Emissão     :', proposal_dict['proposta']['date_issue'], 'Desconto    :', '0, 00'],
        ['Contato     :', proposal_dict['contact_name'], 'Cond. Pagto :', proposal_dict['payment_condition']],
        ['Vendedor    :', 'Promotor', 'Mapa Carreg.:', 'NÃO CARREGA'],
        ['Transportad.:', 'GERAFORCA LOCACAO E COM. DE EQUIP. LTDA', 'Validade    :', proposal_dict['proposta']['validity']],
        ['Observação:', '', '', '']
    ]

    tabela_proposta_pedido = Table(info_proposta, colWidths=[2.5 * cm, 11.15 * cm, 2.5 * cm, 11.15 * cm])
    tabela_proposta_pedido.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
        ('LINEBELOW', (0, 4), (-1, 4), 1, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        ('LEADING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (-1, 1), (-1, 1), 35)
    ]))
    elementos.append(tabela_proposta_pedido)
    elementos.append(Spacer(1, 0.05 * cm))

    # Tabela de Itens
    itens_dados = [['Item', 'Produto', 'Descrição', 'Qtde', 'Vlr Unit.', 'Vlr Item', '%Desc.', 'Val.', 'Desc.', '%A']]
    item_counter = 1
    total_unidades = 0
    for equipamento in proposal_dict['products']:
        quantidade = int(equipamento['quantity'])
        total_unidades += quantidade
        itens_dados.append([
            str(item_counter),
            str(equipamento['product_code']),
            equipamento['description'],
            str(quantidade),
            str(equipamento['unit_price']),
            str(equipamento['price']),
            '0,00', '0,00', '0,00', '0,00',
        ])
        item_counter += 1

    for ressarcimento in proposal_dict['services']:
        quantidade = int(ressarcimento['service_quantity'])
        total_unidades += quantidade
        itens_dados.append([
            str(item_counter),
            str(ressarcimento['cod']),
            ressarcimento['descript'],
            str(quantidade),
            str(ressarcimento['service_unit_price']),
            str(ressarcimento['service_price']),
            '0,00', '0,00', '0,00', '0,00',
        ])
        item_counter += 1

    tabela_itens = Table(itens_dados, colWidths=[0.7 * cm, 4.3 * cm, 9.3 * cm, 2 * cm, 3 * cm, 3 * cm, 1.25 * cm, 1.25 * cm, 1.25 * cm, 1.25 * cm])
    tabela_itens.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEADING', (0, 0), (-1, -1), 8),
        ('LINEABOVE', (0, 1), (-1, 1), 1, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.black),
    ]))
    elementos.append(tabela_itens)
    elementos.append(Spacer(1, 0.05 * cm))

    # Resumo de valores
    resumo_dados = [['Total das quantidades:', str(total_unidades), 'Vlr.total Mercadoria:', proposal_dict['proposta']['value']]]

    tabela_resumo = Table(resumo_dados, colWidths=[17.3 * cm, 2.5 * cm, 5 * cm, 2.5 * cm])
    tabela_resumo.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elementos.append(tabela_resumo)

    # Geração do PDF
    doc.build(elementos)
    buffer.seek(0)
    return buffer
