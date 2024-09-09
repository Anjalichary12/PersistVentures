import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from num2words import num2words

# Function to convert numbers to words
def num_to_words(num):
    return num2words(num, lang='en').capitalize()

# Function to generate an invoice
def generate_invoice(data):
    # Load Jinja2 template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('invoice_template.html')

    # Calculate item details
    for item in data['items']:
        item['net_amount'] = item['unit_price'] * item['quantity'] - item['discount']
        item['tax'] = item['net_amount'] * (data['tax_rate'] / 100)
        item['total'] = item['net_amount'] + item['tax']

    # Calculate totals
    total_amount = sum(item['total'] for item in data['items'])
    data['total_amount'] = total_amount
    data['amount_in_words'] = num_to_words(total_amount)

    # Render the template
    html_out = template.render(data)

    # Save to PDF using WeasyPrint
    HTML(string=html_out).write_pdf('invoice.pdf')

# Example data for generating invoice
data = {
    'logo': "C:\Assignments_INTERNSHALA\Persist ventures\logo.png",  # Replace with your logo file path
    'seller_name': 'Varasiddhi Silk Exports',
    'seller_address': '7/5, 3rd Cross, Lalbagh Road, Bengaluru, Karnataka, 560027',
    'seller_pan': 'AACFV3325K',
    'seller_gst': '29AACFV3325K1ZY',
    'invoice_no': 'IN-761',
    'invoice_date': '28.10.2019',
    'billing_name': 'Eurofins IT Solutions India Pvt Ltd.',
    'billing_address': '1st Floor, Maruti Platinum, Lakshmipuram Pura, AECS Layout, Bengaluru',
    'billing_state_code': '29',
    'shipping_name': 'Madhu B',
    'shipping_address': 'Eurofins IT Solutions India Pvt Ltd., 1st Floor, Maruti Platinum, Lakshmipuram Pura, Bengaluru',
    'shipping_state_code': '29',
    'items': [
        {
            'description': "Men's Formal Shirt (Navy Blue, 40)",
            'quantity': 1,
            'unit_price': 499.00,
            'discount': 50.00,
        },
        {
            'description': "Men's Formal Shirt (Navy Blue, 41)",
            'quantity': 1,
            'unit_price': 599.00,
            'discount': 50.00,
        }
    ],
    'tax_rate': 18,  # 18% tax
    'signature': "C:\Assignments_INTERNSHALA\Persist ventures\Signature.png"  # Replace with your signature file path
}

# Generate the invoice
generate_invoice(data)

# Output: 'invoice.pdf' will be generated in the current directory
