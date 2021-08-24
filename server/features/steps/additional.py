from behave import when, then, given
from server.settings import BASE_URL


my_token = '4e346bad-54e9-4fad-a3db-90ff2efbd700'

@given(u'Я открыл страницу создания дополнения')
def open_position_create_page(context):
    context.browser.get(f'{BASE_URL}kitchen/additional/create/')

@given(u'Я попадаю на страницу просмотра детального просмотра дополнения')
def should_be_at_detail_additional(context):
    context.browser.get(f'{BASE_URL}kitchen/additional/1/')

@given(u'Я зашел на "{page}"')
def visit(context, page):
    context.browser.get(f'{BASE_URL}accounts/{my_token}')


@when(u'Я ввожу "{text}" в поле "{name}"')
def enter_text(context, text, name):
    context.browser.find_element_by_name(name).clear()
    context.browser.find_element_by_name(name).send_keys(text)


@when(u'Я нажимаю кнопку редактировать')
def click_edit(context):
    context.browser.find_element_by_css_selector('#edit_btn').click()


@when(u'Я нажимаю сохранить')
def submit_form(context):
    context.browser.find_element_by_css_selector('#savePosition').click()


@when(u'Я попадаю на страницу просмотра списка дополнений')
def should_be_at_additional_list(context):
    assert context.browser.current_url == f'{BASE_URL}kitchen/additional/list/'


@then(u'Я должен быть на странице создания дополнения')
def should_be_at_create(context):
    assert context.browser.current_url == f'{BASE_URL}kitchen/additional/create/'


@then(u'Я попадаю на страницу просмотра списка дополнений')
def should_be_at_main(context):
    assert context.browser.current_url == f'{BASE_URL}kitchen/additional/list/'
