from scrapy import Selector


def get_element_content(html: Selector, css_selector: str, default=None) -> str:
    """Возвращает очищенное содержимое элемента dom-дерева с селектором css_selector.

    Под очисткой подразумевается удаление лишних символов по краям:
    - пробелы
    - переносы строк
    - символы табуляции
    """
    result = html.css(css_selector).get()
    return result.strip() if result is not None else default
