import re
from playwright.sync_api import expect
def test_user_creates_car_in_browser(page, live_server):
 page.goto(f"{live_server}/cars/new")
 page.get_by_label("Make", exact=True).fill("Toyota")
 page.get_by_label("Model", exact=True).fill("Yaris")
 page.get_by_label("Year", exact=True).fill("2020")
 page.get_by_label("Color", exact=False).fill("Blue")
 page.get_by_role("button", name="Create car").click()
 expect(page).to_have_url(re.compile(r"/cars/\d+$"))
 expect(page.get_by_role("heading", name="Toyota Yaris")).to_be_visible()

def test_user_edits_car_and_change_survives_reload(page, live_server):
    # 1. 创建 Honda Civic 2022
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_role("button", name="Create car").click()

    # 2. 点击编辑链接
    page.get_by_role("link", name="Edit car").click()

    # 3. 修改型号和年份
    page.get_by_label("Model", exact=True).fill("Accord")
    page.get_by_label("Year", exact=True).fill("2023")
    with page.expect_navigation():
      page.get_by_role("button", name="Save changes").click()


    # 4. 断言详情页标题
    expect(page).to_have_url(re.compile(r"/cars/\d+$"))

    # 断言具体字段，而不是整个标题
    expect(page.get_by_role("heading", name="Honda Accord")).to_be_visible()

    # 5. 刷新页面
    page.reload()

    # 6. 断言修改后的数据依然存在（使用详情页的 #car-model 和 #car-year）
    expect(page.locator("#car-model")).to_have_text("Accord")
    expect(page.locator("#car-year")).to_have_text("2023")
