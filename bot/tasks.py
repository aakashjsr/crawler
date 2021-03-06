import time, datetime, json
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
    url = "https://www.dropship-clothes.com/"
    item_number = 1

    completed_items = []
    import pdb

    for product_code in products:
        pdb.set_trace()
        print(product_code)
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
                if not search_box:
                    delay += 1
                else:
                    break
        search_box.click()
        search_box.clear()
        search_box.send_keys(product_code)
        search_box.send_keys(Keys.ENTER)
        items = driver.find_elements_by_class_name('pic_box')
        if len(items):
            search_items = items[0].find_elements_by_class_name("pic")
            item = search_items[0]
            try:
                item.click()
            except:
                driver.save_screenshot("/tmp/task_{}_item_{}.png".format(task.id, product_code))
                print("item not visible. {}".format(item))
            else:
                sizes = driver.find_elements_by_class_name('sale_property')
                for size in sizes:
                    try:
                        size.click()
                        out_of_stock_button = driver.find_elements_by_class_name("add_out_of_stock")
                        if len(out_of_stock_button):
                            print("{} - {} is out of stock".format(product_code, size.text))
                            # (code, size, quantity)
                            out_of_stock_list.append((product_code, size.text.strip().split(")")[-1], 0))
                        else:
                            # item is back in stock
                            # (code, size, quantity)
                            size_box = driver.find_element_by_id("goods_stock_num")
                            size = int(size_box.text)
                            print((product_code, size.text.strip().split(")")[-1], size))
                            if find_out_of_stock:
                                back_in_stock_list.append((product_code, size.text.strip().split(")")[-1], size))
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
        completed_items.append(product_code)
        print("Took {} seconds to process {}".format(end-start, product_code))
        task.percent = int((100 * item_number) / products_length)
        task.completed_items = json.dumps(completed_items)
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
        driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any --load-images=no'], service_log_path='/tmp/ghostdriver.log')
    except:
        task.exception_message = "Phantom JS unavailable"
        task.status = "failed"
        task.save()
    else:
        data = task.item_codes[1: len(task.item_codes) - 1]
        data = data.split(',')
        data = [i.strip().replace("'", "") for i in data]
        completed_items = json.loads(task.completed_items)
        if len(completed_items):
            data = list(set(data).difference(set(completed_items)))
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
