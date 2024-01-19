from selenium import webdriver
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
import datetime
from google.cloud import storage
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# 設置 Chrome 選項
# service = Service(executable_path=ChromeDriverManager().install())
# chrome_options = Options()
# chrome_options.add_argument('--headless')  # 如果你需要在無界面模式下運行，可以加入這一行
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--disable-notifications")
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')

# 添加自定義 User-Agent
# user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0 #zh-tw使用者'
# chrome_options.add_argument(f'user-agent={user_agent}')


def upload_image_to_gcs(bucket_name, image, destination_blob_name, folder_name, image_format='PNG'):
    """将 PIL.Image 对象上传到指定的存储桶"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(folder_name + '/' + destination_blob_name)

    # 将 Image 对象保存到 BytesIO 对象
    byte_stream = BytesIO()
    image.save(byte_stream, format=image_format)
    byte_stream.seek(0)

    # 使用 upload_from_file 方法上传
    blob.upload_from_file(byte_stream, content_type='image/png')

    

def crawlRecord(IMGUR_CLIENT_ID,name):
    # 初始化 Chrome 瀏覽器並設置選項
    driver = webdriver.Chrome(service=service, options=chrome_options)    
    uni_name = quote(name)
    # 載入網頁
    url = 'https://www.op.gg/summoners/tw/'+uni_name
    driver.get(url)

    dropdown_button = driver.find_element(By.XPATH, "//button[@class='css-17jvkpw ez6zw1e1'][contains(span, 'English')]")
    dropdown_button.click()
    # dropdown_menu = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, 'css-w2p1w6.ez6zw1e3'))
    # )
    # print("############")
    # print(dropdown_menu)
    chinese_button = driver.find_element(By.XPATH, "//button[@class='css-w2p1w6 ez6zw1e3'][contains(span, '繁體中文')]")
    chinese_button.click()
    # 等待一些時間，以確保頁面完全載入
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, 'css-1s9fubg e1jlljr10'))
    # )

    refresh_button = driver.find_element(By.XPATH, "//button[text()='戰績更新']")
    if refresh_button.is_enabled():
        refresh_button.click()
        driver.refresh()
    time.sleep(5)

    # 以元素 class 定位元素
    class_name = 'css-164r41r.e17ux5u10'
    element = driver.find_element(By.CLASS_NAME, class_name)

    # 截取指定元素的截圖
    screenshot = element.screenshot_as_png


    # 關閉瀏覽器
    driver.quit()

    img = Image.open(BytesIO(screenshot))

    # 顯示圖片
    img.save('element_screenshot.png')

    PATH = "element_screenshot.png" #A Filepath to an image on your computer"

    im = pyimgur.Imgur(IMGUR_CLIENT_ID)
    uploaded_image = im.upload_image(PATH)
    print(uploaded_image.link)
    return uploaded_image.link

def crawlRecordMap(name):
    driver = None
    # 初始化 Chrome 瀏覽器並設置選項
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 如果你需要在無界面模式下運行，可以加入這一行
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # 设置 User-Agent
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0 #zh-tw使用者'
        chrome_options.add_argument(f'user-agent={user_agent}')

        driver = webdriver.Chrome(options=chrome_options)
    # driver.maximize_window()
        uni_name = quote(name)
    # 載入網頁
        url = 'https://www.op.gg/summoners/tw/'+uni_name
        driver.get(url)

        dropdown_button = driver.find_element(By.XPATH, "//button[@class='css-17jvkpw e1efcbgv1'][contains(span, 'English')]")
        dropdown_button.click()
    # dropdown_menu = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, 'css-w2p1w6.ez6zw1e3'))
    # )
    # print("############")
    # print(dropdown_menu)
        chinese_button = driver.find_element(By.XPATH, "//button[@class='css-w2p1w6 e1efcbgv3'][contains(span, '繁體中文')]")
        chinese_button.click()
    # 等待一些時間，以確保頁面完全載入
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, 'css-1s9fubg e1jlljr10'))
    # )

        refresh_button = driver.find_element(By.XPATH, "//button[text()='戰績更新']")
        if refresh_button.is_enabled():
            refresh_button.click()
            driver.refresh()
    # time.sleep(5)

    # 以元素 class 定位元素
        element = driver.find_element(By.CLASS_NAME, 'css-1jxewmm.e1mwhike0')
    # 截取指定元素的截圖
        screenshot = element.screenshot_as_png
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        # 确保无论如何 WebDriver 都被关闭
        if driver:
            driver.quit()

    bucket_name = 'linebot-pic-opgg'
    folder_name = str(datetime.datetime.now()).replace(" ", "")

    img = Image.open(BytesIO(screenshot))
    # path = "C:\\Users\\nest\\Desktop\\opggapp\\pngformap\\"
    new_width = [240,300,460,700,1040]
    # 計算新的高度，保持原始圖片的寬高比
    for i in new_width:
        height_percent = (i / float(img.size[0]))
        new_height = int((float(img.size[1]) * float(height_percent)))
        resized_img = img.resize((i, new_height))
        upload_image_to_gcs(bucket_name, resized_img, str(i), folder_name)
        # resized_img.save(path+str(i)+'.png')
        # resized_img.save(path+str(i),format=img.format)
    return f"https://storage.googleapis.com/{bucket_name}/{folder_name}"
