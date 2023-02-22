from django import get_version


def test_django_version():
    min_ver = '3.2.16'
    assert get_version() >= min_ver, (
        f'Пожалуйста, используйте версию Django >= {min_ver}')


def test_static_dir(settings_app_name, project_dirname):
    settings_app = __import__(f'{settings_app_name}', globals(), locals())
    try:
        staticfiles_dirs = settings_app.settings.STATICFILES_DIRS
    except Exception as e:
        raise AssertionError(
            'Убедитесь, что задали переменную `STATICFILES_DIRS` в файле '
            'settings.py'
        ) from e
    assert isinstance(staticfiles_dirs, list), (
        'Убедитесь, что значением переменной `STATICFILES_DIRS` в файле '
        'settings.py является списком.'
    )


def test_apps_registered(settings_app_name, project_dirname):
    register_apps_old_style = ['blog', 'pages']
    register_apps_new_style = [
        'blog.apps.BlogConfig', 'pages.apps.PagesConfig']
    settings_app = __import__(f'{settings_app_name}')
    installed_apps = settings_app.settings.INSTALLED_APPS
    registered = set(installed_apps)
    app_names = ' и '.join(f'`{n}`' for n in register_apps_old_style)
    assert set(register_apps_new_style).issubset(registered) or (
        set(register_apps_old_style).issubset(registered)
    ), (
        f'Убедитесь, что зарегистрировали приложения {app_names} в файле '
        'settings.py'
    )
