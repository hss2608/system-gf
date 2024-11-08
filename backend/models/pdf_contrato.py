from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT, TA_LEFT
from num2words import num2words
import io
import locale
from datetime import datetime


def gerar_pdf_contrato(contract_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1*cm, leftMargin=1*cm, topMargin=1*cm, bottomMargin=2*cm)
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    contract_dict = contract_data[0]
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    estilo1 = ParagraphStyle(
        name="estilo1",
        parent=styles['Normal'],
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=colors.black,
        alignment=1,
        spaceAfter=3
    )

    estilo2 = ParagraphStyle(
        name="estilo2",
        parent=styles['Normal'],
        fontName="Helvetica-Bold",
        fontSize=7,
        textColor=colors.black,
        alignment=1
    )

    estilo3 = ParagraphStyle(
        name="estilo3",
        parent=styles['Normal'],
        fontName="Helvetica-Oblique",
        fontSize=9,
        textColor=colors.black,
        alignment=1,
    )

    titulo_estilo = ParagraphStyle(
        name='CustomStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        textColor=colors.black,
        alignment=TA_CENTER,
        leftIndent=0,
        rightIndent=0
    )

    estilo_texto_apresentacao = ParagraphStyle(
        name='styleText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        alignment=TA_JUSTIFY,
    )

    estilo_cliente_negrito = ParagraphStyle(
        name='estiloClienteNegrito',
        fontName='Helvetica-Bold',
        fontSize=8,
        spaceAfter=6,
    )

    style_bold = ParagraphStyle(
        name='estiloCliente',
        fontName='Helvetica-Bold',
        fontSize=6,
        alignment=TA_CENTER,
        leading=8
    )

    estilo_equipamentos1 = ParagraphStyle(
        name='estiloEquipamentos1',
        fontName='Helvetica',
        fontSize=7,
        alignment=TA_CENTER
    )

    estilo_equipamentos2 = ParagraphStyle(
        name='estiloEquipamentos2',
        fontName='Helvetica',
        fontSize=7,
        alignment=TA_LEFT
    )

    estilo_equipamentos3 = ParagraphStyle(
        name='estiloEquipamentos3',
        fontName='Helvetica',
        fontSize=7,
        alignment=TA_RIGHT
    )

    rodape_estilo = ParagraphStyle(
        name='RodapeStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=colors.black,
        alignment=TA_LEFT,
    )

    cabecalho2_direita_estilo = ParagraphStyle(
        name='Cabecalho2DirStyle',
        fontName='Helvetica',
        fontSize=7,
        textColor=colors.black,
        alignment=TA_RIGHT,
    )

    cabecalho2_esquerda_estilo = ParagraphStyle(
        name='Cabecalho2EsqStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        textColor=colors.black,
        alignment=TA_LEFT,
        leading=5
    )

    cond_gerais_style = ParagraphStyle(
        name='CondGeraisStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.75,
        textColor=colors.black,
        leftIndent=0,
        spaceAfter=0,
        leading=2.2,
        alignment=TA_JUSTIFY
    )

    estilo_assinatura = ParagraphStyle(
        name='styleTextAssign',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=5,
        alignment=TA_JUSTIFY,
    )

    estilo_assinatura2 = ParagraphStyle(
        name='styleTextAssign',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=5,
        alignment=TA_CENTER,
    )
    elementos = []

    caminho_logotipo = "C:\\Users\\Henrique.santos\\PycharmProjects\\sistemaGF\\backend\\logo_geraforca.png"
    logo = Image(caminho_logotipo, width=9 * cm, height=2 * cm)
    cabecalho = [
        ("LOCAÇÃO DE GRUPO GERADORES", estilo1),
        ("CONVENCIONAIS, CARENADOS E SILENCIADOS DE 16 A 1000 kVA", estilo2),
        ("Matriz SP - Fone/Fax: (11)4612-2466", estilo3),
        ("Filial MG - Fone/Fax: (31)3394-7840", estilo3),
        ("geraforca@geraforca.com.br<br/>www.locacaogeradores.srv.br - www.geraforca.com.br", estilo3),
    ]

    paragrafos_cabecalhos = [Paragraph(linha[0], linha[1]) for linha in cabecalho]
    data = [[logo, paragrafos_cabecalhos]]

    tabela_cabecalho = Table(data, colWidths=[10*cm, 10*cm])
    tabela_cabecalho.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('LEFTPADDING', (1, 0), (1, 0), 10),
        ('RIGHTPADDING', (0, 0), (0, 0), 5),
    ]))

    elementos.append(tabela_cabecalho)
    elementos.append(Spacer(1, 12))

    numero_contrato = contract_dict['contrato']['contract_id']

    titulo_contrato = f"""
        CONTRATO DE LOCAÇÃO DE EQUIPAMENTOS N° {numero_contrato}
    """

    elementos.append(Paragraph(titulo_contrato, titulo_estilo))
    elementos.append(Spacer(1, 16))

    texto_apresentacao = """
        Pelo presente instrumento, GERAFORÇA LOCAÇÃO E COMERCIO DE EQUIPAMENTOS LTDA., sociedade com sede na Estrada do
        Capuava,6351, Moinho Velho - Alt. Km 26 - Rod Raposo Tavares, município de Cotia, estado de São Paulo, com CNPJ n°
        53.002.077/0001-67, neste ato representada de acordo com o seu contrato social, por seu procurador abaixo assinado,
        doravante denominada simplemente LOCADORA dá em locação, à sociedade a seguir nomeada, daqui por diante denominada
        LOCATÁRIA os bens móveis abaixo descritos e identificados, mediante as cláusulas e condições estipuladas neste contrato.
    """

    elementos.append(Paragraph(texto_apresentacao, estilo_texto_apresentacao))
    elementos.append(Spacer(1, 12))

    dados_cliente = [
        [Paragraph('<b>LOCATÁRIA:</b>', estilo_cliente_negrito), contract_dict['company'], '', '', '', '', ''],
        [Paragraph('<b>ENDEREÇO:</b>', estilo_cliente_negrito), contract_dict['company_address'], '', '', '', '', ''],
        [Paragraph('<b>Município:</b>', estilo_cliente_negrito), contract_dict['municipio'], '', '', Paragraph('<b>UF:</b>', estilo_cliente_negrito), contract_dict['uf'], ''],
        [Paragraph('<b>Bairro:</b>', estilo_cliente_negrito), contract_dict['bairro'], '', '', Paragraph('<b>CEP:</b>', estilo_cliente_negrito), contract_dict['cep'], ''],
        [Paragraph('<b>C.N.P.J./CPF:</b>', estilo_cliente_negrito), contract_dict['cpf_cnpj'], '', '', Paragraph('<b>INSCR. ESTADUAL/RG:</b>', estilo_cliente_negrito), contract_dict['state_registration'], '']
    ]

    tabela_cliente = Table(dados_cliente, colWidths=[3 * cm, 5 * cm, 1 * cm, 1 * cm, 5 * cm, 3 * cm, 1 * cm],
                           rowHeights=[0.4 * cm] * len(dados_cliente))
    tabela_cliente.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))

    elementos.append(tabela_cliente)
    elementos.append(Spacer(1, 6))

    titulos_equipamentos = [
        [Paragraph('<b>ITEM</b>', style_bold),
         Paragraph('<b>EQUIPAMENTO BÁSICO/FORNECE. COMPLEMENTARES</b>', style_bold),
         Paragraph('<b>VALOR BÁSICO</b>', style_bold),
         Paragraph('<b>TARIFA</b>', style_bold), ],
        ['', '', '', Paragraph('<b>UNITÁRIO</b>', style_bold), Paragraph('<b>TOTAL</b>', style_bold)]
    ]

    linhas_equipamentos = []
    for idx, equipamento in enumerate(contract_dict['produtos'], start=1):
        linha = [
            Paragraph(str(idx), estilo_equipamentos1),
            Paragraph(f"{equipamento['description'] + ' ' + equipamento['add_description']}", estilo_equipamentos2),
            Paragraph(f"{equipamento['valor_basico']:2f}", estilo_equipamentos1),
            Paragraph(equipamento['unit_price'], estilo_equipamentos3),
            Paragraph(equipamento['price'], estilo_equipamentos3)
        ]
        linhas_equipamentos.append(linha)

    num_total_linhas = 13
    linhas_faltando = num_total_linhas - len(linhas_equipamentos)
    for _ in range(linhas_faltando):
        linha_vazia = ['', '', '', '', '']
        linhas_equipamentos.append(linha_vazia)

    tabela_dados_equipamentos = titulos_equipamentos + linhas_equipamentos

    tabela_equipamentos = Table(tabela_dados_equipamentos, colWidths=[1.1 * cm, 11 * cm, 3 * cm, 2 * cm, 2 * cm],#19.1cm
                                rowHeights=[0.5 * cm, 0.5 * cm, 0.7 * cm, 0.7 * cm, 0.7 * cm, 0.7 * cm, 0.7 * cm,
                                            0.7 * cm, 0.7 * cm, 0.7 * cm, 0.7 * cm, 0.7 * cm, 0.7 * cm, 0.7 * cm,
                                            0.7 * cm])
    tabela_equipamentos.setStyle(TableStyle([
        ('SPAN', (0, 0), (0, 1)),
        ('SPAN', (1, 0), (1, 1)),
        ('SPAN', (2, 0), (2, 1)),
        ('SPAN', (3, 0), (4, 0)),
        ('GRID', (0, 0), (-1, 1), 1, colors.black),
        ('LINEBEFORE', (0, 2), (-1, -1), 1, colors.black),
        ('LINEAFTER', (0, 2), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, 1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 1), 'MIDDLE'),
        ('LEADING', (0, 0), (-1, -1), 12),
    ]))

    elementos.append(tabela_equipamentos)

    dias_contrato = contract_dict['contrato']['contract_days']
    service_price = contract_dict['servicos'][0]['service_price'].replace('R$', '').replace('.', '').replace(',', '.')
    preco_servico = float(service_price)

    for idx, equipamento in enumerate(contract_dict['produtos'], start=1):
        valor_unitario = float(equipamento['unit_price'])
        rental_hours = int(equipamento['rental_hours'])
        preco_produtos = dias_contrato * valor_unitario
        total_geral = preco_produtos + preco_servico

        infos = [
            [Paragraph('<b>DATA INICIAL</b>', style_bold),
             Paragraph(f"{contract_dict['contrato']['start_contract']}", estilo_equipamentos1),
             Paragraph('<b>DATA FINAL</b>', style_bold),
             Paragraph(f"{contract_dict['contrato']['end_contract']}", estilo_equipamentos1),
             Paragraph('<b>PRAZO</b>', style_bold),
             Paragraph(f"{dias_contrato} dia(s)", estilo_equipamentos1),
             Paragraph('<b>TOTAL</b>', style_bold),
             Paragraph(f"R$ {locale.format_string('%.2f', preco_produtos, grouping=True)}", estilo_equipamentos1)],

            [Paragraph('<b>FRANQUIA</b>', style_bold),
             Paragraph(f"{rental_hours} hora(s) / dia", estilo_equipamentos2),
             Paragraph('', estilo_equipamentos1),
             Paragraph('', estilo_equipamentos1),
             Paragraph('<b>FATURAMENTO MINIMO</b>', style_bold),
             Paragraph(f"{dias_contrato} dia(s)", estilo_equipamentos1),
             Paragraph('<b>DESPESAS ADICIONAIS</b>', style_bold),
             Paragraph(f"R$ {locale.format_string('%.2f', preco_servico, grouping=True)}", estilo_equipamentos1)],

            [Paragraph('<b>CONDIÇÕES DE PAGAMENTO</b>', style_bold),
             Paragraph(f"{contract_dict['payment_condition']}", estilo_equipamentos2),
             Paragraph('', estilo_equipamentos1),
             Paragraph('', estilo_equipamentos1),
             Paragraph('', estilo_equipamentos1),
             Paragraph('', estilo_equipamentos1),
             Paragraph('<b>TOTAL GERAL</b>', style_bold),
             Paragraph(f"R$ {locale.format_string('%.2f', total_geral, grouping=True)}", estilo_equipamentos1)],

            [Paragraph('<b>LOCAL PAGAMENTO</b>', style_bold),
             Paragraph(f"CEP: {contract_dict['billing_cep']} - {contract_dict['billing_address']} - "
                       f"{contract_dict['billing_bairro']} -"
                       f" {contract_dict['billing_municipio']} - {contract_dict['billing_uf']}", estilo_equipamentos2)
             ],

            [Paragraph('<b>LOCAL INSTALAÇÃO</b>', style_bold),
             Paragraph(f"{contract_dict['delivery_address']}", estilo_equipamentos2)
             ],

            [Paragraph('<b>TRANSPORTADORA</b>', style_bold),
             Paragraph(f"GERAFORÇA LOCACAO E COM. DE EQUIP. LTDA", estilo_equipamentos2)
             ],

            [Paragraph('<b>OBSERVAÇÕES</b>', style_bold),
             Paragraph(f"{contract_dict['contrato']['contract_comments']}", estilo_equipamentos2)
             ]
        ]

        tabela_infos_contrato = Table(infos, colWidths=[2.7 * cm, 2.07 * cm, 2.17 * cm, 2.6 * cm, 2.38 * cm,
                                                        2.4 * cm, 2.18 * cm, 2.6 * cm],
                                      rowHeights=[0.7 * cm, 0.7 * cm, 0.7 * cm, 0.7 * cm, 0.7 * cm, 0.7 * cm, 2 * cm]) # * len(infos))

        tabela_infos_contrato.setStyle(TableStyle([
            ('SPAN', (1, 1), (3, 1)),
            ('SPAN', (1, 2), (5, 2)),
            ('SPAN', (1, 3), (7, 3)),
            ('SPAN', (1, 4), (7, 4)),
            ('SPAN', (1, 5), (7, 5)),
            ('SPAN', (1, 6), (7, 6)),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        elementos.append(tabela_infos_contrato)
        elementos.append(Spacer(1, 12))

        texto_rodape = """
            VISTOS DA LOCADORA E DA LOCATÁRIA NA 1ª E 2ª Via DESTE CONTRATO DE LOCAÇÃO
        """
        elementos.append(Paragraph(texto_rodape, rodape_estilo))
        elementos.append(PageBreak())

    cabecalho_condgerais = [
        [Paragraph("CONDIÇÕES GERAIS", cabecalho2_esquerda_estilo),
         Paragraph(f"CONTRATO N° {numero_contrato}", cabecalho2_direita_estilo)],
        [Paragraph("I - ALUGUEL", cabecalho2_esquerda_estilo), Paragraph("", estilo_equipamentos1)],
        [Paragraph("1)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Considera-se como mínimo a ser pago pela LOCATÁRIA à LOCADORA, o aluguel estipulado no presente Contrato de Locação de Equipamentos, de acordo com as tarifas aqui", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;referidas. Esse aluguel será sempre devido e faturado, ainda que a(s) máquina(s) e/ou equipamento(s) não tenha(m) sido utilizado(s) pelo total de horas para o(s) qual(ais)", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;foi(ram) locado(s), considerando-se dias corridos de 8 (oito) horas.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("2)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;REAJUSTE DE PREÇOS - 0 aluguel será reajustado de acordo com a legislação vigente, sendo considerada como data-base a do inicio do contrato.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("3)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;HORAS-EXTRAS - Serão cobradas proporcionalmente à tarifa diária. O cálculo será feito com base na leitura do horímetro que acompanha a máquina de acordo com as", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;tarifas referidas neste contrato. Para períodos de locação acima de 30 (trinta) dias, o cálculo das horas-extras será feito com base na leitura do horímetro da máquina, nas", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;datas programadas para manutenção da mesma. Convém salientar, neste critério, que nem sempre as datas de manutenção coincidem com períodos de 30 (trinta) dias", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;corridos, ocasionando algumas vezes, períodos maiores ou menores. Para a locação na qual a manutenção da(s) máquinas) e/ou equipamento(s) ficar a cargo da", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;LOCATÁRIA, esta deverá comunicar à LOCADORA, a leitura do horímetro periodicamente (a cada 30 dias).", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("4)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Como títulos representativos de tudo que lhe seja devido por força deste instrumento, inclusive, portanto, pelos aluguéis mensais, a LOCADORA, a seu exclusivo critério,", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;poderá sacar contra a LOCATÁRIA, duplicatas ou letras de câmbio, devendo a LOCATÁRIA em qualquer das hipóteses, no prazo que para isso lhe for estabelecido, aceitar e", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;liquidar os títulos assim emitidos. Mediante entendimento com a LOCATÁRIA, poderão também por esta ser emitidas notas promissórias correspondentes ao valor do débito.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],

        [Paragraph("II - PRAZO", cabecalho2_esquerda_estilo), Paragraph("", estilo_equipamentos1)],
        [Paragraph("5)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Na contagem de prazo, inclui-se o dia de saída da(s) máquina(s) e/ou equipamento(s) do depósito da LOCADORA, ou quando os mesmos ficarem disponíveis para serem", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;retirados pela LOCATÁRIA, assim como, por ocasião de sua devolução, será computado um dia de aluguel quando a(s) máquina(s) e/ou equipamento(s) forem devolvido(s)", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pela LOCATÁRIA, ou quando o pedido de retirada for formulado pela LOCATÁRIA após às 09:30 hs. Não são descontados os dias feriados, inclusos no prazo de locação, nem", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;o tempo em que não tenham sido utilizados por motivos alheios à LOCADORA.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("6)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Caso, ao término do prazo estipulado, a LOCATÁRIA não devolver a(s) máquina(s) e/ou equipamento(s), tal fato acarretará a prorrogação automática do prazo de locação. A ", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;locação contratada só terá o seu termo final por ocasião da efetiva e real devolução com a respectiva nota fiscal, respondendo obviamente a LOCATÁRIA, pelo aluguel e", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;demais encargos devidos neste contrato.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("6.1)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;LOCADORA e LOCATÁRIA podem, após a vigência do prazo referido no Contrato de Locação de Máquina(s) e/ou Equipamento(s), a qualquer momento, dar por rescindido", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;o contrato prorrogado, nos termos constantes nesta cláusula, mediante aviso por escrito, com antecedência de 10 (dez) dias dessa sua intenção, ficando facultado à", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;LOCADORA o direito de retirar a(s) máquina(s) e/ou equipamento(s).", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("6.2)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tendo a LOCADORA feito a comunicação referida no item anterior e tendo decorrido o prazo para a devolução da(s) máquinas e/ou equipamentos e a LOCATÁRIA recusar-", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;se a entregar o(s) mesmo(s), fica a LOCATÁRIA obrigada a arcar com todas as despesas judiciais e extrajudiciais que houver, decorrente de processo que vier a ser movido", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pela LOCADORA, bem como, ao pagamento de uma multa diária de 0,5 (meio por cento) do valor do contrato, como penalização até a efetiva data da devolução, sem", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;prejuízo do aluguel devido e demais cominações legais contratuais.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("7)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;O faturamento do aluguel e encargos decorrentes dessa prorrogação será efetuado de acordo com as condições de pagamento estabelecidas neste contrato de locação e/ou", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;na data da efetiva devolução do objeto do contrato.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],

        [Paragraph("III - ENTREGA", cabecalho2_esquerda_estilo), Paragraph("", estilo_equipamentos1)],
        [Paragraph("8)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Os bens locados somente serão entregues após assinatura deste contrato e serão entregues à LOCATÁRIA através da Nota Fiscal de locação, para serem instalados e", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;utilizados na obra da LOCATÁRIA determinada no item 'Local de Instalação', constante neste contrato.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("9)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A LOCATÁRIA recebe os bens tendo testado-os, inspecionado e aprovado previamente e, portanto, declara que os mesmos se encontram em perfeito estado de", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;funcionamento e segurança e que entendeu detalhadamente sua correta utilização e operação, pelo que se obriga a devolvê-los em idênticas condições de funcionamento ao", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;final desta locação.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("10)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Nos casos em que os bens locados forem entregues na obra da LOCATÁRIA, é indispensável a presença de um responsável desta, para receber as instruções e a chave de", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;partida.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],

        [Paragraph("IV - CONDIÇÕES DE USO E VISTORIA", cabecalho2_esquerda_estilo), Paragraph("", estilo_equipamentos1)],
        [Paragraph("11)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A LOCADORA, para fiscalizar o cumprimento do acima exposto, poderá inspecionar periodicamente os bens locados, efetuando as provas e testes que forem necessários.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("12)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A LOCATÁRIA utilizará os bens locados unicamente na exploração de seus negócios de forma cuidadosa e adequados à natureza e características dos mesmos.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("13)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Todos os consertos e reparos que os bens vierem a precisar serão efetuados exclusivamente pela LOCADORA, em local de sua livre escolha.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("14)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Para melhor utilização dos bens ora locados, uma única pessoa responsável da LOCATÁRIA deverá operá-los.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],

        [Paragraph("V - ASSISTÊNCIA TÉCNICA", cabecalho2_esquerda_estilo), Paragraph("", estilo_equipamentos1)],
        [Paragraph("15)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Quando ocorrer, nos bens locados, qualquer desarranjo ou avaria devido ao desgaste ou falha mecânica normal, a LOCATÁRIA deverá informar de imediato à LOCADORA,", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sendo que essa informação deve ser completa e fiel, incluindo, dentre outros, os elementos seguintes: identificação do número de frota e tipo de máquina, local onde se", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;encontra, descrição do problema e menção do horário em que haverá pessoa responsável para atender o mecânico da Assistência Técnica da LOCADORA.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("15.1)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Se qualquer dos bens apresentar eventual falha ou defeito, muito embora observadas pela LOCATÁRIA as normas e condições de uso estabelecidas pela LOCADORA, será", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;descontado na última fatura do contrato o valor correspondente ao tempo em que ficou parado.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("15.1.1)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Para efeito de descontos da tarifa de locação referida nesta cláusula, levar-se-á em conta a hora que a LOCADORA recebeu a comunicação sobre a máquina avariada até", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a hora que a máquina e/ou equipamento voltou a funcionar de acordo com o Relatório de Assistência Técnica da LOCADORA, devidamente assinado por um funcionário", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;da LOCATÁRIA.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("15.1.2)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A comunicação mencionada no item 15.1.1. poderá ser feita verbalmente e posteriormente deverá ser confirmada por escrito, no prazo máximo de 24 (vinte e quatro)", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;horas.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("16)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;No caso em que o defeito da(s) máquina(s) e/ou equipamento(s) tenha sido originado pelo uso em discordância com as condições deste contrato, e/ou das instruções", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;especificas de sua utilização, a LOCATÁRIA será responsável por todos os reparos e consertos e o custo dos mesmos, inclusive mão-de-obra e peças serão pagos pela", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;LOCATÁRIA, a qual também não terá direito à recuperação das horas gastas com estes reparos, respondendo a LOCATÁRIA, ainda, pelas despesas de transporte dos bens", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ao estabelecimento da LOCADORA e de seu retorno, caso a máquina ou equipamento, ou alguma de suas peças e componentes tenham que ser reparados fora do local", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;onde é usado pela LOCATÁRIA; portanto, responderá a LOCATÁRIA pelo aluguel total e por todas as despesas decorrentes que lhe serão faturadas.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("17)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Entre as paralisações de responsabilidade da LOCATÁRIA, destacam-se, sem excluir outras, as seguintes: - entrada de ar no circuito de alimentação do óleo diesel, devido ao", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;esvaziamento do reservatório (falta de combustível); - entrada de água, sujeira ou estopa no circuito de alimentação de óleo diesel, devido ao uso de combustível impuro; -", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;descarga de baterias por tentativa de partida sem obedecer as instruções; - outras circunstâncias.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("18)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Fica certo que a LOCADORA em hipótese alguma responderá por eventuais prejuízos que a LOCATÁRIA venha a ter pela paralisação da(s) máquinas) e/ou equipamento(s), ", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;durante o tempo necessário ao seu conserto ou reparo, mesmo que este decorra de faltas normais, não imputáveis à LOCATÁRIA.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("19)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A LOCADORA cobrará a importância correspondente aos serviços de assistência técnica e transporte dos bens locados, com base em tabela vigente na oportunidade.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],

        [Paragraph("VI - MANUTENÇÃO", cabecalho2_esquerda_estilo), Paragraph("", estilo_equipamentos1)],
        [Paragraph("20)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A manutenção fica por conta da LOCADORA, sendo executada periodicamente na obra da LOCATÁRIA, obedecendo a uma programação. Quando as visitas normais e", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;periódicas de manutenção, com a finalidade de verificar o bom funcionamento da(s) máquinas) e/ou equipamento(s), troca de óleo, limpeza de filtros, etc. não puderem ser", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;efetuadas por motivos de responsabilidade da LOCATÁRIA, serão realizadas posteriormente e, nesses casos, faturadas com base nas tarifas de assistência técnica, cláusula", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'V-21' acima. Como motivos de impedimento das visitas são, dentre outros, citados os seguintes: a) encontrarem-se os bens locados em local diferente daquele mencionado", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;neste contrato, sem prejuízo do disposto na cláusula 'V-21' deste contrato; b) encontrarem-se os bens em local de acesso impraticável ; c) o pessoal da LOCATÁRIA ou o", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;seu responsável no local, não permitir que o mecânico da LOCADORA tenha acesso aos bens ou não permitir que a operação destes seja interrompida para a realização da", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;manutenção.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("21)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Nos casos especiais em que a manutenção fique a cargo da LOCATÁRIA, as instruções enviadas pela LOCADORA devem ser rigorosamente obedecidas pela mesma.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Exemplo: fora da Grande São Paulo.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("22)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A LOCATÁRIA se responsabiliza pelo abastecimento da(s) máquinas) e/ou equipamento(s), com exceção do óleo lubrificante, que será fornecido pela LOCADORA.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],

        [Paragraph("VII - LIMITES DE CARGAS DE GERADOR", cabecalho2_esquerda_estilo), Paragraph("", estilo_equipamentos1)],
        [Paragraph("23)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;O gerador só pode alimentar equipamentos elétricos de capacidade inferior à capacidade máxima nominal do mesmo.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("24)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Quando o gerador estiver alimentando um único motor, este não poderá ter capacidade, em HP, superior a 45% da capacidade nominal do gerador, expressa em KVA.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("25)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Se o gerador estiver alimentando vários motores de menor potência, a soma das potências dos motores, em HP, poderá chegar no máximo a 65% da capacidade do", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;gerador, expressada em KVA.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],

        [Paragraph("VIII - TREINAMENTO DE OPERADORES", cabecalho2_esquerda_estilo), Paragraph("", estilo_equipamentos1)],
        [Paragraph("26)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A LOCATÁRIA pode enviar operadores ao depósito da LOCADORA para serem treinados para operação e manutenção de geradores, mediante prévio entendimento.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
    ]

    tabela_cabecalho2 = Table(cabecalho_condgerais, colWidths=[14*cm, 6*cm])

    tabela_cabecalho2.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (0, 0), 4),
        ('LEFTPADDING', (0, 1), (0, 1), 4),
        ('LEFTPADDING', (0, 2), (0, 2), 4),
        ('LEFTPADDING', (0, 3), (0, 3), 4),
        ('LEFTPADDING', (0, 4), (0, 4), 4),
        ('LEFTPADDING', (0, 5), (0, 5), 4),
        ('LEFTPADDING', (0, 6), (0, 6), 4),
        ('LEFTPADDING', (0, 7), (0, 7), 4),
        ('LEFTPADDING', (0, 8), (0, 8), 4),
        ('LEFTPADDING', (0, 9), (0, 9), 4),
        ('LEFTPADDING', (0, 10), (0, 10), 4),
        ('LEFTPADDING', (0, 11), (0, 11), 4),
        ('LEFTPADDING', (0, 12), (0, 12), 4),
        ('LEFTPADDING', (0, 13), (0, 13), 4),
        ('LEFTPADDING', (0, 14), (0, 14), 4),
        ('LEFTPADDING', (0, 15), (0, 15), 4),
        ('LEFTPADDING', (0, 16), (0, 16), 4),
        ('LEFTPADDING', (0, 17), (0, 17), 4),
        ('LEFTPADDING', (0, 18), (0, 18), 4),
        ('LEFTPADDING', (0, 19), (0, 19), 4),
        ('LEFTPADDING', (0, 20), (0, 20), 4),
        ('LEFTPADDING', (0, 21), (0, 21), 4),
        ('LEFTPADDING', (0, 22), (0, 22), 4),
        ('LEFTPADDING', (0, 23), (0, 23), 4),
        ('LEFTPADDING', (0, 24), (0, 24), 4),
        ('LEFTPADDING', (0, 25), (0, 25), 4),
        ('LEFTPADDING', (0, 26), (0, 26), 4),
        ('LEFTPADDING', (0, 27), (0, 27), 4),
        ('LEFTPADDING', (0, 28), (0, 28), 4),
        ('LEFTPADDING', (0, 29), (0, 29), 4),
        ('LEFTPADDING', (0, 30), (0, 30), 4),
        ('LEFTPADDING', (0, 31), (0, 31), 4),
        ('LEFTPADDING', (0, 32), (0, 32), 4),
        ('LEFTPADDING', (0, 33), (0, 33), 4),
        ('LEFTPADDING', (0, 34), (0, 34), 4),
        ('LEFTPADDING', (0, 35), (0, 35), 4),
        ('LEFTPADDING', (0, 36), (0, 36), 4),
        ('LEFTPADDING', (0, 37), (0, 37), 4),
        ('LEFTPADDING', (0, 38), (0, 38), 4),
        ('LEFTPADDING', (0, 39), (0, 39), 4),
        ('LEFTPADDING', (0, 40), (0, 40), 4),
        ('LEFTPADDING', (0, 41), (0, 41), 4),
        ('LEFTPADDING', (0, 42), (0, 42), 4),
        ('LEFTPADDING', (0, 43), (0, 43), 4),
        ('LEFTPADDING', (0, 44), (0, 44), 4),
        ('LEFTPADDING', (0, 45), (0, 45), 4),
        ('LEFTPADDING', (0, 46), (0, 46), 4),
        ('LEFTPADDING', (0, 47), (0, 47), 4),
        ('LEFTPADDING', (0, 48), (0, 48), 4),
        ('LEFTPADDING', (0, 49), (0, 49), 4),
        ('LEFTPADDING', (0, 50), (0, 50), 4),
        ('LEFTPADDING', (0, 51), (0, 51), 4),
        ('LEFTPADDING', (0, 52), (0, 52), 4),
        ('LEFTPADDING', (0, 53), (0, 53), 4),
        ('LEFTPADDING', (0, 54), (0, 54), 4),
        ('LEFTPADDING', (0, 55), (0, 55), 4),
        ('LEFTPADDING', (0, 56), (0, 56), 4),
        ('LEFTPADDING', (0, 57), (0, 57), 4),
        ('LEFTPADDING', (0, 58), (0, 58), 4),
        ('LEFTPADDING', (0, 59), (0, 59), 4),
        ('LEFTPADDING', (0, 60), (0, 60), 4),
        ('LEFTPADDING', (0, 61), (0, 61), 4),
        ('LEFTPADDING', (0, 62), (0, 62), 4),
        ('LEFTPADDING', (0, 63), (0, 63), 4),
        ('LEFTPADDING', (0, 64), (0, 64), 4),
        ('LEFTPADDING', (0, 65), (0, 65), 4),
        ('LEFTPADDING', (0, 66), (0, 66), 4),
        ('LEFTPADDING', (0, 67), (0, 67), 4),
        ('LEFTPADDING', (0, 68), (0, 68), 4),
        ('LEFTPADDING', (0, 69), (0, 69), 4),
        ('LEFTPADDING', (0, 70), (0, 70), 4),
        ('LEFTPADDING', (0, 71), (0, 71), 4),
        ('LEFTPADDING', (0, 72), (0, 72), 4),
        ('LEFTPADDING', (0, 73), (0, 73), 4),
        ('LEFTPADDING', (0, 74), (0, 74), 4),
        ('LEFTPADDING', (0, 75), (0, 75), 4),
        ('LEFTPADDING', (0, 76), (0, 76), 4),
        ('LEFTPADDING', (0, 77), (0, 77), 4),
        ('LEFTPADDING', (0, 78), (0, 78), 4),
        ('LEFTPADDING', (0, 79), (0, 79), 4),
        ('LEFTPADDING', (0, 80), (0, 80), 4),
        ('LEFTPADDING', (0, 81), (0, 81), 4),
        ('LEFTPADDING', (0, 82), (0, 82), 4),
        ('LEFTPADDING', (0, 83), (0, 83), 4),
        ('RIGHTPADDING', (1, 0), (1, 0), 0),
        ('SPAN', (0, 2), (1, 2)),
        ('SPAN', (0, 3), (1, 3)),
        ('SPAN', (0, 4), (1, 4)),
        ('SPAN', (0, 5), (1, 5)),
        ('SPAN', (0, 6), (1, 6)),
        ('SPAN', (0, 7), (1, 7)),
        ('SPAN', (0, 8), (1, 8)),
        ('SPAN', (0, 9), (1, 9)),
        ('SPAN', (0, 10), (1, 10)),
        ('SPAN', (0, 11), (1, 11)),
        ('SPAN', (0, 12), (1, 12)),
        ('SPAN', (0, 13), (1, 13)),
        ('SPAN', (0, 14), (1, 14)),
        ('SPAN', (0, 15), (1, 15)),
        ('SPAN', (0, 16), (1, 16)),
        ('SPAN', (0, 17), (1, 17)),
        ('SPAN', (0, 18), (1, 18)),
        ('SPAN', (0, 19), (1, 19)),
        ('SPAN', (0, 20), (1, 20)),
        ('SPAN', (0, 21), (1, 21)),
        ('SPAN', (0, 22), (1, 22)),
        ('SPAN', (0, 23), (1, 23)),
        ('SPAN', (0, 24), (1, 24)),
        ('SPAN', (0, 25), (1, 25)),
        ('SPAN', (0, 26), (1, 26)),
        ('SPAN', (0, 27), (1, 27)),
        ('SPAN', (0, 28), (1, 28)),
        ('SPAN', (0, 29), (1, 29)),
        ('SPAN', (0, 30), (1, 30)),
        ('SPAN', (0, 31), (1, 31)),
        ('SPAN', (0, 32), (1, 32)),
        ('SPAN', (0, 33), (1, 33)),
        ('SPAN', (0, 34), (1, 34)),
        ('SPAN', (0, 35), (1, 35)),
        ('SPAN', (0, 36), (1, 36)),
        ('SPAN', (0, 37), (1, 37)),
        ('SPAN', (0, 38), (1, 38)),
        ('SPAN', (0, 39), (1, 39)),
        ('SPAN', (0, 40), (1, 40)),
        ('SPAN', (0, 41), (1, 41)),
        ('SPAN', (0, 42), (1, 42)),
        ('SPAN', (0, 43), (1, 43)),
        ('SPAN', (0, 44), (1, 44)),
        ('SPAN', (0, 45), (1, 45)),
        ('SPAN', (0, 46), (1, 46)),
        ('SPAN', (0, 47), (1, 47)),
        ('SPAN', (0, 48), (1, 48)),
        ('SPAN', (0, 49), (1, 49)),
        ('SPAN', (0, 50), (1, 50)),
        ('SPAN', (0, 51), (1, 51)),
        ('SPAN', (0, 52), (1, 52)),
        ('SPAN', (0, 53), (1, 53)),
        ('SPAN', (0, 54), (1, 54)),
        ('SPAN', (0, 55), (1, 55)),
        ('SPAN', (0, 56), (1, 56)),
        ('SPAN', (0, 57), (1, 57)),
        ('SPAN', (0, 58), (1, 58)),
        ('SPAN', (0, 59), (1, 59)),
        ('SPAN', (0, 60), (1, 60)),
        ('SPAN', (0, 61), (1, 61)),
        ('SPAN', (0, 62), (1, 62)),
        ('SPAN', (0, 63), (1, 63)),
        ('SPAN', (0, 64), (1, 64)),
        ('SPAN', (0, 65), (1, 65)),
        ('SPAN', (0, 66), (1, 66)),
        ('SPAN', (0, 67), (1, 67)),
        ('SPAN', (0, 68), (1, 68)),
        ('SPAN', (0, 69), (1, 69)),
        ('SPAN', (0, 70), (1, 70)),
        ('SPAN', (0, 71), (1, 71)),
        ('SPAN', (0, 72), (1, 72)),
        ('SPAN', (0, 73), (1, 73)),
        ('SPAN', (0, 74), (1, 74)),
        ('SPAN', (0, 75), (1, 75)),
        ('SPAN', (0, 76), (1, 76)),
        ('SPAN', (0, 77), (1, 77)),
        ('SPAN', (0, 78), (1, 78)),
        ('SPAN', (0, 79), (1, 79)),
        ('SPAN', (0, 80), (1, 80)),
        ('SPAN', (0, 81), (1, 81)),
        ('SPAN', (0, 82), (1, 82)),
        ('SPAN', (0, 83), (1, 83)),
        ('LEADING', (0, 1), (0, 2), 5)
    ]))

    elementos.append(tabela_cabecalho2)
    elementos.append(Spacer(1, 10))

    texto_rodape2 = """
        VISTOS DA LOCADORA E DA LOCATÁRIA NA 1ª E 2ª Via DESTE CONTRATO DE LOCAÇÃO
    """
    elementos.append(Paragraph(texto_rodape2, rodape_estilo))
    elementos.append(PageBreak())

    date_issue = contract_dict['contrato']['date_issue']
    date_obj = datetime.strptime(date_issue, "%d/%m/%Y")
    formatted_date = date_obj.strftime("%d de %B de %Y")

    mes_em_portugues = {
        "January": "Janeiro", "February": "Fevereiro", "March": "Março",
        "April": "Abril", "May": "Maio", "June": "Junho",
        "July": "Julho", "August": "Agosto", "September": "Setembro",
        "October": "Outubro", "November": "Novembro", "December": "Dezembro"
    }

    for english, portuguese in mes_em_portugues.items():
        formatted_date.replace(english, portuguese)

    data_contrato = formatted_date

    cond_gerais2 = [
        [Paragraph("IX - OPERADOR", cabecalho2_esquerda_estilo), Paragraph(f"CONTRATO N° {numero_contrato}", cabecalho2_direita_estilo)],
        [Paragraph("27)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sempre que um operador acompanhar a(s) máquina(s) e/ou equipamento(s) locados, serão faturadas as horas e despesas correspondentes, mediante prévio acordo,", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;conforme o estabelecido neste contrato.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],

        [Paragraph("X - RESPONSABILIDADES", cabecalho2_esquerda_estilo), Paragraph("", estilo_equipamentos1)],
        [Paragraph("28)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Está expressamente entendido entre as partes, que a LOCADORA não será responsável por qualquer perda, atraso ou prejuízo de qualquer natureza, inclusive lucros", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;cessantes, resultantes de defeitos, ineficácia ou quebra acidental da(s) máquinas) e/ou equipamentos) objeto deste contrato de locação.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("29)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Os riscos pessoais e/ou materiais da LOCATÁRIA ou de terceiros, decorrentes da utilização da(s) máquinas) e/ou equipamento(s) e acessórios locados, são de exclusiva e", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;integral responsabilidade da LOCATÁRIA.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("30)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A LOCATÁRIA responsabiliza-se pela(s) máquina(s) e/ou equipamentos e acessórios locados até o final da locação. Em caso de destruição total ou parcial, efetiva ou fictícia,", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;motivado por incêndio, queda, uso indevido, ou em caso de perda, furto, roubo ou extravio, ou ainda qualquer outro motivo não especificado neste contrato, a LOCATÁRIA", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pagará à LOCADORA o valor da(s) máquinas) e/ou equipamento(s), na data da ocorrência, pelo preço de mercado à época do efetivo pagamento, ou pagará o valor", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;equivalente aos reparos, caso o bem venha a comportar tais consertos. Neste caso, o pagamento do aluguel deverá continuar sendo efetuado pela LOCATÁRIA,", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;normalmente, até que o bem esteja em perfeitas condições de operação e conservação.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("31)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Todos os riscos materiais e pessoais inerentes ao transporte (quando efetuado pela LOCATÁRIA) e/ou a utilização dos bens, inclusive os provenientes de acidentes que", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;venham a sofrer terceiros, a própria LOCATÁRIA ou o seu pessoal, são de exclusiva responsabilidade da LOCATÁRIA.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("32)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ficam por conta da LOCATÁRIA todos os encargos e tributos de qualquer natureza que incidam ou venham a incidir sobre os bens locados.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],

        [Paragraph("XI - DEVOLUÇÃO", cabecalho2_esquerda_estilo), Paragraph("", estilo_equipamentos1)],
        [Paragraph("33)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A LOCADORA não receberá a(s) máquina(s) e/ou equipamento(s) locados em devolução sem estarem os mesmos acompanhados da respectiva Nota Fiscal de devolução.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Nessa ocasião deverá estar presente um funcionário da LOCATÁRIA com poderes bastante para assistir a verificação, tomar ciência de eventuais danos constatados, ou falta", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;de equipamentos, peças e/ou acessórios, bem como assinar a OREL - Ordem de Retirada de Equipamento Locado. A ausência de qualquer representante da LOCATÁRIA", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;valerá como concordância do termo lavrado pela LOCADORA. Peças e/ou materiais de manutenção entregues à LOCATÁRIA junto com a(s) máquina(s) e/ou equipamento(s),", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;deverão ser devolvidos com os mesmos à LOCADORA sob pena de, em não o sendo, serem debitados pelo valor atualizado de mercado.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("34)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Caso, na devolução da(s) máquina(s) e/ou equipamento(s) e acessórios, por ocasião de sua entrega pela LOCATÁRIA à LOCADORA, ou retirada por solicitação da", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;LOCADORA, ocorrer algum impedimento alheio à LOCADORA, que esta não possa recebê-los ou retira-los, serão cobradas as despesas e o aluguel da(s) máquinas) e/ou", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;equipamento(s) e acessórios até o seu efetivo recebimento.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],

        [Paragraph("XII - TRANSPORTE", cabecalho2_esquerda_estilo), Paragraph("", estilo_equipamentos1)],
        [Paragraph("35)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;O transporte será conforme consta no Contrato de Locação de Equipamentos de acordo com a tarifa ali referida.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("35.1)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Nos casos em que o transporte for de responsabilidade da LOCATÁRIA, sendo realizado pela LOCADORA, as despesas decorrentes serão debitadas como adicionais.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],

        [Paragraph("XIII - RESCISÃO CONTRATUAL", cabecalho2_esquerda_estilo), Paragraph("", estilo_equipamentos1)],
        [Paragraph("36)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A ocorrência dos eventos a seguir relacionados fará com que este contrato seja considerado vencido antecipadamente, independente de interpelação, aviso ou notificação", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;judicial ou extra-judicial, a saber: a) Falta de pagamento de qualquer débito vencido, que decorra direta ou indiretamente deste contrato; b) Protesto legítimo de título de", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;crédito, insolvência, decretação de falência, cessação de atividades ou liquidação judicial ou extra-judicial da LOCATÁRIA, assim como requerimento de concordata pela", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;LOCATÁRIA; c) A falsidade de qualquer declaração prestada pela LOCATÁRIA, neste contrato ou de informação à LOCADORA; d) Não aceitar ou negar-se a devolver à", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;LOCADORA os títulos representativos de crédito entregues para aceite.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("37)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A infração de qualquer uma das cláusulas e condições deste contrato, por parte da LOCATÁRIA, importará na rescisão de pleno direito do contrato, independentemente de", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;qualquer aviso, notificação ou procedimento judicial, obrigando a LOCATÁRIA a, incontinenti, devolver a(s) máquina(s) e/ou equipamento(s) locados, sob pena de, não o", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;fazendo, responder pelas perdas e danos que ocasionar, devendo, portanto, ser imediatamente a LOCADORA reintegrada na posse dos mesmos bens, ficando-lhe facultado", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;retirar os bens locados, respondendo a LOCATÁRIA pelas despesas que dai advirem.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("38)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;É vedado à LOCATÁRIA: a) sublocar, ceder, emprestar ou dar a(s) máquina(s) e/ou equipamento(s) em garantia de terceiros; b) remover ou transportar os bens locados do", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;local designado no contrato, sendo que, se autorizada pela LOCADORA por escrito, quanto à mudança de local, a LOCATÁRIA responderá pelas despesas que isso ocasionar", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;e por eventuais danos derivados dessa mudança; c) usar os bens locados de outro modo que não descrito no contrato.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],

        [Paragraph("XIV - OUTRAS DISPOSIÇÕES", cabecalho2_esquerda_estilo), Paragraph("", estilo_equipamentos1)],
        [Paragraph("39)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Nenhuma tolerância da LOCADORA em receber quaisquer importâncias aqui estabelecidas, ou quanto ao cumprimento de quaisquer das cláusulas aqui estipuladas, poderá", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ser entendida como aceitação, novação ou precedente.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("40)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Se, para haver qualquer crédito originário deste contrato, a LOCADORA tiver que recorrer a meios judiciais, será ela ressarcida das custas e despesas processuais, honorários", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;advocatícios, estes na base de 20% sobre o valor do débito cobrado, bem como multa contratual na base de 10% sobre o valor do contrato.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],

        [Paragraph("XV - FORO", cabecalho2_esquerda_estilo), Paragraph("", estilo_equipamentos1)],
        [Paragraph("41)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Fica eleito o foro da Comarca de Cotia, Estado de São Paulo, para dirimir as dúvidas oriundas deste contrato, com exclusão de qualquer outro, por mais privilegiado que", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;possa ser e sem prejuízo de optar a LOCADORA pelo foro do domicílio da LOCATÁRIA.", cond_gerais_style), Paragraph("", estilo_equipamentos1)],
        [Paragraph("", cabecalho2_esquerda_estilo), Paragraph("", estilo_equipamentos1)],
        [Paragraph("", cabecalho2_esquerda_estilo), Paragraph("", estilo_equipamentos1)],
        [Paragraph(f"Cotia, {data_contrato}", cabecalho2_esquerda_estilo), Paragraph("", estilo_equipamentos1)],
    ]

    tabela_cond_gerais = Table(cond_gerais2, colWidths=[14*cm, 6*cm])

    tabela_cond_gerais.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (0, 0), 4),
        ('LEFTPADDING', (0, 1), (0, 1), 4),
        ('LEFTPADDING', (0, 2), (0, 2), 4),
        ('LEFTPADDING', (0, 3), (0, 3), 4),
        ('LEFTPADDING', (0, 4), (0, 4), 4),
        ('LEFTPADDING', (0, 5), (0, 5), 4),
        ('LEFTPADDING', (0, 6), (0, 6), 4),
        ('LEFTPADDING', (0, 7), (0, 7), 4),
        ('LEFTPADDING', (0, 8), (0, 8), 4),
        ('LEFTPADDING', (0, 9), (0, 9), 4),
        ('LEFTPADDING', (0, 10), (0, 10), 4),
        ('LEFTPADDING', (0, 11), (0, 11), 4),
        ('LEFTPADDING', (0, 12), (0, 12), 4),
        ('LEFTPADDING', (0, 13), (0, 13), 4),
        ('LEFTPADDING', (0, 14), (0, 14), 4),
        ('LEFTPADDING', (0, 15), (0, 15), 4),
        ('LEFTPADDING', (0, 16), (0, 16), 4),
        ('LEFTPADDING', (0, 17), (0, 17), 4),
        ('LEFTPADDING', (0, 18), (0, 18), 4),
        ('LEFTPADDING', (0, 19), (0, 19), 4),
        ('LEFTPADDING', (0, 20), (0, 20), 4),
        ('LEFTPADDING', (0, 21), (0, 21), 4),
        ('LEFTPADDING', (0, 22), (0, 22), 4),
        ('LEFTPADDING', (0, 23), (0, 23), 4),
        ('LEFTPADDING', (0, 24), (0, 24), 4),
        ('LEFTPADDING', (0, 25), (0, 25), 4),
        ('LEFTPADDING', (0, 26), (0, 26), 4),
        ('LEFTPADDING', (0, 27), (0, 27), 4),
        ('LEFTPADDING', (0, 28), (0, 28), 4),
        ('LEFTPADDING', (0, 29), (0, 29), 4),
        ('LEFTPADDING', (0, 30), (0, 30), 4),
        ('LEFTPADDING', (0, 31), (0, 31), 4),
        ('LEFTPADDING', (0, 32), (0, 32), 4),
        ('LEFTPADDING', (0, 33), (0, 33), 4),
        ('LEFTPADDING', (0, 34), (0, 34), 4),
        ('LEFTPADDING', (0, 35), (0, 35), 4),
        ('LEFTPADDING', (0, 36), (0, 36), 4),
        ('LEFTPADDING', (0, 37), (0, 37), 4),
        ('LEFTPADDING', (0, 38), (0, 38), 4),
        ('LEFTPADDING', (0, 39), (0, 39), 4),
        ('LEFTPADDING', (0, 40), (0, 40), 4),
        ('LEFTPADDING', (0, 41), (0, 41), 4),
        ('LEFTPADDING', (0, 42), (0, 42), 4),
        ('LEFTPADDING', (0, 43), (0, 43), 4),
        ('LEFTPADDING', (0, 44), (0, 44), 4),
        ('LEFTPADDING', (0, 45), (0, 45), 4),
        ('LEFTPADDING', (0, 46), (0, 46), 4),
        ('LEFTPADDING', (0, 47), (0, 47), 4),
        ('LEFTPADDING', (0, 48), (0, 48), 4),
        ('LEFTPADDING', (0, 49), (0, 49), 4),
        ('LEFTPADDING', (0, 50), (0, 50), 4),
        ('LEFTPADDING', (0, 51), (0, 51), 4),
        ('LEFTPADDING', (0, 52), (0, 52), 4),
        ('LEFTPADDING', (0, 53), (0, 53), 4),
        ('RIGHTPADDING', (1, 0), (1, 0), 0),
        ('SPAN', (0, 1), (1, 1)),
        ('SPAN', (0, 2), (1, 2)),
        ('SPAN', (0, 3), (1, 3)),
        ('SPAN', (0, 4), (1, 4)),
        ('SPAN', (0, 5), (1, 5)),
        ('SPAN', (0, 6), (1, 6)),
        ('SPAN', (0, 7), (1, 7)),
        ('SPAN', (0, 8), (1, 8)),
        ('SPAN', (0, 9), (1, 9)),
        ('SPAN', (0, 10), (1, 10)),
        ('SPAN', (0, 11), (1, 11)),
        ('SPAN', (0, 12), (1, 12)),
        ('SPAN', (0, 13), (1, 13)),
        ('SPAN', (0, 14), (1, 14)),
        ('SPAN', (0, 15), (1, 15)),
        ('SPAN', (0, 16), (1, 16)),
        ('SPAN', (0, 17), (1, 17)),
        ('SPAN', (0, 18), (1, 18)),
        ('SPAN', (0, 19), (1, 19)),
        ('SPAN', (0, 20), (1, 20)),
        ('SPAN', (0, 21), (1, 21)),
        ('SPAN', (0, 22), (1, 22)),
        ('SPAN', (0, 23), (1, 23)),
        ('SPAN', (0, 24), (1, 24)),
        ('SPAN', (0, 25), (1, 25)),
        ('SPAN', (0, 26), (1, 26)),
        ('SPAN', (0, 27), (1, 27)),
        ('SPAN', (0, 28), (1, 28)),
        ('SPAN', (0, 29), (1, 29)),
        ('SPAN', (0, 30), (1, 30)),
        ('SPAN', (0, 31), (1, 31)),
        ('SPAN', (0, 32), (1, 32)),
        ('SPAN', (0, 33), (1, 33)),
        ('SPAN', (0, 34), (1, 34)),
        ('SPAN', (0, 35), (1, 35)),
        ('SPAN', (0, 36), (1, 36)),
        ('SPAN', (0, 37), (1, 37)),
        ('SPAN', (0, 38), (1, 38)),
        ('SPAN', (0, 39), (1, 39)),
        ('SPAN', (0, 40), (1, 40)),
        ('SPAN', (0, 41), (1, 41)),
        ('SPAN', (0, 42), (1, 42)),
        ('SPAN', (0, 43), (1, 43)),
        ('SPAN', (0, 44), (1, 44)),
        ('SPAN', (0, 45), (1, 45)),
        ('SPAN', (0, 46), (1, 46)),
        ('SPAN', (0, 47), (1, 47)),
        ('SPAN', (0, 48), (1, 48)),
        ('SPAN', (0, 49), (1, 49)),
        ('SPAN', (0, 50), (1, 50)),
        ('SPAN', (0, 51), (1, 51)),
        ('SPAN', (0, 52), (1, 52)),
        ('SPAN', (0, 53), (1, 53))
    ]))

    elementos.append(tabela_cond_gerais)
    elementos.append(Spacer(1, 36))

    assinaturas = [
        [Paragraph("Assinat.________________________________________________", estilo_assinatura), Paragraph("Assinat.________________________________________________", estilo_assinatura)],
        [Paragraph(f"{contract_dict['contact_name']}", estilo_assinatura2), Paragraph("Geraforca Locação e Comércio de Equipamentos Ltda", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("________________________________________________________", estilo_assinatura), Paragraph("________________________________________________________", estilo_assinatura)],
        [Paragraph("Nome Completo e n° RG do Representante legal da Empresa", estilo_assinatura2), Paragraph("Nome Completo e n° RG do Representante legal da Empresa", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("Assinat.________________________________________________", estilo_assinatura), Paragraph("Assinat.________________________________________________", estilo_assinatura)],
        [Paragraph("Testemunha", estilo_assinatura2), Paragraph("Testemunha", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("", estilo_assinatura2), Paragraph("", estilo_assinatura2)],
        [Paragraph("________________________________________________________", estilo_assinatura), Paragraph("________________________________________________________", estilo_assinatura)],
        [Paragraph("Nome Completo e n° RG", estilo_assinatura2), Paragraph("Nome Completo e n° RG", estilo_assinatura2)]
    ]

    tabela_assinaturas = Table(assinaturas, colWidths=[10 * cm, 10 * cm])
    tabela_assinaturas.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (0, 0), 4),
        ('RIGHTPADDING', (1, 0), (1, 0), 0),
    ]))

    elementos.append(tabela_assinaturas)
    elementos.append(Spacer(1, 12))

    texto_rodape3 = """
            FAVOR ASSINAR, IDENTIFICAR E DEVOLVER UMA VIA PARA A LOCADORA
        """
    elementos.append(Paragraph(texto_rodape3, rodape_estilo))
    elementos.append(Spacer(1, 6))

    texto_rodape4 = """
            VISTOS DA LOCADORA E DA LOCATÁRIA NA 1ª E 2ª Via DESTE CONTRATO DE LOCAÇÃO
        """
    elementos.append(Paragraph(texto_rodape4, rodape_estilo))
    doc.build(elementos)
    buffer.seek(0)
    return buffer
