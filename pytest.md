# Pytest使用指南
## 入門與快速上手
### 安裝pytest與相關plugin
於項目目錄執行以下指令
```bash
pipenv install --dev
```
它會從Pipfile裡頭安裝所有測試需要的dev-packages。

執行測試
```bash
pipenv run pytest
```

### 測試文件命名規則
Pytest會從 testpath 或當前目錄開始遞歸查找相關的測試項目，測試項目必須滿足以下的命名規則：
- 檔案命名為 test_*.py 或 *_test.py
- 以test為前綴的函數或方法
- 以Test為前綴的測試類 (不帶 __init__ 方法)

有關如何自定義測試文件的命名規則，可以參考[官方範例](https://www.osgeo.cn/pytest/example/pythoncollection.html)

### 創建第一個測試
用四行代碼創建第一個測試
```python
# content of test_sample.py
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 5
```
就是這樣簡單，然後可以執行測試功能：
```bash
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-5.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 1 item

test_sample.py F                                                     [100%]

================================= FAILURES =================================
_______________________________ test_answer ________________________________

    def test_answer():
>       assert func(3) == 5
E       assert 4 == 5
E        +  where 4 = func(3)

test_sample.py:5: AssertionError
========================= 1 failed in 0.12 seconds =========================
```
此測試報告會返回一個失敗，因為func(3)返回值不等於5。

### 測試分類
當測試案例開發到一定數量時，你可能會希望將測試分組，你有兩個選擇，用module將測試分開成不同的檔案，或是用將相同屬性的測試案例分組成一個類。
```python
# content of test_class.py
class TestClass(object):
    def test_one(self):
        x = "this"
        assert 'h' in x

class TestClass2(object):
    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')

```

## pytest夾具：顯式、模塊化、可擴展
pytest.fixture提供了一個模塊化的annotation，它可以用來激活你所需要的測試函數、模塊或是類。並且提供參數化的功能，或者讓你可以跨函數、類、模塊或是整個測試項目中重覆使用。

## 夾具項目參數化
```python
# content of ./test_smtpsimple.py
import pytest

@pytest.fixture
def smtp_connection():
    import smtplib
    return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)

def test_ehlo(smtp_connection):
    response, msg = smtp_connection.ehlo()
    assert response == 250
    assert 0 # for demo purposes
```
## 共享測試數據
利用夾具項目參數化的方法，我們可以先創建一個class，再寫一個夾具項目化函數返回一個實例，當我們需要跨類或是跨函數傳遞參數時，可以把數據先保存在實例的參數裡，再引用該實例的參數。
```python
@pytest.fixture
def item():
    return Item()

# 創建一個保存數據用的class
class Item:
    token = None


class TestLogin:
    def test_login(self,item):
        r = requests.post('/login',headers=headers,data=data)
        if r.status == 200:
            # 登入成功，將token保存於item.token
            item.token = json.loads(r.data.decode())['token']
            
class TestShopping:
    def test_checkout(self,item):
        # 將登入後拿到的token放到post data裡面
        data.update({'token':item.token})
        # do the shopping process
        ...
        r = requests.post('/checkout',headers=heasers,data=data)
        assert r.status == 200
```

## conftest.py 共享夾具功能
conftest.py是pytest的entrypoint，如果是有一個fixture夾具是被多個測試文件使用的，你可以將它保存在conftest中，你不需要在測試文件import conftest，pytest會在測試執行前先執行conftest內定義的所有代碼。

舉例來說，我們可以將上一個例子重構成不同的module：
```python
# content of conftest.py
@pytest.fixture
def item():
    return Item()

# 創建一個保存數據用的class
class Item:
    token = None


# content of test_login.py
class TestLogin:
    def test_login(self,item):
        r = requests.post('/login',headers=headers,data=data)
        if r.status == 200:
            # 登入成功，將token保存於item.token
            item.token = json.loads(r.data.decode())['token']
         
# content of test_shopping.py   
class TestShopping:
    def test_checkout(self,item):
        # 將登入後拿到的token放到post data裡面
        data.update({'token':item.token})
        # do the shopping process
        ...
        r = r.post('/checkout',headers=heasers,data=data)
        assert r.status == 200
```

## 常用夾具介紹
### pytest.mark.skipif
當判斷條件為True時會跳過被標記的測試案例，如果測試環境或是依賴不允許某些測試，可以用這個標記跳過

> 參數: condition (bool or str) -- True/False skip測試的條件判斷式或 condition string   
reason (str) -- 跳過測試的原因

### pytest.mark.xfail
這個方法是我們直接將測試案例標記為失敗，通常用在功能未完成、已知有問題的測試案例。或是需要測試前置作業的測試案例，當前置作業執行失敗時，我們就可以直接將該案例標記失敗，也就是xfail。

舉例來說，我們將下面這個已知為失敗的函數用pytest.mark.xfail標記。
```python
    @pytest.mark.xfail
    def test_one(self):
            print("test_one方法执行" )
            assert 1==2
```
執行後它會顯示1 xfailed而不是顯示失敗。
```bash
===============================  1 xfailed  in 0.02s =========================
```
> 參數: strict -- True/False ，預設為False，當strict=True時，測試案例執行成功會被標為Fail，而不是 xpassed

### 自定義標記
我們可以自定義標記，例如我們想用標記分類想要執行的測試範圍，未標記的測試案例直接跳過。

首先要創建一個pytest.ini的文件放在項目根目錄底下，在此項目中我們為pytest.mark定義了新的標記home、product、basket、checkout和complete。
```
# content of pytest.ini
[pytest]
markers = home
    product
    basket
    checkout
    complete
```
並且在測試文件中標記
```python
# content of test_app.py
@pytest.mark.home
class TestClass:
        ...
        

@pytest.mark.product
class TestProduct:
        ...
        
@pytest.mark.basket
class TestCart:
        ...
```

pytest 執行時可加入參數 -m 指定需要測試的範圍，未被指定的測試項目會自動略過。
```bash
$  pytest -v -m basket
rootdir: /liveServerPy, inifile: pytest.ini
plugins: mock-1.11.2, flask-sqlalchemy-1.0.2, cov-2.8.1, flask-0.15.0
collected 13 items / 8 deselected / 5 selected  
========== 5 passed, 8 deselected, 2 warnings in 3.46s ==========
```
## 配置文件
pytest.ini是pytest的主要配置文件，可以改變pytest的預設參數
ini檔案的基本格式為\[pytest]開頭，每一行為你要覆寫pytest的預設參數內容。
```bash
[pytest]
# 綁定的pytest 參數
addopts = --strict-markers
# xfail_strict的預設值改為true
xfail_strict=true
# 自定義marker
markers = home
    product
    basket
    checkout
    complete

```

使用pytest --help指令可以查找pytest.ini的設置項目
```bash
  markers (linelist)       markers for test functions
  empty_parameter_set_mark (string) default marker for empty parametersets
  norecursedirs (args)     directory patterns to avoid for recursion
  testpaths (args)         directories to search for tests when no files or dire

  console_output_style (string) console output: classic or with additional progr

  usefixtures (args)       list of default fixtures to be used with this project

  python_files (args)      glob-style file patterns for Python test module disco

  python_classes (args)    prefixes or glob names for Python test class discover

  python_functions (args)  prefixes or glob names for Python test function and m

  xfail_strict (bool)      default for the strict parameter of 
  addopts (args)           extra command line options
  minversion (string)      minimally required pytest version
```