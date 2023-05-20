from django.shortcuts import render


# Create your views here.


def index(request):
    context = {
        'title': 'Home dish',
    }
    return render(request, 'dish/html/index.html', context=context)


def dishes(request):
    context = {
        'title': 'Dish',
        'dish': [
            {
                'img': '/static/vendor/img/dishes/Adidas-hoodie.png',
                'name': 'Худи черного цвета с монограммами adidas Originals',
                'price': 6090,
                'description': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.',
            },
            {
                'img': '/static/vendor/img/dishes/Adidas-hoodie.png',
                'name': 'Худи черного цвета с монограммами adidas Originals',
                'price': 6090,
                'description': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.',
            },
            {
                'img': '/static/vendor/img/dishes/Adidas-hoodie.png',
                'name': 'Худи черного цвета с монограммами adidas Originals',
                'price': 6090,
                'description': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.',
            },
        ]
    }
    return render(request, 'dish/html/dishs.html', context=context)
