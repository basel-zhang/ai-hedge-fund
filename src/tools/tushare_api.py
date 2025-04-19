# -*- coding: utf-8 -*-
import os

import tushare as ts

from data.models import Price

pro = ts.pro_api(os.environ.get("TUSHARE_API_KEY"))


def get_prices(ticker: str, start_date: str, end_date: str) -> list[Price]:
    df = pro.daily(ts_code=ticker, start_date=start_date, end_date=end_date)
    if df.empty:
        return []
    else:
        # Use list comprehension with to_dict('records') for better performance
        prices = [
            Price(
                open=row["open"],
                close=row["close"],
                high=row["high"],
                low=row["low"],
                volume=row["vol"],
                time=row["trade_date"],
            )
            for row in df.to_dict("records")
        ]
        return prices
