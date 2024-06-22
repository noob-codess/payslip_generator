from flask import Flask, render_template, request, send_file
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import calendar
import os

app = Flask(__name__)

def calculate_monthly_salary(annual_income):
    monthly_salary = annual_income / 12
    return monthly_salary

def calculate_tax(monthly_salary):
    annual_salary = monthly_salary * 12
    if annual_salary <= 250000:
        tax = 0
    elif annual_salary <= 500000:
        tax = (annual_salary - 250000) * 0.05
    elif annual_salary <= 750000:
        tax = 250000 * 0.05 + (annual_salary - 500000) * 0.1
    elif annual_salary <= 1000000:
        tax = 250000 * 0.05 + 250000 * 0.1 + (annual_salary - 750000) * 0.15
    elif annual_salary <= 1250000:
        tax = 250000 * 0.05 + 250000 * 0.1 + 250000 * 0.15 + (annual_salary - 1000000) * 0.2
    elif annual_salary <= 1500000:
        tax = 250000 * 0.05 + 250000 * 0.1 + 250000 * 0.15 + 250000 * 0.2 + (annual_salary - 1250000) * 0.25
    else:
        tax = 250000 * 0.05 + 250000 * 0.1 + 250000 * 0.15 + 250000 * 0.2 + 250000 * 0.25 + (annual_salary - 1500000) * 0.3
    monthly_tax = tax / 12
    return monthly_tax

def get_next_month(month):
    month_number = list(calendar.month_name).index(month)
    if month_number == 12:
        next_month_number = 1
    else:
        next_month_number = month_number + 1
    return calendar.month_name[next_month_number]

@app.route('/')
def index():
    return render_template('payslip.html')

@app.route('/generate_payslip', methods=['POST'])
def generate_payslip():
    org_name = request.form['org_name']
    gstin = request.form['gstin']
    employee_name = request.form['employee_name']
    employee_id = request.form['employee_id']
    department = request.form['department']
    designation = request.form['designation']
    bank_name = request.form['bank_name']
    bank_account_number = request.form['bank_account_number']
    annual_income = float(request.form['annual_income'])
    month = request.form['month']
    year = int(request.form['year'])
    leaves_taken = int(request.form['leaves_taken'])
    doj_month = request.form['doj_month']
    doj_year = request.form['doj_year']

    monthly_salary = calculate_monthly_salary(annual_income)
    professional_tax = calculate_tax(monthly_salary)
    health_insurance = monthly_salary * 0.02
    net_salary = monthly_salary - professional_tax - health_insurance

    basic = monthly_salary * 0.5
    hra = min(monthly_salary * 0.3, 5000)
    adhoc_allowance = monthly_salary * 0.15
    misc_allowance = monthly_salary * 0.05

    if hra < monthly_salary * 0.3:
        basic += (monthly_salary * 0.3 - hra)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Register DejaVu fonts
    font_path_regular = os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf')
    font_path_bold = os.path.join(os.path.dirname(__file__), 'DejaVuSans-Bold.ttf')
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path_regular))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', font_path_bold))

    # Header
    header = Paragraph(f'<strong>{org_name}</strong>', styles['Title'])
    gstin_paragraph = Paragraph(f'GSTIN: {gstin}', styles['Normal'])
    subtitle = Paragraph(f'Payslip for {month.capitalize()}, {year}', styles['Normal'])
    elements.append(header)
    elements.append(gstin_paragraph)
    #elements.append(Spacer(1, 12))
    elements.append(subtitle)
    elements.append(Spacer(1, 12))

    # Employee Details
    employee_data = [
        ['Employee Name:', employee_name],
        ['Employee ID:', employee_id],
        ['Department:', department],
        ['Designation:', designation],
        ['Bank Name:', bank_name],
        ['Bank Account Number:', bank_account_number],
        ['Date of Joining:', f'{doj_month} {doj_year}'],
        ['Leaves Taken:', str(leaves_taken)],
    ]
    employee_table = Table(employee_data, colWidths=[150, 350])
    employee_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(employee_table)

    # Salary Details
    salary_data = [
        ['Salary Component', 'Amount (₹)'],
        ['Total Salary:', f'{monthly_salary:.2f}'],
        ['Professional Tax:', f'{professional_tax:.2f}'],
        ['Health Insurance:', f'{health_insurance:.2f}'],
        ['Net Salary:', f'{net_salary:.2f}'],
    ]
    salary_table = Table(salary_data, colWidths=[150, 350])
    salary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(salary_table)

    # Earnings
    earnings_data = [
        ['Earnings', 'Amount (₹)'],
        ['Basic Salary:', f'{basic:.2f}'],
        ['House Rent Allowance:', f'{hra:.2f}'],
        ['Adhoc Allowance:', f'{adhoc_allowance:.2f}'],
        ['Miscellaneous Allowance:', f'{misc_allowance:.2f}'],
        ['Gross Earnings:', f'{monthly_salary:.2f}'],
    ]
    earnings_table = Table(earnings_data, colWidths=[150, 350])
    earnings_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(earnings_table)

    # Deductions
    deductions_data = [
        ['Deductions', 'Amount (₹)'],
        ['Professional Tax:', f'{professional_tax:.2f}'],
        ['Health Insurance:', f'{health_insurance:.2f}'],
    ]
    deductions_table = Table(deductions_data, colWidths=[150, 350])
    deductions_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(deductions_table)

    # Footer
    next_month = get_next_month(month.capitalize())
    footer = Paragraph(f'Payslip generated in {next_month}, {year}', styles['Normal'])
    elements.append(Spacer(1, 100))  # Ensure footer is at the bottom of the page
    elements.append(footer)

    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f'payslip_{month.capitalize()}.pdf')

if __name__ == '__main__':
    app.run(debug=True)
