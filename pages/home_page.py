from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    # Tabs
    TAB_TOP_RATED = (By.XPATH, "//button[normalize-space()='Top Rated' or @role='tab' and contains(.,'Top Rated')]")
    TAB_TRENDING = (By.XPATH, "//button[normalize-space()='Trending' or @role='tab' and contains(.,'Trending')]")

    # Search
    INPUT_SEARCH = (By.CSS_SELECTOR, "input[placeholder*='search' i]")

    # Filters (example; adjust to actual controls)
    INPUT_YEAR = (By.XPATH, "//label[contains(.,'Year')]/following::input[1]")
    INPUT_RATING = (By.XPATH, "//label[contains(.,'Rating')]/following::input[1]")
    SELECT_GENRE = (By.XPATH, "//label[contains(.,'Genre')]/following::select[1]")
    BTN_MOVIES = (By.XPATH, "//button[contains(.,'Movies')]")
    BTN_TV = (By.XPATH, "//button[contains(.,'TV')]")

    # Cards
    CARD_TITLES = (By.CSS_SELECTOR, "[data-testid='card-title']")
    CARDS = (By.CSS_SELECTOR, "[data-testid='card']")

    # Pagination
    BTN_PAGE_1 = (By.XPATH, "//button[normalize-space()='1']")
    BTN_PAGE_2 = (By.XPATH, "//button[normalize-space()='2']")
    BTN_NEXT = (By.XPATH, "//button[contains(.,'Next') or @aria-label='Next']")

    def open_home(self):
        self.open("")

    def open_slug(self, slug):
        self.open(slug)

    def switch_to_top_rated(self):
        self.click(self.TAB_TOP_RATED)

    def search_title(self, text):
        self.type(self.INPUT_SEARCH, text)

    def set_year(self, year: int):
        self.type(self.INPUT_YEAR, str(year))

    def set_rating(self, rating: int):
        self.type(self.INPUT_RATING, str(rating))

    def choose_genre(self, label="Drama"):
        from selenium.webdriver.support.ui import Select
        select = Select(self.driver.find_element(*self.SELECT_GENRE))
        select.select_by_visible_text(label)

    def choose_movies(self):
        self.click(self.BTN_MOVIES)

    def choose_tv(self):
        self.click(self.BTN_TV)

    def titles(self):
        return self.all_texts(self.CARD_TITLES)
