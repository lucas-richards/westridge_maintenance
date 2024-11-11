import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()

from django.utils import timezone
from workorder.models import ProdItemStd


def seed_prod_items(data):
    for item in data:
        obj, created = ProdItemStd.objects.update_or_create(
            sku=item.get('sku'),
            defaults={
            'description': item.get('description'),
            'pph': item.get('pph'),
            'people_inline': item.get('people_inline'),
            'setup_time': item.get('setup_time'),
            'setup_people': item.get('setup_people'),
            }
        )
        print(f"Product Item {obj.sku} created/updated.")

if __name__ == "__main__":
    data = [
        {
            'sku': 'HRFBBLCHC4',
            'description': 'Bleach Bottles',
            'pph': 261,
            'people_inline': 5,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDD11335',
            'description': '8.5 Love Honey Enjoy',
            'pph': 152,
            'people_inline': 5,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDD11358',
            'description': '8.5 VALM 8.5 Silicone',
            'pph': 190,
            'people_inline': 4,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDD11366',
            'description': '8 Health Vibes Silicone',
            'pph': 218,
            'people_inline': 4,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDD11398',
            'description': '4.4 Moist Anal',
            'pph': 273,
            'people_inline': 4,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDD114G1',
            'description': '8.5 Glide AMAZON',
            'pph': 190,
            'people_inline': 4,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDD11605',
            'description': '16 Health Vibes WB USA',
            'pph': 130,
            'people_inline': 5,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDD11C01',
            'description': '4 Spencers OONA Free',
            'pph': 216,
            'people_inline': 4,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDD11C04',
            'description': '8.5 Spencers Hott Love Ecstasy',
            'pph': 190,
            'people_inline': 4,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDD11C05',
            'description': '4.4 Spencers Toy Lube',
            'pph': 220,
            'people_inline': 4,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDD11C06',
            'description': '1oz SPENCERS',
            'pph': 392,
            'people_inline': 3,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDD11E00',
            'description': '4 Autoblow Cleaner',
            'pph': 287,
            'people_inline': 3,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDD11E01',
            'description': '8 Fap Lube',
            'pph': 217,
            'people_inline': 4,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDD11E02',
            'description': '2 Fap Lube',
            'pph': 216,
            'people_inline': 4,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDD11E03',
            'description': '8 Autoblow Cleaner',
            'pph': 287,
            'people_inline': 3,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDD11F01',
            'description': '4.4 Blissfun WB',
            'pph': 217,
            'people_inline': 4,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDDGLD08C2',
            'description': '8.5 Glide',
            'pph': 289,
            'people_inline': 3,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDDGTB04C2',
            'description': '4.4 Sex Grease - WB',
            'pph': 321,
            'people_inline': 3,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDDGTB08C2',
            'description': '8.5 Sex Grease -WB',
            'pph': 286,
            'people_inline': 3,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDDHAB04C2',
            'description': '4 Hero H20',
            'pph': 304,
            'people_inline': 4,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDDHAB04C4',
            'description': '4 Hero H20 - Spencers',
            'pph': 236,
            'people_inline': 5,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDDMLL01C3',
            'description': '1 Millennium',
            'pph': 297,
            'people_inline': 4,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDDMLL02C3',
            'description': '2.2 Millennium',
            'pph': 324,
            'people_inline': 3,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDDPLS01C3',
            'description': '1 Pleasure',
            'pph': 396,
            'people_inline': 3,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDDPLS04C2',
            'description': '4.4 Pleasure',
            'pph': 326,
            'people_inline': 3,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDDPLS08C2',
            'description': '8.5 Pleasure',
            'pph': 253,
            'people_inline': 3,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDDPLS17C1',
            'description': '17 Pleasure',
            'pph': 194,
            'people_inline': 4,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDDSNS01C3',
            'description': '1 Sensation',
            'pph': 297,
            'people_inline': 4,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDDSNS02C3',
            'description': '2.2 Sensation',
            'pph': 327,
            'people_inline': 3,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDDSNS04C2',
            'description': '4.4 Sensation',
            'pph': 316,
            'people_inline': 3,
            'setup_time': 2,
            'setup_people': 2
        },
        {
            'sku': 'IDDSNS08C2',
            'description': '8.5 Sensation',
            'pph': 290,
            'people_inline': 3,
            'setup_time': 2,
            'setup_people': 2
        }
    ]


    seed_prod_items(data)
    print("Seeding completed.")