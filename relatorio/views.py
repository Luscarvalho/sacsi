import io
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import FileResponse
from django.views.generic.list import ListView
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, TableStyle, LongTable, SimpleDocTemplate, Spacer
from aproveitamento.models import Aproveitamento, Aluno
from atividade.models import Atividade


class RelatorioGeral(LoginRequiredMixin, ListView):
    template_name = 'listar_relatorio.html'
    model = Aluno
    context_object_name = 'alunos'


@login_required
def exportar_dados(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch * 1.5)
    textob.setFont("Helvetica", 14)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(inch, inch, "Relatório de Aproveitamento")

    lines = []

    alunos = Aluno.objects.all()

    for aluno in alunos:
        lines.append(aluno.nome)
        lines.append("")
        lines.append('Código | Atividade | Carga Horária')
        for aproveitamento in Aproveitamento.objects.filter(aluno=aluno):
            lines.append(f'{aproveitamento.categoria} | {aproveitamento.descricao} | {aproveitamento.ch}')
        lines.append('')

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='relatorio.pdf')


@login_required
def exportar_dados_aluno_simples(request, pk):
    aluno = Aluno.objects.get(id_aluno=pk)

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)

    style_header = ParagraphStyle(
        'header',
        fontSize=14
    )

    style_cels = ParagraphStyle(
        'cels',
        fontSize=11
    )

    elements = [Paragraph(f'Nome: {aluno.nome}', style_header),
                Spacer(1, 5),
                Paragraph(f'Matrícula: {aluno.matricula}', style_header),
                Spacer(1, 20)]

    data = [['Código', 'Atividade', 'CH Realizada', 'AP Máximo']]

    aproveitamentos = Aproveitamento.objects.filter(aluno=aluno)
    codigos = aproveitamentos.values('categoria__codigo').annotate(total_ch=Sum('ch'))

    for codigo in codigos:
        aproveitamento_maximo = (
            Aproveitamento.objects.filter(categoria__codigo=codigo['categoria__codigo']).first().categoria.ap_max)
        descricao = (
            Aproveitamento.objects.filter(categoria__codigo=codigo['categoria__codigo']).first().categoria.descricao)
        data.append([codigo["categoria__codigo"],
                     Paragraph(descricao, style_cels),
                     codigo["total_ch"],
                     aproveitamento_maximo])

    table = LongTable(data, colWidths=[50, '*', 80, 80])

    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)

    doc.build(elements)

    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename=f'Relatório Simples - {aluno.nome}.pdf')


@login_required
def exportar_dados_aluno_completo(request, pk):
    aluno = Aluno.objects.get(id_aluno=pk)

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)

    style_header = ParagraphStyle(
        'header',
        fontSize=14
    )

    style_cels = ParagraphStyle(
        'cels',
        fontSize=11
    )

    elements = [Paragraph(f'Nome: {aluno.nome}', style_header),
                Spacer(1, 5),
                Paragraph(f'Matrícula: {aluno.matricula}', style_header),
                Spacer(1, 20)]

    data = [['Código', 'Atividade', 'CH Realizada', 'AP Máximo']]

    aproveitamentos = Aproveitamento.objects.filter(aluno=aluno)
    codigos = aproveitamentos.values('categoria__codigo').annotate(total_ch=Sum('ch'))
    modalidades = aproveitamentos.values('categoria__modalidade').annotate(total_ch=Sum('ch'))

    for codigo in codigos:
        aproveitamento_maximo = (
            Aproveitamento.objects.filter(categoria__codigo=codigo['categoria__codigo']).first().categoria.ap_max)
        descricao = (
            Aproveitamento.objects.filter(categoria__codigo=codigo['categoria__codigo']).first().categoria.descricao)
        data.append([codigo["categoria__codigo"],
                     Paragraph(descricao, style_cels),
                     codigo["total_ch"],
                     aproveitamento_maximo])

    table = LongTable(data, colWidths=[50, '*', 80, 80])

    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    data = [['Código', 'Atividade', 'CH Realizada']]

    for aproveitamento in aproveitamentos:
        data.append([aproveitamento.categoria.codigo,
                     Paragraph(aproveitamento.descricao, style_cels),
                     f'{aproveitamento.ch}'])

    table = LongTable(data, colWidths=[50, '*', 80])

    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    style = ParagraphStyle(
        'normal',
        fontSize=12
    )

    for modalidade in modalidades:
        atividade = Atividade.objects.filter(modalidade=modalidade["categoria__modalidade"]).first()
        nome_completo_modalidade = atividade.get_modalidade_display()
        elements.append(
            Paragraph(f'Total de horas na modalidade '
                      f'{nome_completo_modalidade}: '
                      f'{modalidade["total_ch"]} horas', style))

    total_ch = aproveitamentos.aggregate(total_ch=Sum('ch'))['total_ch'] or 0
    elements.append(Paragraph(f'Total de horas: {total_ch} horas', style))
    if total_ch > 170:
        elements.append(Paragraph(f'Horas excedentes: {total_ch - 170} horas', style))
    elif total_ch == 170:
        elements.append(Paragraph('Horas completas', style))
    else:
        elements.append(Paragraph(f'Falta para completar: {170 - total_ch} horas', style))

    doc.build(elements)

    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename=f'Relatório Completo - {aluno.nome}.pdf')
