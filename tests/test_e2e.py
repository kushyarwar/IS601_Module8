import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def navigate_to_app(page: Page, live_server: str):
    page.goto(live_server)


# --- Page load ---

def test_page_title(page: Page, live_server: str):
    expect(page).to_have_title("FastAPI Calculator")


def test_calculator_heading_visible(page: Page, live_server: str):
    heading = page.locator("h1")
    expect(heading).to_be_visible()
    expect(heading).to_contain_text("Calculator")


def test_input_fields_present(page: Page, live_server: str):
    expect(page.locator("#num-a")).to_be_visible()
    expect(page.locator("#num-b")).to_be_visible()


def test_all_buttons_present(page: Page, live_server: str):
    expect(page.locator("#btn-add")).to_be_visible()
    expect(page.locator("#btn-subtract")).to_be_visible()
    expect(page.locator("#btn-multiply")).to_be_visible()
    expect(page.locator("#btn-divide")).to_be_visible()


# --- Add ---

def test_add_two_numbers(page: Page, live_server: str):
    page.fill("#num-a", "8")
    page.fill("#num-b", "5")
    page.click("#btn-add")
    page.wait_for_function("document.getElementById('result').textContent !== '—'")
    expect(page.locator("#result")).to_have_text("13")


def test_add_negative_numbers(page: Page, live_server: str):
    page.fill("#num-a", "-4")
    page.fill("#num-b", "-6")
    page.click("#btn-add")
    page.wait_for_function("document.getElementById('result').textContent !== '—'")
    expect(page.locator("#result")).to_have_text("-10")


# --- Subtract ---

def test_subtract_two_numbers(page: Page, live_server: str):
    page.fill("#num-a", "20")
    page.fill("#num-b", "7")
    page.click("#btn-subtract")
    page.wait_for_function("document.getElementById('result').textContent !== '—'")
    expect(page.locator("#result")).to_have_text("13")


def test_subtract_results_in_negative(page: Page, live_server: str):
    page.fill("#num-a", "3")
    page.fill("#num-b", "10")
    page.click("#btn-subtract")
    page.wait_for_function("document.getElementById('result').textContent !== '—'")
    expect(page.locator("#result")).to_have_text("-7")


# --- Multiply ---

def test_multiply_two_numbers(page: Page, live_server: str):
    page.fill("#num-a", "6")
    page.fill("#num-b", "7")
    page.click("#btn-multiply")
    page.wait_for_function("document.getElementById('result').textContent !== '—'")
    expect(page.locator("#result")).to_have_text("42")


def test_multiply_by_zero(page: Page, live_server: str):
    page.fill("#num-a", "99")
    page.fill("#num-b", "0")
    page.click("#btn-multiply")
    page.wait_for_function("document.getElementById('result').textContent !== '—'")
    expect(page.locator("#result")).to_have_text("0")


# --- Divide ---

def test_divide_two_numbers(page: Page, live_server: str):
    page.fill("#num-a", "15")
    page.fill("#num-b", "3")
    page.click("#btn-divide")
    page.wait_for_function("document.getElementById('result').textContent !== '—'")
    expect(page.locator("#result")).to_have_text("5")


def test_divide_by_zero_shows_error(page: Page, live_server: str):
    page.fill("#num-a", "10")
    page.fill("#num-b", "0")
    page.click("#btn-divide")
    page.wait_for_function("document.getElementById('result').textContent !== '—'")
    result_el = page.locator("#result")
    expect(result_el).to_contain_text("zero")


# --- Edge cases ---

def test_empty_inputs_shows_message(page: Page, live_server: str):
    page.click("#btn-add")
    result_el = page.locator("#result")
    expect(result_el).to_contain_text("Enter both numbers")
