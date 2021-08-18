from behave import when, then, given


URL = 'http://localhost:8000/'
my_token = '8c2334ed-f09c-4eb5-b89c-aadd651dce9f'

@given(u'Я открыл страницу создания дополнения')
def open_position_create_page(context):
    context.browser.get(f'{URL}kitchen/additional/create/')

@given(u'Я попадаю на страницу просмотра детального просмотра дополнения')
def should_be_at_detail_additional(context):
    context.browser.get(f'{URL}kitchen/additional/1/')

@given(u'Я зашел на "{page}"')
def visit(context, page):
    context.browser.get(f'{URL}accounts/{my_token}')


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
    assert context.browser.current_url == f'{URL}kitchen/additional/list/'


@then(u'Я должен быть на странице создания дополнения')
def should_be_at_create(context):
    assert context.browser.current_url == f'{URL}kitchen/additional/create/'


@then(u'Я попадаю на страницу просмотра списка дополнений')
def should_be_at_main(context):
    assert context.browser.current_url == f'{URL}kitchen/additional/list/'