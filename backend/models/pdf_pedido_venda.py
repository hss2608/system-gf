from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import io
from datetime import datetime
from babel.dates import format_date
from backend.models.contrato import buscar_contrato_por_id, buscar_contrato_por_proposta


def gerar_pdf_pedido_venda(proposal_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=0.5 * cm,
        leftMargin=0.5 * cm,
        topMargin=0.5 * cm,
        bottomMargin=0.5 * cm
    )
    elementos = []

    caminho_logotipo = "C:\\Users\\Henrique.santos\\PycharmProjects\\sistemaGF\\backend\\logo_geraforca.png"
    logo = Image(caminho_logotipo, width=5 * cm, height=1 * cm)
    logo.hAlign = 'LEFT'

    proposal_dict = proposal_data[0]
    proposal_id = int(proposal_dict['proposta']['proposal_id'].split('/')[0])
    contract_id, contract_date_issue = buscar_contrato_por_proposta(proposal_id)
    if contract_id and contract_date_issue:
        mes = f"{contract_date_issue.month:02d}"
        ano = str(contract_date_issue.year)
        contrato_id = f"{int(contract_id):05d}/{mes}/{ano}"
    else:
        contrato_id = 'NÃO DISPONÍVEL'

    # Cabeçalho
    header_data = [
        [logo, "PEDIDO DE GMG PARA LOCAÇÃO", ''],
        ['', 'VENDEDOR: ', ''],
        [f'CONTRATO: {contrato_id}', 'OFICINA:', "Emissão.: " + datetime.now().strftime("%d/%m/%Y")],
        ["Hora..: " + datetime.now().strftime("%H:%M:%S"), '[    ] Nova Locação',
         '[    ] Acrescimo de Maquina ou Acessórios']
    ]

    cabecalho = Table(header_data, colWidths=[9.1 * cm, 9.1 * cm, 9.1 * cm])
    cabecalho.setStyle(TableStyle([
        ('SPAN', (0, 0), (0, 1)),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('FONTSIZE', (1, 0), (1, 0), 15),
        ('VALIGN', (1, 0), (1, 0), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTSIZE', (1, -1), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (0, 1), 'MIDDLE'),
        ('VALIGN', (1, -1), (-1, -1), 'MIDDLE'),
    ]))

    elementos.append(cabecalho)
    elementos.append(Spacer(1, 6))

    # Informações principais
    cliente_dados = [
        ['EMPRESA: ', proposal_dict['company'], 'CNPJ: ', proposal_dict['cpf_cnpj']]
    ]

    tabela_cliente = Table(cliente_dados, colWidths=[2 * cm, 16.3 * cm, 1.5 * cm, 7.5 * cm],
                           rowHeights=[0.5 * cm])
    tabela_cliente.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (0, 0), 7),
        ('FONTSIZE', (-2, 0), (-2, 0), 7),
        ('FONTSIZE', (1, 0), (1, 0), 8),
        ('FONTSIZE', (-1, -1), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (0, 0), colors.silver),
        ('BACKGROUND', (-2, 0), (-2, 0), colors.silver),
    ]))
    elementos.append(tabela_cliente)
    elementos.append(Spacer(1, 0.05 * cm))

    info_contatos = [
        ['CONTATOS', '', '', '', '', ''],
        ['SOLICITANTE', proposal_dict['contact_name'], 'RECEPTOR', '', 'COMPRAS', ''],
        ['TEL:', proposal_dict['phone'], 'TEL:', '', 'TEL:', ''],
    ]

    tabela_contatos = Table(info_contatos,
                            colWidths=[1.7 * cm, 7.4 * cm, 1.5 * cm, 7.6 * cm, 1.5 * cm, 7.6 * cm],
                            rowHeights=[0.4 * cm, 0.5 * cm, 0.5 * cm])
    tabela_contatos.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (0, -1), 8),
        ('FONTSIZE', (0, 1), (0, -1), 6),
        ('FONTSIZE', (2, 1), (2, -1), 6),
        ('FONTSIZE', (-2, 1), (-2, -1), 6),
        ('FONTSIZE', (1, 1), (1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.silver),
        ('BACKGROUND', (0, 1), (0, 1), colors.silver),
        ('BACKGROUND', (0, -1), (0, -1), colors.silver),
        ('BACKGROUND', (2, 1), (2, 1), colors.silver),
        ('BACKGROUND', (2, -1), (2, -1), colors.silver),
        ('BACKGROUND', (4, 1), (4, 1), colors.silver),
        ('BACKGROUND', (4, -1), (4, -1), colors.silver),
        ('LINEBELOW', (1, 1), (1, 1), 1, colors.black),
        ('LINEBELOW', (3, 1), (3, 1), 1, colors.black),
        ('LINEBELOW', (-1, 1), (-1, 1), 1, colors.black)
    ]))
    elementos.append(tabela_contatos)
    elementos.append(Spacer(1, 0.1 * cm))

    delivery_date_proposal = proposal_dict['proposta']['delivery_date']
    data_obj = datetime.strptime(delivery_date_proposal, "%d/%m/%Y")
    delivery_date = format_date(data_obj, "EEEE, dd 'de' MMMM 'de' yyyy", locale='pt_BR')

    info_transporte = [
        ['TRANSPORTE', '', '', '', '', '', '', ''],
        ['ENDEREÇO DE ENTREGA:', f"{proposal_dict['proposta']['delivery_address']} - {proposal_dict['proposta']['delivery_bairro']}", '', '',
         '', '', proposal_dict['proposta']['delivery_municipio'], ''],
        [f'FRETE: {proposal_dict['services'][0]['km']} KM', 'POR CONTA: [    ] GERAFORÇA  [    ] LOCATÁRIO',
         'GERAFORÇA', '', 'TERCEIRO (GF)', '', 'LOCATÁRIO', ''],
        ['', '', 'MOTORISTA:', '', 'MOTORISTA:', '', 'MOTORISTA', ''],
        ['Entrega solicitada para:', delivery_date, 'PLACA:', '', 'PLACA:', '', 'PLACA',
         ''],
    ]

    tabela_transporte = Table(info_transporte,
                              colWidths=[3 * cm, 6.1 * cm, 1.5 * cm, 4.5 * cm, 1.5 * cm, 4.5 * cm, 1.5 * cm, 4.7 * cm],
                              rowHeights=[0.4 * cm, 0.5 * cm, 0.5 * cm, 0.5 * cm, 0.5 * cm])
    tabela_transporte.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('SPAN', (1, 1), (5, 1)),
        ('SPAN', (-2, 1), (-1, 1)),
        ('SPAN', (2, 2), (3, 2)),
        ('SPAN', (4, 2), (5, 2)),
        ('SPAN', (-2, 2), (-1, 2)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, 1), 'LEFT'),
        ('VALIGN', (1, 1), (1, 1), 'MIDDLE'),
        ('ALIGN', (0, 1), (0, 2), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (0, 0), 8),
        ('FONTSIZE', (1, 1), (-2, 1), 9),
        ('FONTSIZE', (0, 1), (0, 1), 6),
        ('FONTSIZE', (0, 2), (-1, -1), 7),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.silver),
        ('BACKGROUND', (0, 1), (0, 1), colors.silver),
        ('BACKGROUND', (0, 2), (0, 2), colors.silver),
        ('BACKGROUND', (1, -1), (1, -1), colors.silver),
        ('BACKGROUND', (0, 1), (0, 1), colors.silver),
        ('BACKGROUND', (2, 2), (2, 2), colors.silver),
        ('BACKGROUND', (2, -1), (2, -1), colors.lightgrey),
        ('BACKGROUND', (2, -2), (2, -2), colors.lightgrey),
        ('BACKGROUND', (4, 2), (4, 2), colors.silver),
        ('BACKGROUND', (4, -1), (4, -1), colors.lightgrey),
        ('BACKGROUND', (4, -2), (4, -2), colors.lightgrey),
        ('BACKGROUND', (-2, 2), (-2, 2), colors.silver),
        ('BACKGROUND', (-2, -1), (-2, -1), colors.lightgrey),
        ('BACKGROUND', (-2, -2), (-2, -2), colors.lightgrey),
        ('LINEBELOW', (3, -2), (3, -2), 1, colors.black),
        ('LINEBELOW', (5, -2), (5, -2), 1, colors.black),
        ('LINEBELOW', (-1, -2), (-1, -2), 1, colors.black)
    ]))
    elementos.append(tabela_transporte)
    elementos.append(Spacer(1, 0.1 * cm))

    info_adicionais = [
        ['ADICIONAIS', '', ''],
        ['ACESSÓRIOS PADRÃO', '', 'CONTRATAÇÕES EXTRAS'],
        ['[    ] CABOS:   DISTÂNCIA:  ________ MTS', '[    ] QTA: ___________________________________',
         '[    ] MANUT. PREV.  ___________________________________________________'],
        ['[    ] TANQUE:  CAPACIDADE: ________ LTS', '[    ] REVERSORA (QTM) _______________________',
         '[    ] OLEO DIESEL   _________ HS DE FUNCIONAMENTO;  __________LTS'],
        ['[    ] BANDEJA:   [    ] PEQUENA    [    ] MÉDIA   [    ] GRANDE',
         '[    ] PAINEL/QD DISTRIBUIÇÃO:________________',
         '[    ] SUP. TECNICA   _________ HORAS;  NO(s) DIA(s): ______________________'],
        ['[    ] EXTINTOR', '[    ] ACESSÓRIO ADC_1: ______________________',
         '[    ] VEICULO NO LOCAL   _________ HORAS;  NO(s) DIA(s): _________________'],
        ['[    ] TOMADA __________________________', '[    ] ACESSÓRIO ADC_1: ______________________',
         '[    ] _________________________________________________________________'],
    ]

    tabela_adicionais = Table(info_adicionais,
                              colWidths=[8.5 * cm, 7.5 * cm, 11.3 * cm],
                              rowHeights=[0.5 * cm, 0.3 * cm, 0.5 * cm, 0.5 * cm, 0.5 * cm, 0.5 * cm, 0.5 * cm])
    tabela_adicionais.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('SPAN', (0, 1), (1, 1)),
        ('ALIGN', (0, 0), (-1, 1), 'CENTER'),
        ('ALIGN', (0, 2), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, 1), 6),
        ('FONTSIZE', (0, 2), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.silver),
        ('BACKGROUND', (0, 1), (1, 1), colors.lightgrey),
        ('BACKGROUND', (-1, 1), (-1, 1), colors.lightgrey),
    ]))
    elementos.append(tabela_adicionais)
    elementos.append(Spacer(1, 0.1 * cm))

    observacoes = [
        ['OBS.: ', ''],
        ['', '']
    ]

    tabela_observacoes = Table(observacoes, colWidths=[1.5 * cm, 25.8 * cm],
                               rowHeights=[0.5 * cm, 0.5 * cm])
    tabela_observacoes.setStyle(TableStyle([
        ('SPAN', (0, -1), (-1, -1)),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, 1), 6),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('BACKGROUND', (0, 0), (0, 0), colors.silver),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),
    ]))
    elementos.append(tabela_observacoes)
    elementos.append(Spacer(1, 0.1 * cm))

    geradores = [
        ['CÓDIGO GMG', 'HORÍMETRO', 'POTÊNCIA', 'TENSÃO', 'N° TANQUE', 'DIESEL', 'BAND', 'QTA/QTM',
         'CABOS/TOMADAS/OUTROS', 'METROS', 'EXTINTOR', "NF's"],
        ['', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', '']
    ]

    tabela_geradores = Table(geradores, colWidths=[2.5 * cm, 1.5 * cm, 2 * cm, 1.5 * cm, 2.5 * cm, 1.5 * cm, 1 * cm,
                                                   2.5 * cm, 6 * cm, 1.5 * cm, 3.3 * cm, 1.5 * cm],
                             rowHeights=[0.4 * cm, 0.5 * cm, 0.5 * cm, 0.5 * cm, 0.5 * cm])
    tabela_geradores.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, 1), 6),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.silver),
        ('BACKGROUND', (2, 1), (3, -1), colors.lightgrey),
    ]))
    elementos.append(tabela_geradores)
    elementos.append(Spacer(1, 0.5 * cm))

    observacoes2 = [
        ['OBSERVAÇÕES', 'OBSERVAÇÕES'],
        ['', '']
    ]

    tabela_observacoes2 = Table(observacoes2, colWidths=[13.65 * cm, 13.65 * cm],
                                rowHeights=[0.5 * cm, 2.5 * cm])
    tabela_observacoes2.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    elementos.append(tabela_observacoes2)
    elementos.append(Spacer(1, 0.1 * cm))

    infos_adc = [
        ['INFORMAÇÕES ADC.:', 'FICHA (    )', 'QUADRO (    )', 'PLANILHA (    )', 'PROTHEUS (    )', 'MATRIZ (    )',
         'ASS. RESP. LIB.:'],
        ['', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '']
    ]

    tabela_infoadc = Table(infos_adc, colWidths=[4 * cm, 3.5 * cm, 3.5 * cm, 3.5 * cm, 3.5 * cm, 3.5 * cm, 5.8 * cm],
                           rowHeights=[0.5 * cm, 0.5 * cm, 0.5 * cm])
    tabela_infoadc.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, 0), 1, colors.black),
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),
        ('LINEBELOW', (0, 1), (-1, 1), 0.5, colors.black),
    ]))
    elementos.append(tabela_infoadc)
    elementos.append(Spacer(1, 0.1 * cm))

    # Geração do PDF
    doc.build(elementos)
    buffer.seek(0)
    return buffer
