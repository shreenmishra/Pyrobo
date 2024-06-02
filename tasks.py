from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive
import time

@task
def minimal_task():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    message = "Hello"
    message = message + " World!"

@task
def order_robots_from_RobotSpareBin():
    browser.configure(
        slowmo=100,
    )
    orders = get_orders()
    print(orders)
    open_robot_order_website()
    for i in orders:
        fill_form(i)
    zip_pdf()

def open_robot_order_website():
    # TODO: Implement your function here
    browser.goto('https://robotsparebinindustries.com/#/robot-order')
    page = browser.page()

def get_orders():
    # To download the csv file and load the table
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", target_file='orders.csv', overwrite=True)
    excel = Tables()
    table = excel.read_table_from_csv('orders.csv', header=True)
    return table

def fill_form(robo):
    page = browser.page()
    page.click('text=OK')
    page.select_option('#head',index=int(robo['Head']))
    page.set_checked("//input[@name='body' and @value='"+str(robo['Body'])+"']",checked=True)
    page.fill("//input[@placeholder='Enter the part number for the legs']", robo['Legs'])
    page.fill('#address', robo['Address'])
    page.click('#order')
    export_pdf(robo['Order number'])    
    page.click('text=Order another robot')

def export_pdf(name):
    page = browser.page()
    element = page.locator('#receipt').inner_html()
    page.wait_for_load_state()
    time.sleep(2)
    page.locator('#robot-preview-image').screenshot(path="output/screenshot/"+str(name)+".png")
    pdf = PDF()
    pdf.html_to_pdf(element, "output/receipt/"+str(name)+".pdf")
    pdf.add_files_to_pdf(
        files=["output/screenshot/"+str(name)+".png"],
        target_document="output/receipt/"+str(name)+".pdf",
        append=True)

def zip_pdf():
    arc = Archive()
    arc.archive_folder_with_zip('output/receipt','output/receipt.zip')


    





    


    
