import os 
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the absolute path to the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
STOCK_PATH = os.path.join(DATA_DIR, 'stock.json')
LAPTOP_DATA_DIR = os.path.join(DATA_DIR, 'laptops')

logger.info(f"Loading data from: {STOCK_PATH}")

laptops_main_categories = [ 
 'מחשבים ניידים 2in1',
 'מחשבים ניידים Acer',
 'מחשבים ניידים Apple',
 'מחשבים ניידים Asus',
 'מחשבים ניידים Dell',
 'מחשבים ניידים HP',
 'מחשבים ניידים Lenovo',
 'מחשבים ניידים MSI',
]



def load_data(file_path: str) -> list[dict]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f'Error loading data from {file_path}: {e}')
        raise e

def save_data(data: list[dict], file_path: str):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f'Error saving data to {file_path}: {e}')
        raise e

def save_jsons(data: list[dict], categories: list[str], *id_sets: set):

    map_category = {
        'מחשבים ניידים 2in1': 'two_in_one_laptops',
        'מחשבים ניידים Acer': 'acer_laptops',
        'מחשבים ניידים Apple': 'apple_laptops',
        'מחשבים ניידים Asus': 'asus_laptops',
        'מחשבים ניידים Dell': 'dell_laptops',
        'מחשבים ניידים HP': 'hp_laptops',
        'מחשבים ניידים Lenovo': 'lenovo_laptops',
        'מחשבים ניידים MSI': 'msi_laptops',
    }
    try:
        if not os.path.exists(LAPTOP_DATA_DIR):
            os.makedirs(LAPTOP_DATA_DIR)
            
        # Zip categories with their corresponding ID sets
        for category, ids in zip(categories, id_sets):
            category_data = [item for item in data if item['id'] in ids]
            filename = map_category[category]
            category_file_path = os.path.join(LAPTOP_DATA_DIR, f'{filename}.json')
            
            logger.info(f'Saving {len(category_data)} items to {category_file_path}')
            with open(category_file_path, 'w', encoding='utf-8') as f:
                json.dump(category_data, f, ensure_ascii=False, indent=4)
                
    except Exception as e:
        logger.error(f'Error saving category data: {e}')
        raise e
    
def handle_laptops(data: list[dict]):
    """
    Handle laptops data.
    """
    laptops_ids = set()  # Initialize the set
    
    # First, populate laptops_ids
    for item in data:
        if item['stock_status'] == 'outofstock':
            continue
        for category in item['categories']:
            if category['name'] == 'מחשבים ניידים':  # Main laptop category
                laptops_ids.add(item['id'])
                break

    # Initialize category sets
    two_in_one_laptops_ids = set()
    acer_laptops_ids = set()
    apple_laptops_ids = set()
    asus_laptops_ids = set()
    dell_laptops_ids = set()
    hp_laptops_ids = set()
    lenovo_laptops_ids = set()
    msi_laptops_ids = set()

    # Now process categories for laptops we found
    for item in data:
        if item['stock_status'] == 'outofstock':
            continue
        if item['id'] in laptops_ids:
            for category in item['categories']:
                if category['name'] == 'מחשבים ניידים 2in1':
                    two_in_one_laptops_ids.add(item['id'])
                elif category['name'] == 'מחשבים ניידים Acer':
                    acer_laptops_ids.add(item['id'])
                elif category['name'] == 'מחשבים ניידים Apple':
                    apple_laptops_ids.add(item['id'])
                elif category['name'] == 'מחשבים ניידים Asus':
                    asus_laptops_ids.add(item['id'])
                elif category['name'] == 'מחשבים ניידים Dell':
                    dell_laptops_ids.add(item['id'])
                elif category['name'] == 'מחשבים ניידים HP':
                    hp_laptops_ids.add(item['id'])
                elif category['name'] == 'מחשבים ניידים Lenovo':
                    lenovo_laptops_ids.add(item['id'])
                elif category['name'] == 'מחשבים ניידים MSI':
                    msi_laptops_ids.add(item['id'])

    all_categorized = set().union(
        two_in_one_laptops_ids,
        acer_laptops_ids,
        apple_laptops_ids,
        asus_laptops_ids,
        dell_laptops_ids,
        hp_laptops_ids,
        lenovo_laptops_ids,
        msi_laptops_ids
    )

    uncategorized = laptops_ids - all_categorized

    # Print statistics
    logger.info(f'Number of in-stock laptops ids: {len(laptops_ids)}')
    logger.info(f'Number of two in one laptops ids: {len(two_in_one_laptops_ids)}')
    logger.info(f'Number of acer laptops ids: {len(acer_laptops_ids)}')
    logger.info(f'Number of apple laptops ids: {len(apple_laptops_ids)}')
    logger.info(f'Number of asus laptops ids: {len(asus_laptops_ids)}')
    logger.info(f'Number of dell laptops ids: {len(dell_laptops_ids)}')
    logger.info(f'Number of hp laptops ids: {len(hp_laptops_ids)}')
    logger.info(f'Number of lenovo laptops ids: {len(lenovo_laptops_ids)}')
    logger.info(f'Number of msi laptops ids: {len(msi_laptops_ids)}')
    logger.info(f'Number of uncategorized laptops ids: {len(uncategorized)}')

    if len(uncategorized) > 0:
        logger.info('Filling missing categories for laptops...')
        fill_missing_categories_laptops(data, uncategorized)


    logger.info('Saving laptops data...')
    save_data(data, STOCK_PATH)

    # Save each category to json files
    save_jsons(
        data, 
        laptops_main_categories,
        two_in_one_laptops_ids,
        acer_laptops_ids,
        apple_laptops_ids,
        asus_laptops_ids,
        dell_laptops_ids,
        hp_laptops_ids,
        lenovo_laptops_ids,
        msi_laptops_ids
    )

def fill_missing_categories_laptops(data: list[dict], uncategorized: set[str]):
    n_filled = 0
    brand_categories = {
        "Lenovo": {
                "id": 7136,
                "name": "מחשבים ניידים Lenovo",
                "slug": "%d7%9e%d7%97%d7%a9%d7%91%d7%99%d7%9d-%d7%a0%d7%99%d7%99%d7%93%d7%99%d7%9d-lenovo"
        },
        "Acer": {
                "id": 11002,
                "name": "מחשבים ניידים Acer",
                "slug": "%d7%9e%d7%97%d7%a9%d7%91%d7%99%d7%9d-%d7%a0%d7%99%d7%99%d7%93%d7%99%d7%9d-acer"
        },
        "Dell": {
            "id": 7137,
            "name": "מחשבים ניידים Dell",
            "slug": "%d7%9e%d7%97%d7%a9%d7%91%d7%99%d7%9d-%d7%a0%d7%99%d7%99%d7%93%d7%99%d7%9d-dell"
        },
        "HP": {
                "id": 7138,
                "name": "מחשבים ניידים HP",
                "slug": "%d7%9e%d7%97%d7%a9%d7%91%d7%99%d7%9d-%d7%a0%d7%99%d7%99%d7%93%d7%99%d7%9d-hp"
        },
        "Asus": {
                "id": 12955,
                "name": "מחשבים ניידים Asus",
                "slug": "%d7%9e%d7%97%d7%a9%d7%91%d7%99%d7%9d-%d7%a0%d7%99%d7%99%d7%93%d7%99%d7%9d-asus"
        },
        "Apple": {
                "id": 716,
                "name": "מחשבים ניידים Apple",
                "slug": "%d7%9e%d7%97%d7%a9%d7%91%d7%99%d7%9d-%d7%a0%d7%99%d7%99%d7%93%d7%99%d7%9d-apple"
        },
        "MSI": {
                "id": 12743,
                "name": "מחשבים ניידים MSI",
                "slug": "%d7%9e%d7%97%d7%a9%d7%91%d7%99%d7%9d-%d7%a0%d7%99%d7%99%d7%93%d7%99%d7%9d-msi"
        }
    }

    for item in data:
        if item['id'] in uncategorized:
            if 'Lenovo' or 'lenovo' in item['name'].lower():
                item['categories'].append(brand_categories['Lenovo'])
            elif 'Acer' or 'acer' in item['name'].lower():
                item['categories'].append(brand_categories['Acer'])
            elif 'Dell' or 'dell' in item['name'].lower():
                item['categories'].append(brand_categories['Dell'])
            elif 'HP' or 'hp' in item['name'].lower():
                item['categories'].append(brand_categories['HP'])
            elif 'Asus' or 'asus' in item['name'].lower():
                item['categories'].append(brand_categories['Asus'])
            elif 'Apple' or 'apple' in item['name'].lower():
                item['categories'].append(brand_categories['Apple'])
            elif 'MSI' or 'msi' in item['name'].lower():
                item['categories'].append(brand_categories['MSI'])

def main():
    logger.info('Starting data preparation...')
    try:
        data = load_data(STOCK_PATH)
        handle_laptops(data)
        logger.info('Data preparation completed successfully.')
    except Exception as e:
        logger.error(f'Error during data preparation: {e}')
        raise e

if __name__ == '__main__':
    main()
