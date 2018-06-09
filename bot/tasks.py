import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawler.celery import celery_app
from bot.models import Item
from celery import signals


def process(driver, products, find_out_of_stock=False):
    removed_list = []
    out_of_stock_list = []
    back_in_stock_list = []
    url = "http://www.dropship-clothes.com/"

    for product_code in products:
        time.sleep(0.5)
        driver.get(url)
        print("Looking into item {}".format(product_code))
        s_time = time.time()
        e_time = time.time()
        search_box = None
        while e_time - s_time < 10:
            try:
                search_box = driver.find_element_by_class_name('search_input')
            except:
                driver.save_screenshot("/tmp/{}.png".format(time.time()))
                print("Refinding search box")
            else:
                break
        start = time.time()
        search_box.click()
        search_box.clear()
        search_box.send_keys(product_code)
        search_box.send_keys(Keys.ENTER)
        time.sleep(0.2)
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
                    else:
                        # item is back in stock
                        if find_out_of_stock:
                            back_in_stock_list.append((product_code, size.text.split(")")[1]))
                except:
                    # When its a hidden element
                    pass
        else:
            print("item {} not found".format(product_code))
            removed_list.append(product_code)
        end = time.time()
        print("Took {} seconds to process {}".format(end-start, product_code))

    if find_out_of_stock:
        # Mark available items
        for item in out_of_stock_list:
            product = Item.objects.filter(item_code=item[0].lower(), size=item[1].lower())
            if product.exists():
                product = product.first()
                product.status = "available"
                product.save()
    else:
        # Mark Out of Stock items
        for item in out_of_stock_list:
            product = Item.objects.filter(item_code=item[0].lower(), size=item[1].lower())
            if product.exists():
                product = product.first()
                product.status = "out_of_stock"
                product.save()
        # Mark Back in Stock items
        Item.objects.filter(item_code__in=removed_list).update(status="removed")


@celery_app.task(bind=True, max_retries=5)
def run(self, products, check_back_in_stock, *args, **kwargs):
    try:
        print("Got Task...")
        # driver = webdriver.Chrome('/Users/aakashkumardas/Downloads/chromedriver')
        driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'], service_log_path='/tmp/ghostdriver.log')
        process(driver, products, check_back_in_stock)
        driver.quit()
        print("Job Complete")
    except Exception as exc:
        raise Exception(str(exc))
        # self.retry(exc=exc, countdown=2)
