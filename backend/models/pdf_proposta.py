from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from num2words import num2words
import io
from datetime import datetime
from bs4 import BeautifulSoup


def gerar_pdf(proposal_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=3*cm, bottomMargin=3*cm)
    current_date = datetime.now().strftime("%d/%m/%Y")
    elementos = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    observations_style = ParagraphStyle(
        'ObservationsStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        spaceAfter=6
    )

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

    obs_html = proposal_dict['proposta'].get('observations', '')
    if obs_html:
        cleaned_html = clean_html_for_paragraph(obs_html)
        soup = BeautifulSoup(cleaned_html, "html.parser")
        for tag in soup.find_all(['p', 'ul', 'ol', 'li', 'br']):
            text = str(tag)
            elementos.append(Paragraph(text, observations_style))
            elementos.append(Spacer(1, 4))

    condicoes_gerais = [
        "1.&nbsp;&nbsp;&nbsp;&nbsp;Condição de pagamento: " + f"{proposal_dict['payment_condition']}",
        "2.&nbsp;&nbsp;&nbsp;&nbsp;Período de locação: Contrato de 12 meses, com reajustes anuais de acordo com os índices de IPCA;",
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;podendo estender por 24 meses ou 36 meses mediante a assinatura do termo de aditivo próprio.",
        "3.&nbsp;&nbsp;&nbsp;&nbsp;Local da instalação: " + f"{proposal_dict['proposta']['delivery_address']}" + "-" + f"{proposal_dict['proposta']['delivery_bairro']}" + "-" + f"{proposal_dict['proposta']['delivery_municipio']}" + "-" + f"{proposal_dict['proposta']['delivery_uf']}",
        "4.&nbsp;&nbsp;&nbsp;&nbsp;Transporte: Entrega e retirada por conta da GERAFORÇA conforme item II;",
        "5.&nbsp;&nbsp;&nbsp;&nbsp;Operação técnica por conta do LOCATÁRIO conforme item III;",
        "6.&nbsp;&nbsp;&nbsp;&nbsp;Combustível/abastecimento do equipamento por conta do LOCATÁRIO;",
        "7.&nbsp;&nbsp;&nbsp;&nbsp;Guarda e segurança do equipamento por conta do LOCATÁRIO;",
        "8.&nbsp;&nbsp;&nbsp;&nbsp;É de responsabilidade do LOCATÁRIO exigir, conferir e assinar os relatórios de vista técnica /",
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;medição apresentados pelos funcionários da GERAFORÇA;",
        "9.&nbsp;&nbsp;&nbsp;&nbsp;Manutenção corretiva por conta da GERAFORÇA, com despesas repassadas ao locatário, quando o",
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;defeito for proveniente da má utilização do equipamento.",
        "10.&nbsp;&nbsp;&nbsp;Manutenção preventiva a cada 300/360h por conta da GERAFORÇA;",
        "11.&nbsp;&nbsp;&nbsp;Laudos, licenças e documentações especificas, serão cobrados à parte.",
        "12.&nbsp;&nbsp;&nbsp;Acesso do equipamento ao local da instalação de responsibilidade do LOCATÁRIO;",
        "13.&nbsp;&nbsp;&nbsp;Dimensionamento de carga é de responsabilidade do LOCATÁRIO.",
        "14.&nbsp;&nbsp;&nbsp;Validade da proposta: " + f"{proposal_dict['proposta']['validity']}" + ".",
        "15.&nbsp;&nbsp;&nbsp;NF de devolução obrigatoriamente deverá ser feita pelo cliente que possua Inscrição Estadual,",
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;conforme rege legislação tributária vigente."
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

    doc.build(elementos, onFirstPage=header_footer, onLaterPages=header_footer)
    buffer.seek(0)
    return buffer


def header_footer(canvas, doc):
    canvas.saveState()

    caminho_logotipo = "C:\\Users\\Henrique.santos\\PycharmProjects\\sistemaGF\\backend\\logo_geraforca.png"
    canvas.drawImage(caminho_logotipo, 2 * cm, A4[1] - 3 * cm, width=9 * cm, height=2 * cm)

    canvas.setFillColorRGB(0.5, 0.5, 0.5)

    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             "Rua das Orquídeas, 231 - Bairro Chácara Boa Vista - Contagem - MG - CEP 32150-220 - PABX: (31) 3368-7450")

    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawCentredString(A4[0] / 2, 1.2 * cm,
                             "GERAFORÇA LOCAÇÃO E COMÉRCIO DE EQUIPAMENTOS LTDA")

    canvas.drawCentredString(A4[0] - 2 * cm, 1.2 * cm, f"Página {doc.page}")

    canvas.restoreState()


def clean_html_for_paragraph(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")

    allowed_tags = ['b', 'i', 'u', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'p']
    for tag in soup.find_all(True):
        if tag.name not in allowed_tags:
            tag.unwrap()
        else:
            tag.attrs = {}

    return str(soup)

# fontes: Courier, Courier-Bold, Courier-BoldOblique, Courier-Oblique, Helvetica, Helvetica-Bold, Helvetica-BoldOblique,
# Helvetica-Oblique, Symbol, Times-Bold, Times-BoldItalic, Times-Italic, Times-Roman, ZapfDingbats
