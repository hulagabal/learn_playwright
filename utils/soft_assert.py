class SoftAssert:

    def __init__(self):
        self.errors = []

    # -------------------------------
    # BASIC ASSERTS
    # -------------------------------
    def assert_true(self, condition, message="Condition failed"):
        if not condition:
            self.errors.append(f"[TRUE FAILED] {message}")

    def assert_false(self, condition, message="Condition should be False"):
        if condition:
            self.errors.append(f"[FALSE FAILED] {message}")

    def assert_equal(self, actual, expected, message="Values not equal"):
        if actual != expected:
            self.errors.append(
                f"[EQUAL FAILED] {message} | Expected: {expected}, Got: {actual}"
            )

    def assert_in(self, item, container, message="Item not found"):
        if item not in container:
            self.errors.append(
                f"[IN FAILED] {message} | '{item}' not in '{container}'"
            )

    # -------------------------------
    # PLAYWRIGHT HELPERS
    # -------------------------------
    def assert_visible(self, locator, message="Element not visible"):
        if not locator.is_visible():
            self.errors.append(f"[VISIBLE FAILED] {message}")

    def assert_text(self, locator, expected, message="Text mismatch"):
        actual = locator.text_content()
        if actual != expected:
            self.errors.append(
                f"[TEXT FAILED] {message} | Expected: '{expected}', Got: '{actual}'"
            )

    def assert_url_contains(self, page, text, message="URL mismatch"):
        if text not in page.url.lower():
            self.errors.append(
                f"[URL FAILED] {message} | URL: {page.url}"
            )

    # -------------------------------
    # FINAL ASSERT
    # -------------------------------
    def assert_all(self):
        if self.errors:
            error_message = "\n\n".join(self.errors)
            raise AssertionError(f"\nSOFT ASSERT FAILURES:\n{error_message}")