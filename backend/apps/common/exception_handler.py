"""
全局 DRF 异常处理：把数据库锁冲突（高并发写）转成友好 400，
避免用户看到 500 HTML 调试页；其他异常走 DRF 默认逻辑。
"""
from django.db.utils import OperationalError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc, context):
    # SQLite 并发写锁冲突：database is locked
    if isinstance(exc, OperationalError) and 'locked' in str(exc).lower():
        return Response(
            {'detail': '当前下单人数较多，请稍后重试'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return drf_exception_handler(exc, context)
