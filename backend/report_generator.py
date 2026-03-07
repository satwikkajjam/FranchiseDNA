"""
PDF Report Generator - Creates professional analysis reports.
"""
import os
import io
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Frame, PageTemplate,
    BaseDocTemplate
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus.flowables import Flowable
from config import Config


# ── Color Palette ──────────────────────────────────────────────────
NAVY       = HexColor('#1B2A4A')
NAVY_LIGHT = HexColor('#2C3E6B')
ACCENT     = HexColor('#2E86DE')
ACCENT_DK  = HexColor('#1A6BBF')
GREEN      = HexColor('#27AE60')
GREEN_LITE = HexColor('#E8F8F0')
ORANGE     = HexColor('#E67E22')
ORANGE_LT  = HexColor('#FDF2E9')
RED        = HexColor('#E74C3C')
RED_LITE   = HexColor('#FDEDEC')
DARK_TEXT   = HexColor('#1C1C1E')
MID_TEXT    = HexColor('#4A4A4C')
LIGHT_TEXT  = HexColor('#8E8E93')
BORDER      = HexColor('#D5D8DC')
ROW_ALT     = HexColor('#F7F9FC')
WHITE       = HexColor('#FFFFFF')
BG_SOFT     = HexColor('#EFF2F7')

PAGE_W, PAGE_H = A4


# ── Decorative Line ───────────────────────────────────────────────
class ColorBar(Flowable):
    """A thin colored horizontal bar."""
    def __init__(self, width, height=2, color=ACCENT):
        super().__init__()
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.width, self.height, stroke=0, fill=1)


# ── Page Drawing Callbacks ────────────────────────────────────────
def _header_footer(canvas, doc):
    """Draw page number footer and thin top accent line."""
    canvas.saveState()
    # Top accent line
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.5)
    canvas.line(doc.leftMargin, PAGE_H - doc.topMargin + 8,
                PAGE_W - doc.rightMargin, PAGE_H - doc.topMargin + 8)
    # Footer
    canvas.setFont('Times-Roman', 8)
    canvas.setFillColor(LIGHT_TEXT)
    canvas.drawCentredString(PAGE_W / 2, 1.2 * cm,
                             f"FranchiseDNA Report  |  Page {doc.page}")
    canvas.restoreState()


def _title_page_cb(canvas, doc):
    """Callback for the title page (no header/footer)."""
    pass


# ── Styles ────────────────────────────────────────────────────────
def get_styles():
    styles = getSampleStyleSheet()

    # Title page
    styles.add(ParagraphStyle(
        'CoverTitle', fontSize=36, fontName='Helvetica-Bold',
        textColor=NAVY, alignment=TA_CENTER, spaceAfter=6, leading=42,
    ))
    styles.add(ParagraphStyle(
        'CoverSub', fontSize=14, fontName='Times-Roman',
        textColor=ACCENT, alignment=TA_CENTER, spaceAfter=30,
        leading=20,
    ))
    styles.add(ParagraphStyle(
        'CoverDetail', fontSize=11, fontName='Times-Roman',
        textColor=MID_TEXT, alignment=TA_CENTER, spaceAfter=4,
        leading=16,
    ))

    # TOC
    styles.add(ParagraphStyle(
        'TOCTitle', fontSize=22, fontName='Helvetica-Bold',
        textColor=NAVY, spaceBefore=0, spaceAfter=20,
    ))
    styles.add(ParagraphStyle(
        'TOCEntry', fontSize=11, fontName='Times-Roman',
        textColor=DARK_TEXT, spaceBefore=6, spaceAfter=6,
        leading=16, leftIndent=10,
    ))

    # Section & body
    styles.add(ParagraphStyle(
        'SectionNum', fontSize=20, fontName='Helvetica-Bold',
        textColor=NAVY, spaceBefore=18, spaceAfter=4, leading=24,
    ))
    styles.add(ParagraphStyle(
        'SubHead', fontSize=12, fontName='Helvetica-Bold',
        textColor=NAVY_LIGHT, spaceBefore=14, spaceAfter=4, leading=16,
    ))
    styles.add(ParagraphStyle(
        'Body', fontSize=10.5, fontName='Times-Roman',
        textColor=DARK_TEXT, spaceAfter=6, leading=15,
    ))
    styles.add(ParagraphStyle(
        'BodyBold', fontSize=10.5, fontName='Times-Bold',
        textColor=DARK_TEXT, spaceAfter=6, leading=15,
    ))
    styles.add(ParagraphStyle(
        'BulletItem', fontSize=10.5, fontName='Times-Roman',
        textColor=MID_TEXT, spaceAfter=3, leading=15,
        leftIndent=20, bulletIndent=8,
    ))

    # Risk labels
    styles.add(ParagraphStyle(
        'RiskHigh', fontSize=13, fontName='Helvetica-Bold',
        textColor=RED, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        'RiskMedium', fontSize=13, fontName='Helvetica-Bold',
        textColor=ORANGE, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        'RiskLow', fontSize=13, fontName='Helvetica-Bold',
        textColor=GREEN, spaceAfter=4,
    ))

    # Recommendation rank
    styles.add(ParagraphStyle(
        'RecTitle', fontSize=12, fontName='Helvetica-Bold',
        textColor=ACCENT_DK, spaceBefore=10, spaceAfter=2, leading=16,
    ))

    # Disclaimer
    styles.add(ParagraphStyle(
        'Disclaimer', fontSize=8, fontName='Times-Italic',
        textColor=LIGHT_TEXT, alignment=TA_CENTER, spaceBefore=20,
        leading=11,
    ))
    return styles


# ── Helpers ───────────────────────────────────────────────────────
def format_currency(amount):
    if amount >= 10000000:
        return f"\u20b9{amount / 10000000:.2f} Cr"
    elif amount >= 100000:
        return f"\u20b9{amount / 100000:.2f} L"
    elif amount >= 1000:
        return f"\u20b9{amount / 1000:.1f}K"
    return f"\u20b9{amount:,.0f}"


def fmt(num):
    return f"{int(num):,}"


def _table(data, col_widths, header_color=NAVY):
    """Build a styled table with consistent formatting."""
    t = Table(data, colWidths=col_widths, repeatRows=1)
    n_rows = len(data)
    style_cmds = [
        # Header
        ('BACKGROUND',    (0, 0), (-1, 0), header_color),
        ('TEXTCOLOR',     (0, 0), (-1, 0), WHITE),
        ('FONTNAME',      (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, 0), 9.5),
        # Body
        ('FONTNAME',      (0, 1), (-1, -1), 'Times-Roman'),
        ('FONTSIZE',      (0, 1), (-1, -1), 10),
        ('TEXTCOLOR',     (0, 1), (-1, -1), DARK_TEXT),
        # Alternating rows
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, ROW_ALT]),
        # Borders – outer + header bottom
        ('BOX',           (0, 0), (-1, -1), 0.75, BORDER),
        ('LINEBELOW',     (0, 0), (-1, 0), 1.2, header_color),
        # Inner horizontal lines only (cleaner look)
        ('LINEBELOW',     (0, 1), (-1, -2), 0.4, HexColor('#E5E7EB')),
        # Padding
        ('TOPPADDING',    (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
        # Default left-align for first col
        ('ALIGN',         (0, 0), (0, -1), 'LEFT'),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
    ]
    # Right-align value columns (everything except first)
    if len(data[0]) > 1:
        style_cmds.append(('ALIGN', (1, 0), (-1, -1), 'RIGHT'))
    t.setStyle(TableStyle(style_cmds))
    return t


def _section(elements, number, title, styles):
    """Append a numbered section header with accent bar."""
    elements.append(Paragraph(f"{number}. {title}", styles['SectionNum']))
    elements.append(ColorBar(PAGE_W - 3 * cm, 2, ACCENT))
    elements.append(Spacer(1, 10))


# ── Main Generator ────────────────────────────────────────────────
def generate_report(analysis_data, output_path=None):
    """Generate a professional PDF report with Times New Roman body text,
    Helvetica headings, color-coded sections, clean borders, and a
    table of contents."""

    if output_path is None:
        output_path = os.path.join(Config.DATA_DIR, 'franchise_report.pdf')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    buffer = io.BytesIO()

    # Build doc with two page templates: cover (no header) + normal
    doc = BaseDocTemplate(
        buffer, pagesize=A4,
        leftMargin=1.5 * cm, rightMargin=1.5 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height, id='main')
    doc.addPageTemplates([
        PageTemplate(id='Cover', frames=frame, onPage=_title_page_cb),
        PageTemplate(id='Content', frames=frame, onPage=_header_footer),
    ])

    styles = get_styles()
    E = []  # elements list

    location  = analysis_data.get('location', {})
    franchise = analysis_data.get('franchise', {})
    pop       = analysis_data.get('population', {})
    comp      = analysis_data.get('competitors', {})
    profit    = analysis_data.get('profit', {})
    risk      = analysis_data.get('risk', {})
    projs     = analysis_data.get('projections', [])
    recs      = analysis_data.get('recommendations', [])
    today     = datetime.date.today().strftime('%B %d, %Y')

    # ── COVER PAGE ────────────────────────────────────────────────
    E.append(Spacer(1, 2.2 * inch))
    E.append(ColorBar(PAGE_W - 3 * cm, 3, NAVY))
    E.append(Spacer(1, 16))
    E.append(Paragraph("FranchiseDNA", styles['CoverTitle']))
    E.append(Paragraph("Franchise Location Analysis Report", styles['CoverSub']))
    E.append(Spacer(1, 8))
    E.append(ColorBar(PAGE_W - 3 * cm, 1, ACCENT))
    E.append(Spacer(1, 30))
    E.append(Paragraph(f"<b>Location:</b>  {location.get('name', 'N/A')}", styles['CoverDetail']))
    E.append(Paragraph(
        f"<b>Coordinates:</b>  {location.get('latitude', 'N/A')}, "
        f"{location.get('longitude', 'N/A')}", styles['CoverDetail']))
    E.append(Paragraph(
        f"<b>Radius:</b>  {location.get('radius_km', 'N/A')} km", styles['CoverDetail']))
    E.append(Paragraph(
        f"<b>Franchise:</b>  {franchise.get('name', 'N/A')}", styles['CoverDetail']))
    E.append(Paragraph(f"<b>Date:</b>  {today}", styles['CoverDetail']))

    from reportlab.platypus.doctemplate import NextPageTemplate
    E.append(NextPageTemplate('Content'))
    E.append(PageBreak())

    # ── TABLE OF CONTENTS ─────────────────────────────────────────
    E.append(Paragraph("Table of Contents", styles['TOCTitle']))
    E.append(ColorBar(PAGE_W - 3 * cm, 2, NAVY))
    E.append(Spacer(1, 16))

    toc_items = [
        ("1.", "Population Analysis"),
        ("2.", "Franchise Details"),
        ("3.", "Competitor Analysis"),
        ("4.", "Profit Prediction"),
        ("5.", "Five-Year Projections"),
        ("6.", "Risk Analysis"),
        ("7.", "Franchise Recommendations"),
    ]
    toc_data = []
    for num, title in toc_items:
        toc_data.append([num, title])
    toc_table = Table(toc_data, colWidths=[0.5 * inch, 5 * inch])
    toc_table.setStyle(TableStyle([
        ('FONTNAME',     (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME',     (1, 0), (1, -1), 'Times-Roman'),
        ('FONTSIZE',     (0, 0), (-1, -1), 11),
        ('TEXTCOLOR',    (0, 0), (0, -1), ACCENT),
        ('TEXTCOLOR',    (1, 0), (1, -1), DARK_TEXT),
        ('TOPPADDING',   (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 6),
        ('LINEBELOW',    (0, 0), (-1, -2), 0.3, HexColor('#E5E7EB')),
        ('LEFTPADDING',  (0, 0), (-1, -1), 4),
        ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    E.append(toc_table)
    E.append(PageBreak())

    # ── 1. POPULATION ANALYSIS ────────────────────────────────────
    _section(E, 1, "Population Analysis", styles)

    pop_rows = [
        ['Metric', 'Value'],
        ['Total Population',       fmt(pop.get('total_population', 0))],
        ['Working Population',     fmt(pop.get('working_population', 0))],
        ['Total Households',       fmt(pop.get('total_households', 0))],
        ['Average Literacy Rate',  f"{pop.get('avg_literacy_rate', 0):.1f}%"],
        ['Population Density',     f"{pop.get('population_density', 0):,.0f} / sq km"],
        ['Areas Analyzed',         str(pop.get('areas_found', 0))],
    ]
    E.append(_table(pop_rows, [3.2 * inch, 3 * inch], NAVY))
    E.append(Spacer(1, 20))

    # ── 2. FRANCHISE DETAILS ──────────────────────────────────────
    _section(E, 2, "Franchise Details", styles)

    cat = franchise.get('category', 'N/A')
    fran_rows = [
        ['Parameter', 'Value'],
        ['Franchise Name',        franchise.get('name', 'N/A')],
        ['Category',              cat.title() if isinstance(cat, str) else str(cat)],
        ['Setup Cost',            format_currency(franchise.get('setup_cost', 0))],
        ['Avg Customer Spend',    format_currency(franchise.get('avg_customer_spend', 0))],
        ['Employees Required',    str(franchise.get('employees_required', 0))],
        ['Monthly Operating Cost', format_currency(franchise.get('monthly_operating_cost', 0))],
        ['Expected Profit Margin', f"{franchise.get('profit_margin', 0)}%"],
    ]
    E.append(_table(fran_rows, [3.2 * inch, 3 * inch], ACCENT_DK))
    E.append(Spacer(1, 20))

    # ── 3. COMPETITOR ANALYSIS ────────────────────────────────────
    _section(E, 3, "Competitor Analysis", styles)

    E.append(Paragraph(
        f"Total competitors found: <b>{comp.get('total_count', 0)}</b>  |  "
        f"Direct competitors: <b>{comp.get('direct_competitors', 0)}</b>",
        styles['Body']))
    E.append(Spacer(1, 8))

    c_list = comp.get('competitors', [])[:15]
    if c_list:
        c_rows = [['#', 'Name', 'Type', 'Brand']]
        for i, c in enumerate(c_list, 1):
            c_rows.append([
                str(i), c.get('name', 'N/A'),
                c.get('type', 'N/A'), c.get('brand', '-'),
            ])
        ct = _table(c_rows, [0.5 * inch, 2.6 * inch, 1.5 * inch, 1.4 * inch], ORANGE)
        # Left-align all columns for competitor table
        ct.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ]))
        E.append(ct)
    else:
        E.append(Paragraph("No competitors detected in the analysis radius.", styles['Body']))
    E.append(Spacer(1, 20))

    # ── 4. PROFIT PREDICTION ──────────────────────────────────────
    _section(E, 4, "Profit Prediction", styles)

    pr_rows = [
        ['Metric', 'Value'],
        ['Estimated Daily Customers', fmt(profit.get('customers_per_day', 0))],
        ['Daily Revenue',             format_currency(profit.get('daily_revenue', 0))],
        ['Monthly Revenue',           format_currency(profit.get('monthly_revenue', 0))],
        ['Yearly Revenue',            format_currency(profit.get('yearly_revenue', 0))],
        ['Yearly Operating Cost',     format_currency(profit.get('yearly_operating_cost', 0))],
        ['Yearly Profit',             format_currency(profit.get('yearly_profit', 0))],
        ['ROI',                        f"{profit.get('roi_percentage', 0):.1f}%"],
        ['Break-even Period',          f"{profit.get('months_to_breakeven', 'N/A')} months"],
        ['Profit Margin',              f"{profit.get('actual_profit_margin', 0):.1f}%"],
    ]
    E.append(_table(pr_rows, [3.2 * inch, 3 * inch], GREEN))
    E.append(Spacer(1, 14))

    # Franchise vs Bank FD comparison
    fd_rate = profit.get('bank_fd_rate', 7.5)
    bank_rows = [
        ['', 'Franchise', f'Bank FD ({fd_rate}% p.a.)'],
        ['Investment', format_currency(profit.get('total_investment', 0)), format_currency(profit.get('total_investment', 0))],
        ['Yearly Earning', format_currency(profit.get('yearly_profit', 0)), format_currency(profit.get('bank_yearly_interest', 0))],
        ['Return %', f"{profit.get('roi_percentage', 0):.1f}%", f"{fd_rate}%"],
    ]
    E.append(Paragraph("Franchise vs Bank FD Comparison", styles['SubHead']))
    E.append(Spacer(1, 6))
    E.append(_table(bank_rows, [2.0 * inch, 2.1 * inch, 2.1 * inch], GREEN))
    E.append(Spacer(1, 20))

    # ── 5. FIVE-YEAR PROJECTIONS ──────────────────────────────────
    if projs:
        _section(E, 5, "Five-Year Projections", styles)

        pj_rows = [['Year', 'Revenue', 'Expenses', 'Profit', 'Cumulative', 'Bank Interest', 'Bank Cumul.']]
        for p in projs:
            pj_rows.append([
                f"Yr {p['year']}",
                format_currency(p['revenue']),
                format_currency(p['expenses']),
                format_currency(p['profit']),
                format_currency(p['cumulative_profit']),
                format_currency(p.get('bank_interest', 0)),
                format_currency(p.get('cumulative_bank', 0)),
            ])
        E.append(_table(pj_rows,
                        [0.55 * inch, 1.0 * inch, 1.0 * inch, 1.0 * inch, 1.0 * inch, 0.9 * inch, 0.9 * inch],
                        NAVY_LIGHT))
        E.append(Spacer(1, 20))

    # ── 6. RISK ANALYSIS ──────────────────────────────────────────
    _section(E, 6, "Risk Analysis", styles)

    risk_level = risk.get('risk_level', 'Medium')
    risk_style = {'High': 'RiskHigh', 'Medium': 'RiskMedium', 'Low': 'RiskLow'}.get(
        risk_level, 'Body')
    E.append(Paragraph(
        f"Overall Risk Level: {risk_level}  ({risk.get('risk_score', 0)} / 100)",
        styles[risk_style]))
    E.append(Spacer(1, 10))

    risk_factors = risk.get('risk_factors', [])
    if risk_factors:
        rk_header_color = RED if risk_level == 'High' else (ORANGE if risk_level == 'Medium' else GREEN)
        rk_rows = [['Factor', 'Score', 'Level', 'Detail']]
        for rf in risk_factors:
            rk_rows.append([
                rf['factor'],
                f"{rf['score']}/{rf['max_score']}",
                rf['level'],
                rf['detail'],
            ])
        rk_t = _table(rk_rows, [1.2 * inch, 0.7 * inch, 0.7 * inch, 3.4 * inch], rk_header_color)
        rk_t.setStyle(TableStyle([('ALIGN', (1, 0), (2, -1), 'CENTER')]))
        E.append(rk_t)

    E.append(Spacer(1, 12))
    E.append(Paragraph(
        f"<b>Recommendation:</b>  {risk.get('recommendation', '')}",
        styles['Body']))
    E.append(Spacer(1, 20))

    # ── 7. FRANCHISE RECOMMENDATIONS ──────────────────────────────
    if recs:
        E.append(PageBreak())
        _section(E, 7, "Franchise Recommendations", styles)

        for i, rec in enumerate(recs[:5], 1):
            fd = rec['franchise']
            E.append(Paragraph(
                f"#{i}  {fd['name']}  —  Score: {rec['score']}", styles['RecTitle']))
            E.append(Paragraph(
                f"Setup Cost: {format_currency(fd['setup_cost'])}  |  "
                f"Margin: {fd['profit_margin']}%  |  "
                f"Employees: {fd['employees_required']}",
                styles['Body']))
            if rec.get('reasons'):
                for reason in rec['reasons']:
                    E.append(Paragraph(f"\u2022  {reason}", styles['BulletItem']))
            E.append(Spacer(1, 6))
            E.append(HRFlowable(width="100%", color=HexColor('#E5E7EB'), thickness=0.4))
            E.append(Spacer(1, 4))

    # ── DISCLAIMER ────────────────────────────────────────────────
    E.append(Spacer(1, 30))
    E.append(ColorBar(PAGE_W - 3 * cm, 0.5, BORDER))
    E.append(Spacer(1, 8))
    E.append(Paragraph(
        "Disclaimer: This report is generated using Census 2011 data and estimated models. "
        "Actual results may vary. Please conduct additional due diligence before making "
        "investment decisions.",
        styles['Disclaimer']))

    # Build
    doc.build(E)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    with open(output_path, 'wb') as f:
        f.write(pdf_bytes)

    return output_path, pdf_bytes
