import pdfkit
path_wkhtmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
pdfkit.from_url("https://nfe.prefeitura.sp.gov.br/contribuinte/notaprint.aspx?ccm=51858827&nf=3028&cod=4VY4S7FX", "out.pdf", configuration=config)