"""高并发抢购压测：20 并发抢 1 件限量商品（库存10），验证不超卖、无500。

运行：D:\ecommerce\backend\.venv\Scripts\python.exe D:\ecommerce\scripts\stress_test.py
依赖：服务已启动（Redis/后端/Nginx），演示账号 demo/demo123456
"""
import json
import sys
import threading
import time
import urllib.error
import urllib.request
from collections import Counter

BASE = 'http://localhost:8080/api'
TOKEN = None
results = []          # (ok, status_code, detail)
results_lock = threading.Lock()

CONCURRENCY = 20      # 并发数
LIMIT_STOCK = 10      # 限量库存（下单前需用 seed 或 manage.py 设好）
PRODUCT_ID = 2        # 压测商品（星曜X10 5G智能手机）


def http(method, path, body=None, token=None, timeout=15):
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('Content-Type', 'application/json')
    if token:
        req.add_header('Authorization', 'Bearer ' + token)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
    except Exception as e:
        return -1, str(e)


def login():
    code, body = http('POST', '/auth/login/',
                      {'username': 'demo', 'password': 'demo123456'})
    assert code == 200, body
    return json.loads(body)['access']


def grab(_i):
    code, body = http('POST', '/orders/', {
        'items': [{'product_id': PRODUCT_ID, 'quantity': 1}],
        'from_cart': False,
        'receiver_name': '压测用户',
        'receiver_phone': '13800000000',
        'receiver_address': '并发压测地址',
    }, token=TOKEN)
    detail = ''
    try:
        detail = json.loads(body).get('detail', '')
    except Exception:
        detail = body[:80]
    if code == 500:
        # 诊断：把 500 响应完整落盘，便于定位异常
        with open(r'D:\ecommerce\backend\logs\stress_500.html', 'w', encoding='utf-8') as f:
            f.write(body)
    with results_lock:
        results.append((code == 201, code, detail))


def main():
    global TOKEN
    TOKEN = login()
    out = []
    out.append(f'压测配置：并发 {CONCURRENCY} 抢库存 {LIMIT_STOCK}（商品ID {PRODUCT_ID}）')

    threads = [threading.Thread(target=grab, args=(i,)) for i in range(CONCURRENCY)]
    t0 = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    cost = time.time() - t0

    ok = [r for r in results if r[0]]
    fail = [r for r in results if not r[0]]
    fail_codes = Counter(r[1] for r in fail)
    details = Counter(r[2] for r in fail)

    out.append(f'耗时: {cost:.2f}s')
    out.append(f'成功下单: {len(ok)} / {CONCURRENCY}')
    out.append(f'失败: {len(fail)}  状态码分布: {dict(fail_codes)}')
    for d, c in details.most_common():
        out.append(f'  失败原因[{c}次]: {d}')

    code, body = http('GET', f'/products/{PRODUCT_ID}/')
    prod = json.loads(body)
    stock = prod.get('stock')
    out.append(f'终态库存: {stock}')

    # 断言：不多卖、库存精确归零、无 500
    ok_flag = (len(ok) == LIMIT_STOCK and stock == 0 and 500 not in fail_codes)
    out.append('PASS: 不超卖、无500、库存精确归零，限购全部成交' if ok_flag
               else f'FAIL: 成功={len(ok)}/{LIMIT_STOCK} 库存={stock} 500={500 in fail_codes}')

    text = '\n'.join(out)
    print(text)
    with open(r'D:\ecommerce\backend\logs\stress_result.txt', 'w', encoding='utf-8') as f:
        f.write(text + '\n')
    sys.exit(0 if ok_flag else 1)


if __name__ == '__main__':
    main()
