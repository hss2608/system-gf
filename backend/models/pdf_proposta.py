from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from num2words import num2words
import io
from datetime import datetime


def gerar_pdf(proposal_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=1*cm, bottomMargin=2*cm)
    current_date = datetime.now().strftime("%d/%m/%Y")
    elementos = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    special_style = ParagraphStyle(
        name='CustomStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.black,
    )

    caminho_logotipo = "C:\\Users\\Henrique.santos\\PycharmProjects\\sistemaGF\\backend\\logo_geraforca.png"
    logo = Image(caminho_logotipo, width=9 * cm, height=2 * cm)
    logo.hAlign = 'LEFT'
    elementos.append(logo)
    elementos.append(Spacer(1, 12))

    proposal_dict = proposal_data[0]
    numero_proposta = proposal_dict['proposta']['proposal_id']

    data = [
        ['To/Para:', proposal_dict['company'], 'Proposta N°:', numero_proposta],
        ['a/c:', proposal_dict['contact_name'], 'Data:', current_date],
        ['Telefone:', proposal_dict['phone'], 'E-mail:', proposal_dict['email']],
        ['Por:', 'Promotor', 'Telefone:', '(11) 4612-2466 / 4613-3600']
    ]

    tabela = Table(data, colWidths=[2 * cm, 6 * cm, 2.5 * cm, 6 * cm])

    estilo = TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (3, 4), (3, 4), colors.blue),
    ])

    tabela.setStyle(estilo)

    elementos.append(tabela)
    elementos.append(Spacer(1, 12))

    primeiro_texto = """
    Prezados Senhores,
    """
    elementos.append(Paragraph(primeiro_texto, normal_style))
    elementos.append(Spacer(1, 6))

    segundo_texto = """
    Em atendimento a solicitação de V.S.as., apresentamos abaixo nosso melhor preço e demais condições para LOCAÇÃO 
    do(s) seguinte(s) equipamento(s):
    """
    elementos.append(Paragraph(segundo_texto, normal_style))
    elementos.append(Spacer(1, 12))

    equipamentos_titulo = """
        I) EQUIPAMENTO(S) SOLICITADO(S):
    """

    elementos.append(Paragraph(equipamentos_titulo, normal_style))

    equipment_data = [['ITEM', 'QTD', 'DESCRIÇÃO DO EQUIPAMENTO']]

    for i, equipamento in enumerate(proposal_dict['products']):
        equipment_data.append([
            str(i + 1),
            str(equipamento['quantity']),
            equipamento['description']
        ])

    tabela_equipamentos = Table(equipment_data, colWidths=[2 * cm, 2 * cm, 12 * cm])
    tabela_equipamentos.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elementos.append(tabela_equipamentos)
    elementos.append(Spacer(1, 12))

    rental_hours = proposal_dict['products'][0]['rental_hours'] if proposal_dict['products'] else 'N/A'

    terceiro_texto = f"""   
        II) PREÇO DE LOCAÇÃO PARA O PERÍODO DE {proposal_dict['proposta']['start_date']} À {proposal_dict['proposta']['end_date']} (PERÍODO DE {rental_hours} HORAS):
    """
    elementos.append(Paragraph(terceiro_texto, normal_style))
    elementos.append(Spacer(1, 3))

    valor_formatado = proposal_dict['proposta']['value']
    valor_numerico = float(valor_formatado.replace('R$', '').replace('.', '').replace(',', '.').strip())

    valor_por_extenso = num2words(valor_numerico, lang='pt').capitalize()

    valor_texto = f"""
        {valor_formatado} ({valor_por_extenso} reais)    
    """
    elementos.append(Paragraph(valor_texto, special_style))
    elementos.append(Spacer(1, 8))

    extra_hours = proposal_dict['products'][0]['extra_hours'] if proposal_dict['products'] else 'N/A'
    quarto_texto = f"""
        ATENÇÃO: HORAS EXTRAS, além da franquia do item III. 3, serão cobradas a parte razão de R$ {extra_hours} por hora 
        adicional trabalhada.
    """
    elementos.append(Paragraph(quarto_texto, normal_style))
    elementos.append(Spacer(1, 12))

    cond_gerais_titulo = "III) CONDIÇÕES GERAIS:"
    elementos.append(Paragraph(cond_gerais_titulo, normal_style))

    condicoes_gerais = [
        "1.&nbsp;&nbsp;&nbsp;&nbsp;Condição de pagamento: " + f"{proposal_dict['payment_condition']}",
        "2.&nbsp;&nbsp;&nbsp;&nbsp;Transporte: A ser efetuado pela GERAFORÇA.",
        "3.&nbsp;&nbsp;&nbsp;&nbsp;Locação mínima: " + f"{proposal_dict['proposta']['period_days']}" + " dia(s) – Franquia " + f"{rental_hours}" + " hora(s).",
        "4.&nbsp;&nbsp;&nbsp;&nbsp;Utilização do equipamento por conta da LOCATÁRIA.",
        "5.&nbsp;&nbsp;&nbsp;&nbsp;Exclusões: a) guarda e segurança. b) instalação e desinstalação dos cabos na rede. c) ponto de aterramento.",
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;d) remoção interna. e) óleo diesel.",
        "6.&nbsp;&nbsp;&nbsp;&nbsp;Manutenção preventiva e corretiva (nossos equipamentos), por conta da GERAFORÇA.",
        "7.&nbsp;&nbsp;&nbsp;&nbsp;Local da instalação: " + f"{proposal_dict['proposta']['delivery_address']}" + ".",
        "8.&nbsp;&nbsp;&nbsp;&nbsp;Inicio do contrato: = Data da entrega",
        "9.&nbsp;&nbsp;&nbsp;&nbsp;Data da entrega: Dia " + f"{proposal_dict['proposta']['delivery_date']}" + " – Retirada dia " + f"{proposal_dict['proposta']['withdrawal_date']}",
        "10.&nbsp;&nbsp;&nbsp;Solicitação de retirada deverá ser feita por E-mail/Fone;",
        "11.&nbsp;&nbsp;&nbsp;Locatária deverá verificar diariamente os níveis de óleo e água antes do funcionamento do gerador.",
        "12.&nbsp;&nbsp;&nbsp;Validade da proposta: " + f"{proposal_dict['proposta']['validity']}" + "."
    ]

    for condicao in condicoes_gerais:
        condicoes_style = ParagraphStyle(
            name='CustomStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.black,
            leftIndent=14,
            rightIndent=0,
            spaceBefore=0,
            spaceAfter=0,
            leading=8
        )
        elementos.append(Paragraph(condicao, condicoes_style))
        elementos.append(Spacer(1, 6))

    quinto_texto = """
    Solicitamos confirmarem a locação via e-mail fornecendo dados cadastrais completos para emissão de contrato e notas fiscais.
    """

    elementos.append(Paragraph(quinto_texto, normal_style))
    elementos.append(Spacer(1, 12))

    bloco_conteudo = [
        [
            Paragraph("De acordo:", normal_style),
            Paragraph("Nome.:____________________<br/>Ass.....:____________________<br/>Data...:____________________<br/>Carimbo:<br/><br/><br/>", normal_style),
            Paragraph("Atenciosamente,<br/><br/><br/>GERAFORÇA LOCAÇÃO E COMÉRCIO DE<br/>EQUIPAMENTOS LTDA.", special_style)
        ],
    ]

    # Tabela para o quadro retangular
    quadro_tabela = Table(bloco_conteudo, colWidths=[4 * cm, 8 * cm, 8 * cm])
    quadro_tabela.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('VALIGN', (0, 0), (0, 0), 'TOP'),
    ]))

    # Adiciona a tabela do quadro ao PDF
    elementos.append(quadro_tabela)
    elementos.append(Spacer(1, 1))

    texto_rodape1 = """
    Estrada do Capuava, 6.351 – Moinho Velho - Cotia - SP - CEP 06713-630 - Tel. (11) 4612-2466/ 4613-3600
    """
    rodape_style1 = ParagraphStyle(
        name='CustomStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        textColor=colors.black,
        alignment=TA_CENTER
    )
    elementos.append(Paragraph(texto_rodape1, rodape_style1))

    texto_rodape2 = """
    GERADORES "CARENADOS - SILENCIADOS"
    """

    rodape_style2 = ParagraphStyle(
        name='CustomStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=colors.black,
        alignment=TA_CENTER
    )
    elementos.append(Paragraph(texto_rodape2, rodape_style2))

    doc.build(elementos)
    buffer.seek(0)
    return buffer

# fontes: Courier, Courier-Bold, Courier-BoldOblique, Courier-Oblique, Helvetica, Helvetica-Bold, Helvetica-BoldOblique,
# Helvetica-Oblique, Symbol, Times-Bold, Times-BoldItalic, Times-Italic, Times-Roman, ZapfDingbats
