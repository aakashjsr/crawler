from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawler.celery import celery_app
from bot.models import Item


def process(driver, products):
    removed_list = []
    out_of_stock_list = []
    url = "http://www.dropship-clothes.com/"
    driver.get(url)
    for product_code in products:
        print("Looking into item {}".format(product_code))
        search_box = driver.find_element_by_class_name('search_input')
        search_box.click()
        search_box.clear()
        search_box.send_keys(product_code)
        search_box.send_keys(Keys.ENTER)

        items = driver.find_elements_by_class_name('pic')
        if len(items):
            item = items[0]
            item.click()
            sizes = driver.find_elements_by_class_name('sale_property')
            for size in sizes:
                try:
                    size.click()
                    out_of_stock_button = driver.find_elements_by_class_name("add_out_of_stock")
                    if len(out_of_stock_button):
                        print("{} - {} is out of stock".format(product_code, size.text))
                        out_of_stock_list.append((product_code, size.text.split(")")[1]))
                except:
                    # When its a hidden element
                    pass
        else:
            print("item {} not found".format(product_code))
            removed_list.append(product_code)
    Item.objects.filter(item_code__in=removed_list).update(status="removed")
    for item in out_of_stock_list:
        product = Item.objects.filter(item_code=item[0].lower(), size=item[1].lower())
        if product.exists():
            product = product.first()
            product.status = "out_of_stock"
            product.save()
    print(out_of_stock_list)
    print(removed_list)


@celery_app.task
def run(products):
    print("Got Task...")
    # driver = webdriver.Chrome('/Users/aakashkumardas/Downloads/chromedriver')
    driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'], service_log_path='/tmp/ghostdriver.log')
    try:
        process(driver, products)
    except Exception as e:
        print(e)
    driver.quit()
    print("Job Complete")
