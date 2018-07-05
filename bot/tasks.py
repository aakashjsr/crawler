import time, datetime
from datetime import timezone
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawler.celery import celery_app
from bot.models import Item, Task
from celery.exceptions import SoftTimeLimitExceeded


def process(task, driver, products, find_out_of_stock=False):
    products_length = len(products)
    removed_list = []
    out_of_stock_list = []
    back_in_stock_list = []
    url = "http://www.dropship-clothes.com/"
    item_number = 1

    for product_code in products:
        start = time.time()
        delay = 0
        print("\n\nProcessing Item number : {} / {}.".format(item_number, products_length))
        print("Looking into item {}".format(product_code))
        search_box = None
        while delay < 11:
            try:
                print("sleeping for {} seconds.".format(delay))
                time.sleep(delay)
                driver.get(url)
                search_box = driver.find_element_by_class_name('search_input')
            except:
                delay += 1
                driver.save_screenshot("/tmp/task_{}_{}.png".format(task.id, time.time()))
                print("relocating search box")
            else:
                break
        search_box.click()
        search_box.clear()
        search_box.send_keys(product_code)
        search_box.send_keys(Keys.ENTER)
        items = driver.find_elements_by_class_name('pic')
        if len(items):
            item = items[0]
            try:
                item.click()
            except:
                print("item not visible. {}".format(item))
            else:
                sizes = driver.find_elements_by_class_name('sale_property')
                for size in sizes:
                    try:
                        size.click()
                        out_of_stock_button = driver.find_elements_by_class_name("add_out_of_stock")
                        if len(out_of_stock_button):
                            print("{} - {} is out of stock".format(product_code, size.text))
                            out_of_stock_list.append((product_code, size.text.strip().split(")")[-1]))
                        else:
                            # item is back in stock
                            if find_out_of_stock:
                                back_in_stock_list.append((product_code, size.text.strip().split(")")[-1]))
                    except:
                        # When its a hidden element
                        pass
        else:
            search_element = driver.find_elements_by_class_name('search_tit')
            if len(search_element):
                for element in search_element:
                    if element.text.lower() == "not found":
                        print("item {} not found".format(product_code))
                        removed_list.append(product_code)
        end = time.time()
        print("Took {} seconds to process {}".format(end-start, product_code))
        task.percent = int((100 * item_number) / products_length)
        task.save()
        item_number += 1

    if find_out_of_stock:
        # Mark available items
        for item in back_in_stock_list:
            product = Item.objects.filter(item_code=item[0].lower(), size=item[1])
            if product.exists():
                product = product.first()
                product.status = "available"
                product.save()
    else:
        # Mark Out of Stock items
        for item in out_of_stock_list:
            product = Item.objects.filter(item_code=item[0].lower(), size=item[1])
            if product.exists():
                product = product.first()
                product.status = "out_of_stock"
                product.save()
        # Mark Back in Stock items
        Item.objects.filter(item_code__in=removed_list).update(status="removed")

    task.status = "complete"
    task.ended_at = datetime.datetime.now(timezone.utc)
    task.execution_time = "{0:.2f} mins".format((task.ended_at - task.started_at).total_seconds()/60)
    task.save()


@celery_app.task(task_time_limit=1800, soft_time_limit=1740)
def run(task_id):
    task = Task.objects.get(id=task_id)
    try:
        print("Got Task...")
        task.status = "running"
        task.started_at = datetime.datetime.now(timezone.utc)
        task.save()
    except Exception as e:
        task.exception_message = str(e)
        task.status = "failed"
        task.save()
    try:
        # driver = webdriver.Chrome('/Users/aakashkumardas/Downloads/chromedriver')
        driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'], service_log_path='/tmp/ghostdriver.log')
    except:
        task.exception_message = "Phantom JS unavailable"
        task.status = "failed"
        task.save()
    else:
        data = task.item_codes[1: len(task.item_codes) - 1]
        data = data.split(',')
        data = [i.strip().replace("'", "") for i in data]
        try:
            process(task, driver, data, task.check_in_stock)
        except SoftTimeLimitExceeded:
            task.status = "failed"
            task.exception_message = "Time limit exceeded"
            task.save()
        except Exception as e:
            task.status = "failed"
            task.exception_message = str(e)
            task.save()
            raise
        driver.quit()
    print("Job Complete")
