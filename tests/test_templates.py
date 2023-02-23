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
        'Убедитесь, что в шаблон страницы с адресом `posts/<int:pk>/` '
        'передаётся словарь контекста.'
    )
    assert isinstance(response.context.get('post'), dict), (
        'Убедитесь, что в словарь контекста для страницы `posts/<int:pk>/` '
        'по ключу `post` передаётся непустой словарь.'
    )
    assert posts[post_id] == response.context['post'], (
        f'Убедитесь, что в словаре контекста для страницы `posts/{post_id}/` '
        f'под ключом `post` передаётся словарь с `"id": '
        f'{post_id}` из списка `posts`.'
    )


def test_post_list(client, posts):
    url = '/'
    response = try_get_url(client, url)
    assert isinstance(response.context.get('posts'), list), (
        f'Убедитесь, что в словарь контекста для страницы `{url}` '
        'значение ключа `posts` - '
        'это инвертированный список постов из задания.'
    )
    assert response.context['posts'] == posts[::-1], (
        f'Убедитесь, что в словарь контекста для страницы `{url}` '
        'значение ключа `posts` - '
        'это инвертированный список постов из задания.'
    )
