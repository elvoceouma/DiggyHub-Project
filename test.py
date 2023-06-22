from wkhtmltopdf import WKHtmlToPdf

wkhtmltopdf = WKHtmlToPdf(
    url='http://www.google.com',
    output_file='./example.pdf',
)
wkhtmltopdf.render()
