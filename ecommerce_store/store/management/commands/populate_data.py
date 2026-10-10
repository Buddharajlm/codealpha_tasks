from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Seeds initial demo categories, products, and admin superuser for college presentation'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating database with demo data...")

        # 1. Create Superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS("Created admin superuser: username 'admin', password 'admin123'"))
        else:
            self.stdout.write("Superuser 'admin' already exists.")

        # 2. Categories
        categories_data = [
            {'name': 'Electronics', 'icon': '💻', 'description': 'Computers, accessories, and modern gadgets'},
            {'name': 'Audio & Headphones', 'icon': '🎧', 'description': 'High fidelity audio equipment and noise-cancelling headphones'},
            {'name': 'Wearables', 'icon': '⌚', 'description': 'Smartwatches, fitness bands, and wearable trackers'},
            {'name': 'Home & Office', 'icon': '☕', 'description': 'Workspace productivity and home comfort items'},
            {'name': 'Books & Learning', 'icon': '📚', 'description': 'Programming, engineering, and career growth books'},
        ]

        categories = {}
        for cdata in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cdata['name'],
                defaults={'icon': cdata['icon'], 'description': cdata['description']}
            )
            categories[cdata['name']] = cat

        self.stdout.write(self.style.SUCCESS(f"Loaded {len(categories)} categories."))

        # 3. Products
        products_data = [
            {
                'name': 'Sony WH-1000XM5 Wireless Headphones',
                'category': categories['Audio & Headphones'],
                'price': Decimal('299.99'),
                'original_price': Decimal('399.99'),
                'stock': 25,
                'rating': Decimal('4.8'),
                'reviews_count': 142,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80',
                'description': 'Industry-leading noise canceling with two processors and 8 microphones. Up to 30-hour battery life and ultra-comfortable lightweight design.'
            },
            {
                'name': 'Apple MacBook Pro M3 (14-inch)',
                'category': categories['Electronics'],
                'price': Decimal('1499.00'),
                'original_price': Decimal('1699.00'),
                'stock': 12,
                'rating': Decimal('4.9'),
                'reviews_count': 98,
                'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&auto=format&fit=crop&q=80',
                'description': 'Stunning Liquid Retina XDR display, pro-level performance with Apple M3 chip, unified memory, and all-day 18-hour battery longevity.'
            },
            {
                'name': 'Logitech MX Master 3S Wireless Mouse',
                'category': categories['Electronics'],
                'price': Decimal('99.99'),
                'original_price': Decimal('119.99'),
                'stock': 40,
                'rating': Decimal('4.7'),
                'reviews_count': 230,
                'image_url': 'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&auto=format&fit=crop&q=80',
                'description': 'Quiet Clicks ergonomic wireless mouse with 8K DPI track-on-glass sensor and MagSpeed electromagnetic scrolling for supreme precision.'
            },
            {
                'name': 'Samsung Galaxy Watch 6 Classic',
                'category': categories['Wearables'],
                'price': Decimal('249.99'),
                'original_price': Decimal('299.99'),
                'stock': 18,
                'rating': Decimal('4.6'),
                'reviews_count': 64,
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80',
                'description': 'Iconic rotating bezel with sophisticated stainless steel casing, advanced sleep coaching, body composition analysis, and heart fitness tracking.'
            },
            {
                'name': 'Keychron K2 Wireless Mechanical Keyboard',
                'category': categories['Electronics'],
                'price': Decimal('79.99'),
                'original_price': Decimal('99.99'),
                'stock': 30,
                'rating': Decimal('4.8'),
                'reviews_count': 88,
                'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=80',
                'description': '75% compact layout mechanical keyboard with Gateron G Pro Brown switches, Bluetooth 5.1 multi-device pairing, and warm RGB backlighting.'
            },
            {
                'name': 'Minimalist Ergonomic LED Desk Lamp',
                'category': categories['Home & Office'],
                'price': Decimal('45.00'),
                'original_price': Decimal('60.00'),
                'stock': 22,
                'rating': Decimal('4.5'),
                'reviews_count': 41,
                'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&auto=format&fit=crop&q=80',
                'description': 'Architect style swivel-arm LED desk lamp with touch dimmer, 5 color temperature modes, and eye-care anti-glare diffuser for late night study sessions.'
            },
            {
                'name': 'Clean Code: A Handbook of Agile Software Craftsmanship',
                'category': categories['Books & Learning'],
                'price': Decimal('34.50'),
                'original_price': Decimal('45.00'),
                'stock': 35,
                'rating': Decimal('4.9'),
                'reviews_count': 320,
                'image_url': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&auto=format&fit=crop&q=80',
                'description': 'The definitive guide by Robert C. Martin on writing readable, testable, maintainable code. Essential reading for every software engineer.'
            },
            {
                'name': 'Anker 737 Power Bank (24,000mAh, 140W)',
                'category': categories['Electronics'],
                'price': Decimal('119.99'),
                'original_price': Decimal('149.99'),
                'stock': 15,
                'rating': Decimal('4.8'),
                'reviews_count': 112,
                'image_url': 'https://images.unsplash.com/photo-1609592424075-8ea5a8e0307f?w=800&auto=format&fit=crop&q=80',
                'description': 'Ultra-powerful two-way fast charging with smart digital display showing output power, remaining battery percentage, and full recharge time.'
            }
        ]

        created_count = 0
        for pdata in products_data:
            prod, created = Product.objects.get_or_create(
                name=pdata['name'],
                defaults=pdata
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {created_count} new products into database!"))
