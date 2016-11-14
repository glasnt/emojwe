from time import sleep, strftime

from selenium import webdriver
from selenium.webdriver.support.ui import Select


URL = 'http://127.0.0.1:8080/'
SAVE_DIR = '/Users/bren/Documents/code/emojwe/fetch/output/gif'

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', SAVE_DIR)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'image/gif')

browser = webdriver.Firefox(profile)
browser.get(URL)

btn = browser.find_element_by_class_name('make-gif')
status = browser.find_element_by_class_name('gif-done')

select_emoji = Select(browser.find_element_by_name('emoji'))
select_platform = Select(browser.find_element_by_name('platform'))

n_emoji = len(select_emoji.options)
n_platform = len(select_platform.options)
n_platform = 1

last_blob = None


print('start time: {}'.format(strftime("%Y-%m-%d %H:%M:%S")))

for i in range(n_emoji):
    for j in range(n_platform):
        select_emoji.select_by_index(i)
        select_platform.select_by_index(j)

        print('({}, {}): {} - {} ...'.format(
            i, j,
            select_emoji.first_selected_option.text,
            select_platform.first_selected_option.text,
        ))

        btn.click()
        while True:
            latest = status.get_attribute('data-url')
            if latest != last_blob:
                last_blob = latest
                break
            sleep(2)

browser.quit()

print('end time: {}'.format(strftime("%Y-%m-%d %H:%M:%S")))
