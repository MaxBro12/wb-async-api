# Wildberries-Async

Библиотека для асинхронного взаимодействия с API Wildberries, пока в разработке. Реализованно лимитированние запросов и типизация данных frozen-slots датаклассами.

## В разработке

Сейчас библиотека находится в стадии разработки. Я делаю её по мере необходимости. Если есть какие-то предложения или проблемы, не стесняйтесь открывать [issue](https://github.com/MaxBro12/wb-async-api/issues).

## Установка

```shell
pip install git+https://github.com/MaxBro12/wb-async-api.git@master
uv add git+https://github.com/MaxBro12/wb-async-api.git@master
```

## Пример
```python
import asyncio
from wb_async_api import WBService

async def main():
    client = WBService(
        token='token key', # - токен для авторизации
        test=True # - тестовый режим (при использовании тестового токена)
    )
    result = await client.marketplace.offices()

if __name__ == "__main__":
    asyncio.run(main())
```
