import re

import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.e2e


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
    expect(page).to_have_url(re.compile(r"/cars/\d+$"))

    # 2. 点击编辑链接
    page.get_by_role("link", name="Edit car").click()

    # 3. 等待表单加载完这辆车的数据再编辑。
    #    app.js 的 loadForm() 是异步的：在它拿到 /api/cars/{id} 之前，输入框是空的，
    #    如果这时就 fill()，随后 loadForm() 会用旧值把输入内容覆盖掉，
    #    提交的就是原值（CI 上因此报 #car-model = Civic 而不是 Accord）。
    expect(page.get_by_label("Model", exact=True)).to_have_value("Civic")
    expect(page.get_by_label("Year", exact=True)).to_have_value("2022")

    # 4. 修改型号和年份
    page.get_by_label("Model", exact=True).fill("Accord")
    page.get_by_label("Year", exact=True).fill("2023")
    page.get_by_role("button", name="Save changes").click()

    # 5. 断言详情页
    expect(page).to_have_url(re.compile(r"/cars/\d+$"))

    expect(page.locator("#car-model")).to_have_text("Accord")
    expect(page.locator("#car-year")).to_have_text("2023")

    # 6. 刷新页面
    page.reload()

    # 7. 断言修改后的数据依然存在（使用详情页的 #car-model 和 #car-year）
    expect(page.locator("#car-model")).to_have_text("Accord")
    expect(page.locator("#car-year")).to_have_text("2023")
