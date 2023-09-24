def get_html_report(report_details):
    html_string = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            <h2 style='text-align: center'>Sales Report - {report_details.get('current_date')}</h2>
            <table cellpadding="10" cellspacing="0" border="1" style="border-collapse: collapse; font-family: Arial, Helvetica; margin: 0 auto;">
                <tr>
                    <td style="text-align: center; background-color: #f2f2f2;"><strong>Yesterday's Orders</strong></td>
                    <td style="text-align: center;">{report_details.get('orders_yesterday')}</td>
                </tr>
                <tr>
                    <td style="text-align: center; background-color: #f2f2f2;"><strong>Yesterday's Revenue</strong></td>
                    <td style="text-align: center;">Rs.{report_details.get('revenue_yesterday')}</td>
                </tr>
                <tr>
                    <td style="text-align: center; background-color: #f2f2f2;"><strong>This Month's Orders</strong></td>
                    <td style="text-align: center;">{report_details.get('orders_this_month')}</td>
                </tr>
                <tr>
                    <td style="text-align: center; background-color: #f2f2f2;"><strong>This Month's Revenue</strong></td>
                    <td style="text-align: center;">Rs.{report_details.get('revenue_this_month')}</td>
                </tr>
                <tr>
                    <td style="text-align: center; background-color: #f2f2f2;"><strong>Total Customers</strong></td>
                    <td style="text-align: center;">{report_details.get('total_customers')}</td>
                </tr>
            </table>
        </body>
        </html>
    '''
    return html_string
