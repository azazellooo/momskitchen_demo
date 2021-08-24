from behave import when, then, given
from server.settings import BASE_URL


@given(u'Я открыл страницу редактирования профиля')
def open_position_create_page(context):
    context.browser.get(f'{BASE_URL}accounts/update/')


@when(u'Я нажимаю на кнопку редактировать')
def click_edit(context):
    context.browser.find_element_by_css_selector('#update_button').click()


@when(u'Я нажимаю на кнопку отменить')
def click_edit(context):
    context.browser.find_element_by_css_selector('#cancel_button').click()


@when(u'Я пытаюсь изменить юзернейм')
def click_edit(context):
    context.browser.find_element_by_css_selector('#id_username')


@when(u'Я нажимаю is_active')
def click_edit(context):
    context.browser.find_element_by_css_selector('#id_is_active').click()


@when(u'Я нажимаю на кнопку сохранить')
def click_edit(context):
    context.browser.find_element_by_css_selector('#save_button').click()


@then(u'Поля заблокированы')
def click_edit(context):
    assert context.browser.find_element_by_css_selector('#id_is_active').is_enabled() == False


@then(u'Я попадаю на страницу профиля')
def should_be_at_profile_page(context):
    assert context.browser.current_url == f'{BASE_URL}accounts/'
