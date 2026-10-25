# 全栈电商项目（UniApp + Nginx + Django + Redis + Database）

完整电商系统，部署于 **D:\ecommerce**，全链路：

```
浏览器 / UniApp H5
      │  (静态资源 + /api 请求)
      ▼
Nginx  (8080, 反向代理 + 静态托管)
      │  proxy_pass /api/
      ▼
Django / waitress  (8000, DRF 业务接口, JWT 认证)
      │  django-redis 缓存中间层
      ├─────────────► Redis (6379)   ← 首页聚合 / 商品详情 / 高频查询缓存
      ▼
Django ORM
      ▼
数据库 (默认 SQLite，可一键切 MySQL)
```

## 目录结构

```
D:\ecommerce
├── backend                    # Django 后端
│   ├── config/                # settings / urls / wsgi
│   ├── apps/
│   │   ├── users/             # 注册/登录(JWT)/用户信息
│   │   ├── products/          # 分类/商品 + Redis 缓存服务 + 种子数据
│   │   ├── carts/             # 购物车(增删改查/勾选/全选)
│   │   └── orders/            # 下单(事务+锁库存)/列表/模拟支付/取消回补库存
│   ├── db/mall.sqlite3        # 数据库文件
│   └── .venv/                 # 虚拟环境(依赖全部在 D 盘)
├── frontend                   # UniApp 前端(Vue3 + Vite)
│   └── src/pages/             # 首页/分类/详情/购物车/确认订单/订单列表/我的/登录
├── deploy/nginx/nginx.conf    # Nginx 配置
├── tools/
│   ├── redis/                 # Windows Redis(6379)
│   └── nginx/                 # Windows Nginx(8080)
├── scripts/                   # 一键启停脚本
└── README.md
```

## 快速启动（全部在 D 盘）

```powershell
# ① 首次初始化（建 venv、装依赖、迁移建表、灌示例数据、收集静态文件）
D:\ecommerce\scripts\setup_backend.ps1

# ② 构建前端 H5
D:\ecommerce\scripts\build_frontend.ps1

# ③ 一键启动 Redis -> 后端 -> Nginx
D:\ecommerce\scripts\start_all.ps1

# 访问
#   商城 H5      http://localhost:8080
#   Django 后台  http://localhost:8080/admin/   账号 admin/admin123456
#   API 直连     http://localhost:8080/api/home/

# ④ 停止全部服务并释放端口
D:\ecommerce\scripts\stop_all.ps1
```

## 分层说明

| 层 | 技术 | 端口 | 说明 |
|---|---|---|---|
| 前端 | UniApp (Vue3+Vite) | 5173(dev) / 8080(生产H5) | 8 个页面，`src/api` 统一请求封装，token 自动携带 |
| 接入层 | Nginx | 8080 | 静态托管 H5 + `/api`、`/admin` 反向代理 + gzip |
| 服务层 | Django 5.2 + DRF | 8000 | waitress 生产级 WSGI，SimpleJWT 认证，订单事务+行锁 |
| 缓存层 | Redis (django-redis) | 6379 | `mall:home:v1`(首页,300s)、`mall:product:{id}`(详情,600s)，商品变更自动失效 |
| 数据层 | SQLite(默认) / MySQL(可切) | - | 4 张业务表：mall_user / mall_category / mall_product / mall_cart_item / mall_order / mall_order_item |

## API 一览

| 方法 | 路径 | 说明 | 鉴权 |
|---|---|---|---|
| POST | /api/auth/register/ | 注册 | 否 |
| POST | /api/auth/login/ | 登录，返回 JWT access/refresh | 否 |
| GET | /api/auth/user/ | 当前用户信息 | Bearer |
| GET | /api/home/ | 首页聚合（Redis 缓存） | 否 |
| GET | /api/categories/ | 一级分类 | 否 |
| GET | /api/products/?category=&keyword=&hot=&new=&page=&page_size= | 商品列表 | 否 |
| GET | /api/products/{id}/ | 商品详情（Redis 缓存） | 否 |
| GET | /api/cart/ | 购物车列表+合计 | Bearer |
| POST | /api/cart/ | 加购 {product_id, quantity} | Bearer |
| PATCH | /api/cart/{id}/ | 改数量/勾选 | Bearer |
| DELETE | /api/cart/{id}/ | 删除 | Bearer |
| POST | /api/cart/select_all/ | 全选/全不选 | Bearer |
| POST | /api/orders/ | 下单（默认购物车勾选；传 items 为立即购买） | Bearer |
| GET | /api/orders/list/?status= | 订单列表 | Bearer |
| GET | /api/orders/{id}/ | 订单详情 | Bearer |
| POST | /api/orders/{id}/pay/ | 模拟支付 | Bearer |
| POST | /api/orders/{id}/cancel/ | 取消（回补库存） | Bearer |

## 演示账号

- 商城用户：`demo / demo123456`
- Django 后台：`admin / admin123456`

## 验证 Redis 缓存生效

```powershell
# 首次请求 /api/home/ 与 /api/products/{id}/ 后（缓存键带 Django 版本前缀 :1:）
D:\ecommerce\tools\redis\redis-cli.exe -p 6379 -n 1 keys "mall:*"
#  => :1:mall:home:v1  :1:mall:product:18 ...

# 查看 TTL（首页 300s / 详情 600s）
D:\ecommerce\tools\redis\redis-cli.exe -p 6379 -n 1 ttl ":1:mall:home:v1"

# 缓存命中率
D:\ecommerce\tools\redis\redis-cli.exe -p 6379 info stats | findstr hits
```

> 注意：本机 Redis 为 5.0.14（tporadowski Windows 版），不支持 RESP3，
> `settings.py` 已强制 `CONNECTION_POOL_KWARGS: {'protocol': 2}`；
> 该旧版 redis-cli 的 `--scan` 在 Windows 上可能无输出，请用 `keys` 命令。

## 高并发与防超卖（已实测）

**并发加固（已落地）**：
1. **乐观锁原子扣减**：下单不再依赖行锁，改为条件 `UPDATE ... WHERE stock>=qty`，影响行数=0 即库存不足 → 从根上杜绝超卖（SQLite/MySQL 通用）。
2. **订单号防碰撞**：`gen_order_no()` 用「秒级时间戳 + UUID 8位hex」，并发同秒下单不撞 `UNIQUE` 约束。
3. **锁冲突友好化**：全局异常处理器把 `database is locked` 转 400「当前下单人数较多，请稍后重试」，前端 `request.js` 自动弹出，不再见 500 HTML。
4. **SQLite 写锁等待**：`DATABASES OPTIONS.timeout=20`，降低锁冲突概率。

**压测脚本**：`scripts\stress_test.py`（需先启动服务，把目标商品库存设为限量值）。

**压测结果（20 并发抢 10 件，连跑 3 轮）**：

| 轮次 | 成功下单 | 失败 | 状态码 | 终态库存 | 结论 |
|---|---|---|---|---|---|
| 1 | 10 / 20 | 10 | 全部 400（库存不足） | 0 | PASS |
| 2 | 10 / 20 | 10 | 全部 400（库存不足） | 0 | PASS |
| 3 | 10 / 20 | 10 | 全部 400（库存不足） | 0 | PASS |

每轮均精确成交限量数、库存归零无负数、无 500，失败请求全部为友好业务提示。

## 切换 MySQL（生产环境）

1. `pip install mysqlclient`（或 pymysql + 驱动）
2. 打开 `backend\config\settings.py`，启用注释中的 `DATABASES` MySQL 配置
3. 创建数据库 `CREATE DATABASE mall DEFAULT CHARACTER SET utf8mb4;`
4. 重新 `manage.py migrate` 即可，业务代码零改动（全程 Django ORM）

## 开发模式

```powershell
# 前端热更新（5173），HBuilderX 直连后端联调时把 src/api/request.js 的 BASE_URL 改为 http://localhost:8000
D:\ecommerce\scripts\dev_frontend.ps1
```

## 备注

- 商品封面图为 picsum 占位图（需联网）；生产环境替换为对象存储/本地 `/media/` 地址即可。
- 支付为模拟接口，接入真实支付网关时替换 `orders/views.py` 的 `OrderPayView`。
- 80 端口如被占用（本机 Steam++ 占用），Nginx 使用 8080。
