import pytest
from django.urls import reverse, NoReverseMatch


def test_blog_urls():
    try:
        from blog.urls import urlpatterns as solution_urlpatterns
    except Exception as e:
        raise AssertionError(
            'При импорте списка маршрутов `urlpatterns` из файла '
            f'`blog/urls.py` произошла ошибка: {e}'
        ) from e
    assert isinstance(solution_urlpatterns, list), (
        'Убедитесь, что значением переменной `urlpatterns` является список.'
    )
    assert len(solution_urlpatterns) >= 3, (
        'Убедитесь, что добавили необходимые маршруты в список `urlpatterns` '
        'из файла `blog/urls.py`.'
    )


def test_pages_urls():
    try:
        from pages.urls import urlpatterns as solution_urlpatterns
    except Exception as e:
        raise AssertionError(
            'При импорте списка маршрутов `urlpatterns` из файла '
            f'`pages/urls.py` произошла ошибка: {e}'
        ) from e
    assert isinstance(solution_urlpatterns, list), (
        'Убедитесь, что значением переменной `urlpatterns` из файла '
        '`pages/urls.py` является список.'
    )
    assert len(solution_urlpatterns) >= 2, (
        'Убедитесь, что добавили необходимые маршруты в список `urlpatterns` '
        'из файла `pages/urls.py`.'
    )


def test_blog_appname():
    try:
        from blog.urls import app_name as solution_appname
    except ImportError as e:
        raise AssertionError(
            'Убедитесь, что указали `app_name` для приложения `blog`'
        ) from e
    except Exception as e:
        raise AssertionError(
            'При импорте переменной `app_name` из модуля `blog/urls.py` '
            f'возникла ошибка: {e}'
        ) from e
    assert solution_appname == 'blog', (
        'Проверьте значение переменной `app_name` в файле urls.py приложения '
        '`blog`'
    )


def test_pages_appname():
    try:
        from pages.urls import app_name as solution_appname
    except Exception as e:
        raise AssertionError(
            'Убедитесь, что указали `app_name` для приложения `pages`'
        ) from e
    assert solution_appname == 'pages', (
        'Проверьте значение переменной `app_name` в файле urls.py приложения '
        '`pages`'
    )


@pytest.mark.parametrize('value, name', [
    ('', 'blog:index'),
    ('0', 'blog:post_detail'),
    ('category_slug', 'blog:category_posts')
]
)
def test_blog_url_names(value, name):
    args = (value,)
    try:
        reverse(name, args=args if value else None)
    except NoReverseMatch as e:
        raise AssertionError(
            'Проверьте наличие путей из задания для приложения `blog` и '
            'корректность написания их имён. '
            f'При поиске пути по имени `{name}` '
            f'с аргументами `{args}` возникла ошибка: {e}'
        ) from e
    except Exception as e:
        raise AssertionError(
            f'При поиске пути по имени `{name}` '
            f'с аргументами `{args}` возникла ошибка: {e}'
        ) from e


@pytest.mark.parametrize('name', ['pages:about', 'pages:rules'])
def test_pages_url_names(name):
    try:
        reverse(name)
    except NoReverseMatch as e:
        raise AssertionError(
            'Проверьте наличие путей из задания для приложения `pages` и '
            'корректность написания их имён. '
            f'При поиске пути по имени `{name}` возникла ошибка: {e}'
        ) from e
    except Exception as e:
        raise AssertionError(
            f'При поиске пути по имени `{name}` '
            f'возникла ошибка: {e}'
        ) from e
