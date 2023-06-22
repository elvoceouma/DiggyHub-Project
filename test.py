import wkhtmltopdf
from wkhtmltopdf.main import WKHtmlToPdf

wkhtmltopdf = wkhtmltopdf(
    url='http://www.google.com',
    output_file='./example.pdf',
)
wkhtmltopdf.render()
