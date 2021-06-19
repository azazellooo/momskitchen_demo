from behave import when, then, given
from selenium import webdriver
from selenium.webdriver.support.ui import Select


@given(u'Я открыл страницу создания позиции')
def open_position_create_page(context):
    context.browser.get('http://localhost:8000/kitchen/position/create/')

@when(u'Я ввожу текст "{text}" в поле "{name}"')
def enter_text(context, text, name):
    context.browser.find_element_by_name(name).send_keys(text)

@when(u'Я нажимаю на кнопку')
def submit_form(context):
    context.browser.find_element_by_css_selector('.btn').click()

@when(u'Я выбираю опцию "{option_text}" в поле "{element_name}"')
def select_option(context, option_text, element_name):
    select = Select(context.browser.find_element_by_name(element_name))
    select.select_by_visible_text(option_text)

@when(u'Я отправляю форму')
def submit_form(context):
    context.browser.find_element_by_css_selector('#savePosition').click()

@then(u'Я должен быть на странице организаций')
def should_be_at_main(context):
    assert context.browser.current_url == 'http://localhost:8000/organizations/'

@then(u'Я должен быть на странице создания позиции')
def should_be_at_main(context):
    assert context.browser.current_url == 'http://localhost:8000/kitchen/position/create/'

