import pytest
from pytest_django.asserts import assertTemplateUsed

from tests.conftest import try_get_url


@pytest.mark.parametrize(
    'url, template', [
        ('', 'blog/index.html'),
        ('posts/0/', 'blog/detail.html'),
        ('posts/1/', 'blog/detail.html'),
        ('posts/2/', 'blog/detail.html'),
        ('category/category_slug/', 'blog/category.html'),
        ('pages/about/', 'pages/about.html'),
        ('pages/rules/', 'pages/rules.html'),
    ]
)
def test_page_templates(client, url, template):
    url = f'/{url}' if url else '/'
    response = try_get_url(client, url)
    assertTemplateUsed(response, template, msg_prefix=(
        f'Убедитесь, что для отображения страницы `{url}` используется '
        f'шаблон `{template}`.'
    ))


@pytest.mark.parametrize('post_id', (0, 1, 2))
def test_post_detail(post_id, client, posts):
    url = f'/posts/{post_id}/'
    response = try_get_url(client, url)
    assert response.context is not None, (
        'Убедитесь, что в шаблон страницы `posts/<int:pk>/` '
        'передаётся контекст.'
    )
    assert isinstance(response.context.get('post'), dict), (
        'Убедитесь, что в контекст шаблона страницы `posts/<int:pk>/` '
        'по ключу `post` передаётся непустой словарь.'
    )
    assert posts[post_id] == response.context['post'], (
        f'В контексте шаблона страницы `posts/{post_id}/` значение по ключу '
        f'`post` должно равняться {post_id}-му значению списка словарей,'
        ' заданного в условии задачи.'
    )


def test_post_list(client, posts):
    url = '/'
    response = try_get_url(client, url)
    assert isinstance(response.context.get('posts'), list), (
        f'Убедитесь, что в контекст шаблона страницы `{url}` '
        'по ключу `posts` передаётся список постов из задания.'
    )
    assert response.context['posts'] == posts[::-1], (
        f'Убедитесь, что в контекст шаблона страницы `{url}` '
        'по ключу `posts` передаётся инвертированный список постов из задания.'
    )
