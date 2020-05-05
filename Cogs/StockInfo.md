The `k.stock [Ticker] [Timeframe]` command supports stock data from NASDAQ, NYSE, S&P 500, AMEX, DOW, TSX, LSE, FTSE, DAX, SSE, MSX, BSE,
B3, ASX, KRX, and KOSDAQ (probably more, but I have yet to check any others).

<br><br>

**Parameters:**

`[Ticker]`: must be a valid ticker symbol (ex. `AAPL`)<br>
`[Timeframe]`: Choose one of `short`, `medium`, or `long` (`s`, `m`, or `l`)<br><br>
Neither of these parameters are case sensitive (`AAPL` = `aapl`, `SHORT` = `short`).

<br><br>

**Suffixes**: 

**No suffix required**: NASDAQ, NYSE, S&P 500, AMEX, DOW

Checking listings from these DO NOT require a suffix.

Example: `k.stock AAPL short`

Full listings: 
- [NASDAQ](https://www.advfn.com/nasdaq/nasdaq.asp)
- [NYSE](https://www.advfn.com/nyse/newyorkstockexchange.asp)
- [S&P 500](https://markets.businessinsider.com/index/components/s&p_500)
- [AMEX](https://www.advfn.com/amex/americanstockexchange.asp)
- [DOW](https://markets.businessinsider.com/index/components/dow_jones?op=1)

<br>

**Suffix required:** TSX, LSE, FTSE, DAX, SSE, MSX, BSE, B3, ASX, KRX, KOSDAQ

Checking listings from these DO require a suffix. Note that Alpha Vantage does not officially support these exchanges.
Requesting data from them may be faulty/inaccurate. The suffix that corresponds to each market is listed below:

**TSX**:<br>
- Suffix: `.TO`
- Example: `k.stock AC.TO short`
- [TSX full listings](http://www.eoddata.com/StockList/TSX.htm)

**FTSE**: 
- Suffix: `.LON`
- Example: `k.stock SCT.LON medium`
- [FTSE full listings](https://markets.businessinsider.com/index/components/ftse_100)

**LSE**:
- Suffix: `.L`
- Example: `k.stock AAIF.L long`
- [LSE full listings](https://www.dividendmax.com/stock-exchange-listings/united-kingdom/london-stock-exchange)

**DAX**: 
- Suffix: `.DE`
- Example: `k.stock BMW.DE short`
- [DAX full listings](https://markets.businessinsider.com/index/components/dax?op=1)

**SSE**: 
- Suffix: `.SS`
- Example: `k.stock 600578.SS medium`
- [SSE full listings](https://en.wikipedia.org/wiki/Category:Companies_listed_on_the_Shanghai_Stock_Exchange)

**MSX**: 
- Suffix: `.MX`
- Example: `k.stock ALFAA.MX long`
- [MSX full listings](https://en.wikipedia.org/wiki/List_of_companies_traded_on_the_Bolsa_Mexicana_de_Valores)

**BSE**: 
- Suffix: `.BO`
- Example: `k.stock ABCAPITAL.BO short`
- [BSE full listings](https://en.wikipedia.org/wiki/Category:Companies_listed_on_the_Bombay_Stock_Exchange)

**B3**: 
- Suffix: `.SA`
- Example: `k.stock CMIG4.SA medium`
- [B3 full listings](https://en.wikipedia.org/wiki/List_of_companies_listed_on_Ibovespa)

**ASX**: 
- Suffix: `.AX`
- Example: `k.stock NAN.AX long`
- [ASX full listings](https://www.asx.com.au/asx/research/listedCompanies.do)

<br>

*These two are particularly faulty. They might not work half the time.*

<br>

**KRX**: 
- Suffix: `.KS`
- Example: `k.stock 000040.KS short`
- [KRX full listings](https://www.koreanbulls.com/SignalList.aspx?lang=en&MarketSymbol=KOREA)

**KOSDAQ**: *Might not support medium-term. Further testing needed.*
- Suffix: `.KQ`
- Example: `k.stock 009520.KQ long`
- [KOSDAQ full listings](https://www.koreanbulls.com/SignalList.aspx?lang=en&MarketSymbol=KOREAOTC)
