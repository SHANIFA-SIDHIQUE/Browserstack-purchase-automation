import pytest
def pytest_configure(config):
    config.option.log_cli = True
    config.option.log_file = 'browserstack.log'
    config.option.log_file_level = 'INFO'


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == 'call':
         driver = item.funcargs['setup']
         if report.skipped or report.failed:
           filename = "failedscreen.png"
           _capture_screenshot(driver, filename)
           extras.append(pytest_html.extras.image(filename))
         report.extras = extras

def _capture_screenshot(driver, name):
     print("take screenshot")
     driver.get_screenshot_as_file(name)
