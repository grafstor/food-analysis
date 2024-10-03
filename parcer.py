import requests
from lxml import html
from bs4 import BeautifulSoup
import json

def parce_cats(url):
    cats = []

    response = requests.get(url)
    tree = html.fromstring(response.content)
    
    cat_table_xpath = "/html/body/div[1]/div/main/div/div/div/div[3]/div[2]/div"
    cat_table_item_xpath = cat_table_xpath + "/div"
    
    cat_table_item_name_xpath = "./a/div/div"  # text
    cat_table_item_href_xpath = "./a"  # href

    cat_elements = tree.xpath(cat_table_item_xpath)

    for cat_element in cat_elements:
        cat_name_elements = cat_element.xpath(cat_table_item_name_xpath)
        cat_name = cat_name_elements[0].text.strip()
        
        cat_href_elements = cat_element.xpath(cat_table_item_href_xpath)
        cat_href = cat_href_elements[0].get('href')

        cats.append([cat_name, cat_href])

    return cats

def parce_subcats(cats):
    subcats = []
    
    subcat_table_xpath = "/html/body/div[1]/div/main/div/div/div/div[3]/div/div/div"
    subcat_table_item_xpath = subcat_table_xpath + "/div"
    
    subcat_table_item_name_xpath = "./a/span"  # text
    subcat_table_item_href_xpath = "./a"  # href
    
    for cat_name, cat_href in cats:
        full_cat_url = "https://www.perekrestok.ru" + cat_href
    
        response = requests.get(full_cat_url)
        tree = html.fromstring(response.content)
    
        subcat_elements = tree.xpath(subcat_table_item_xpath)
        
        for subcat_element in subcat_elements:
            subcat_name_elements = subcat_element.xpath(subcat_table_item_name_xpath)
            subcat_name = subcat_name_elements[0].text.strip()

            
            subcat_href_elements = subcat_element.xpath(subcat_table_item_href_xpath)
            subcat_href = subcat_href_elements[0].get('href')
            
            subcats.append((subcat_name, cat_name, subcat_href))
    
    return subcats

def get_products(html, url, subcat, cat):
    products = []
    
    soup = BeautifulSoup(html, 'html.parser')
    products_divs = soup.find_all('div', class_='product-card-wrapper')
    
    for product in products_divs:
        product_name = product.find('span', class_='product-card__link-text').text.strip()
        product_href = product.find('a', class_='product-card__link')['href']
        
        product_rating = product.find('div', class_='rating-value')
        
        if product_rating:
            product_rating = product_rating.text.strip()
        else:
            product_rating = "Нет рейтинга"
        
        try:
            product_size = product.find('div', class_='product-card__size').text.strip()
        except:
            product_size = ""

        product_price = product.find('div', class_='product-card__pricing').text.strip()
        
        product_discount = product.find('div', class_='product-card__badges')
        if product_discount.find('span'):
            product_discount_value = product_discount.find('span').text.strip()
            product_new_price = product_discount.find_next('div', class_='price-new').text.strip()
            try:
                product_old_price = product_discount.find_next('div', class_='price-old').text.strip()
            except:
                product_old_price = ""

        else:
            product_discount_value = "Нет скидки"
            product_new_price = product_discount.find_next('div', class_='price-new').text.strip()
            product_old_price = ""

        products.append([
            product_name,
            product_href,
            cat,
            subcat,
            product_rating,
            product_size,
            product_price.replace("\xa0", " "),
            product_new_price.replace("Цена","").replace("\xa0", " "),
            product_old_price.replace("Старая цена","").replace("\xa0", " "),
            product_discount_value,
            url,
        ])
        
    return products

def save_listing_products_to_csv(filename, listing_products):
    fieldnames = [
        'name', 'href', 'rating', 'size', 'price', 'new_price', 'old_price', 'discount', 'subcat_href'
    ]

    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)        
        writer.writerows(listing_products)
    
    print("Список успешно сохранен в файл", filename)

def parce_listing_products(subcats):
    listing_products = []
    
    for subcat, cat, url in subcats:
        html = requests.get("https://www.perekrestok.ru" + url).content
        products = get_products(html, url, subcat, cat)
        listing_products.extend(products)

    return listing_products

def parce_product_page(html, href):
    soup = BeautifulSoup(html, 'html.parser')
    script_tags = soup.find_all('script')
    
    initial_state_dict = None
    for script_tag in script_tags:
        script_content = script_tag.string
        if script_content and "__INITIAL_STATE__" in script_content:
            initial_state_str = script_content.split('__INITIAL_STATE__ = ')[1]
            initial_state_dict = json.loads(initial_state_str)

    dict_href = href.split('/')[4:][0]

    prod = initial_state_dict["catalog"]["productData"][dict_href]

    food_title = prod["title"]
    if prod["priceTag"]:
        price = prod["priceTag"]['price']
        if prod["priceTag"]['labels']:
            disc = prod["priceTag"]['labels'][0]['text']
        else:
            disc = ""
    else:
        price = ""
        disc = ""

    rating = prod["rating"]

    kalories = ""
    proteins = ""
    fats = ""
    carbohydrates = ""
    composition = ""
    manufacturer = ""
    brand = ""
    country = ""
    shelf_life = ""
    max_storage_temperature = ""
    min_storage_temperature = ""

    for k in prod["features"]:
        if k['title'] == "Пищевая ценность на 100г":
            for i in k["items"]:
                title = i['title'].lower().replace(' ', '_')
                if title == "ккал":
                    kalories = i['displayValues'][0]
                elif title == "белки":
                    proteins = i['displayValues'][0]
                elif title == "жиры":
                    fats = i['displayValues'][0]
                elif title == "углеводы":
                    carbohydrates = i['displayValues'][0]
                
        elif k['title'] == "Состав":
            for i in k["items"]:
                composition = i['displayValues'][0]
                
        elif k['title'] == "Информация":
            for i in k["items"]:
                title = i['title'].lower().replace(' ', '_')
                if title == "производитель":
                    manufacturer = i['displayValues'][0]
                elif title == "бренд":
                    brand = i['displayValues'][0]
                elif title == "страна":
                    country = i['displayValues'][0]
                
        elif k['title'] == "Условия хранения":
            for i in k["items"]:
                title = i['title'].lower().replace(' ', '_')
                if title == "срок_хранения_макс.":
                    shelf_life = i['displayValues'][0]
                elif title == "температура_хранения_макс.":
                    max_storage_temperature = i['displayValues'][0]
                elif title == "температура_хранения_мин.":
                    min_storage_temperature = i['displayValues'][0]

    return [
        href,

        food_title,
        price,
        disc,
        rating,

        kalories,
        proteins,
        fats,
        carbohydrates,

        composition,

        manufacturer,
        brand,
        country,

        shelf_life,
        max_storage_temperature,
        min_storage_temperature,
    ]


def save_products_to_csv(filename, food_extended):
    fieldnames = [
        'product_href',
        'title',
        'price',
        'discount',
        'rating',
        'kalories',
        'proteins',
        'fats',
        'carbohydrates',
        'composition',
        'manufacturer',
        'brand',
        'country',
        'shelf_life',
        'max_storage_temperature',
        'min_storage_temperature'
    ]

    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        writer.writerows(food_extended)
    
    print("Список успешно сохранен в файл", filename)

def parce_products(listing_products):
    products = []
    
    for listing_product in listing_products:
        url = listing_product[1]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        html = requests.get("https://www.perekrestok.ru" + url, headers=headers).content
        product = parce_product_page(html, url)
        products.append(product)
        
    return products
