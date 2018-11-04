import baostock as bs
import datetime
import pandas as pd
# now_time = datetime.datetime.now()
# print(now_time)
# delta = datetime.timedelta(days=-7)
# n_days = now_time+delta
# print(n_days)

class StockFunctions:
    #输出从当前开始的一周的K线
    def k_Line(self,stockcode):
        lg = bs.login(user_id="anonymous", password="123456")
        if lg.error_code!="0":
            return "login error"
        now_time = datetime.datetime.now()
        delta = datetime.timedelta(days=-9)
        before_time = now_time+delta
        now_time = now_time.strftime('%Y-%m-%d')
        before_time = before_time.strftime('%Y-%m-%d')
        rs = bs.query_history_k_data(stockcode,
        "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST,peTTM,psTTM,pcfNcfTTM,pbMRQ",
                                     start_date=before_time, end_date=now_time,
                                     frequency="d", adjustflag="3")


        labels = "交易所行情日期,证券代码,开盘价," \
                 "最高价,最低价,收盘价,昨日收盘价,成交量（累计单位：股)," \
                 "成交额（单位：人民币元）,复权状态(1：后复权 2：前复权 3：不复权)," \
                 "换手率,交易状态(1：正常交易 0：停牌),涨跌幅,动态市盈率,市净率,市销率,市现率,是否ST股"

        data_list = []
        columns = rs.fields
        # columns = labels.split(",")
        data_list.append(columns)
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        return data_list

    #三年除权信息
    def ChuquanInfo(self,stockcode):
        lg = bs.login()
        if lg.error_code!="0":
            return "login error"
        #### 查询除权除息信息####
        # 查询2015年除权除息信息
        rs_list = []
        rs_dividend_2015 = bs.query_dividend_data(code=stockcode, year="2015", yearType="report")

        labels = "证券代码,预批露公告日," \
                 "股东大会公告日期,预案公告日," \
                 "分红实施公告日,股权登记告日," \
                 "除权除息日期,派息日,红股上市交易日," \
                 "每股股利税前,每股股利税后," \
                 "每股红股,分红送转,每股转增资本"

        # columns = labels.split(",")
        columns = rs_dividend_2015.fields
        rs_list.append(columns)

        while (rs_dividend_2015.error_code == '0') & rs_dividend_2015.next():
            rs_list.append(rs_dividend_2015.get_row_data())

        # 查询2016年除权除息信息
        rs_dividend_2016 = bs.query_dividend_data(code=stockcode, year="2016", yearType="report")
        while (rs_dividend_2016.error_code == '0') & rs_dividend_2016.next():
            rs_list.append(rs_dividend_2016.get_row_data())

        # 查询2017年除权除息信息
        rs_dividend_2017 = bs.query_dividend_data(code=stockcode, year="2017", yearType="report")
        while (rs_dividend_2017.error_code == '0') & rs_dividend_2017.next():
            rs_list.append(rs_dividend_2017.get_row_data())
        return rs_list
    #复权因子
    def FuquanInfo(self,stockcode):
        lg = bs.login()
        if lg.error_code!="0":
            return "login error"

        # 查询2015至2017年复权因子
        rs_list = []
        rs_factor = bs.query_adjust_factor(code=stockcode, start_date="2015-01-01", end_date="2017-12-31")

        labels = "证券代码,除权除息日期,向前复权因子,向后复权因子,本次复权因子"
        # columns = labels.split(",")
        columns = rs_factor.fields
        rs_list.append(columns)
        while (rs_factor.error_code == '0') & rs_factor.next():
            rs_list.append(rs_factor.get_row_data())
        # 登出系统
        bs.logout()
        return rs_list
    #季频盈利能力
    def Jipinyingli(self,stockcode):
        lg = bs.login()
        if lg.error_code != "0":
            return "login error"
        # 查询季频估值指标盈利能力
        profit_list = []
        rs_profit = bs.query_profit_data(code=stockcode, year=2017, quarter=2)
        labels = "证券代码,公司发布财报的日期,财报统计的季度的最后一天," \
                 "净资产收益率(%),销售净利率(%),销售毛利率(%)," \
                 "净利润(万元),每股收益,主营营业收入(百万元),总股本,流通股本"
        # columns = labels.split(",")
        columns = rs_profit.fields
        profit_list.append(columns)
        while (rs_profit.error_code == '0') & rs_profit.next():
            profit_list.append(rs_profit.get_row_data())
        bs.logout()
        return profit_list
    #季频营运能力
    def Jipinyingyun(self,stockcode):
        lg = bs.login()
        if lg.error_code != "0":
            return "login error"
        operation_list = []
        rs_operation = bs.query_operation_data(code=stockcode, year=2017, quarter=2)
        labels = "证券代码,公司发布财报的日期," \
                 "财报统计的季度的最后一天,净资产收益率(%),销售净利率(%)," \
                 "销售毛利率(%),净利润(万元),每股收益,主营营业收入(百万元),总股本,流通股本"
        # columns = labels.split(",")
        columns = rs_operation.fields
        operation_list.append(columns)
        while (rs_operation.error_code == '0') & rs_operation.next():
            operation_list.append(rs_operation.get_row_data())
        bs.logout()
        return operation_list
    #季频成长能力
    def Jipinchengzhang(self,stockcode):
        lg = bs.login()
        if lg.error_code != "0":
            return "login error"
        growth_list = []
        rs_growth = bs.query_growth_data(code=stockcode, year=2017, quarter=2)

        labels = "证券代码,公司发布财报的日期,财报统计的季度的最后一天," \
                 "净资产同比增长率,总资产同比增长率,净利润同比增长率,基本每股收益同比增长率,归属母公司股东净利润同比增长率"

        # columns = labels.split(",")
        columns = rs_growth.fields
        growth_list.append(columns)
        while (rs_growth.error_code == '0') & rs_growth.next():
            growth_list.append(rs_growth.get_row_data())
        bs.logout()
        return growth_list

    #季频偿债能力
    def Jipinchangzhai(self,stockcode):
        lg = bs.login()
        if lg.error_code != "0":
            return "login error"
        balance_list = []
        rs_balance = bs.query_balance_data(code=stockcode, year=2017, quarter=2)

        labes = "证券代码,公司发布财报的日期,财报统计的季度的最后一天," \
                "流动比率,速动比率,现金比率,总负债同比增长率,资产负债率,权益乘数"
        # columns = labes.split(",")
        columns = rs_balance.fields
        balance_list.append(columns)
        while (rs_balance.error_code == '0') & rs_balance.next():
            balance_list.append(rs_balance.get_row_data())
        bs.logout()
        return balance_list
    #季频现金流
    def Jipinxianjinliu(self,stockcode):
        # 登陆系统
        lg = bs.login()
        if lg.error_code != "0":
            return "login error"
        cash_flow_list = []
        rs_cash_flow = bs.query_cash_flow_data(code=stockcode, year=2017, quarter=2)
        labels = "证券代码,公司发布财报的日期,财报统计的季度的最后一天," \
                 "流动资产除以总资产,非流动资产除以总资产,有形资产除以总资产," \
                 "已获现金倍数,经营活动产生的现金流量净额除以营业收入," \
                 "经营性现金净流量除以净利润,经营性现金净流量除以营业总收入"
        # columns = labels.split(",")
        columns = rs_cash_flow.fields
        cash_flow_list.append(columns)
        while (rs_cash_flow.error_code == '0') & rs_cash_flow.next():
            cash_flow_list.append(rs_cash_flow.get_row_data())
        # 登出系统
        bs.logout()
        return cash_flow_list

    #季频杜邦指数
    def Jipindubang(self,stockcode):
        # 登陆系统
        lg = bs.login()
        if lg.error_code != "0":
            return "login error"

        dupont_list = []
        rs_dupont = bs.query_dupont_data(code=stockcode, year=2017, quarter=2)
        labels = "证券代码,公司发布财报的日期," \
                 "财报统计的季度的最后一天,净资产收益率," \
                 "权益乘数,总资产周转率,归属母公司股东的净利润/净利润," \
                 "净利润/营业总收入," \
                 "净利润/利润总额,利润总额/息税前利润," \
                 "息税前利润/营业总收入"

        # columns = labels.split(",")
        columns = rs_dupont.fields
        dupont_list.append(columns)
        while (rs_dupont.error_code == '0') & rs_dupont.next():
            dupont_list.append(rs_dupont.get_row_data())
        # 登出系统
        bs.logout()
        return dupont_list
    #季频业绩快报
    def Jipinyejikuaibao(self,stockcode):
        lg = bs.login()
        if lg.error_code != "0":
            return "login error"
        #### 获取公司业绩快报 ####
        rs = bs.query_performance_express_report(code=stockcode, start_date="2015-01-01", end_date="2017-12-31")
        result_list = []

        labels = "证券代码,业绩快报披露日,业绩快报统计日期,业绩快报披露日(最新)," \
                 "业绩快报总资产,业绩快报净资产,业绩每股收益增长率,业绩快报净资产收益率ROE-加权," \
                 "业绩快报每股收益EPS-摊薄,业绩快报营业总收入同比,业绩快报营业利润同比"
        # columns = labels.split(",")
        columns = rs.fields
        result_list.append(columns)
        while (rs.error_code == '0') & rs.next():
            result_list.append(rs.get_row_data())
            # 获取一条记录，将记录合并在一起
        #### 登出系统 ####
        bs.logout()
        return result_list
    #季频业绩预告
    def JipinyejiPredict(self,stockcode):
        #### 登陆系统 ####
        lg = bs.login()
        if lg.error_code != "0":
            return "login error"
        #### 获取公司业绩预告 ####
        rs_forecast = bs.query_forecast_report(code=stockcode, start_date="2010-01-01", end_date="2017-12-31")
        rs_forecast_list = []
        labels = "证券代码,业绩预告发布日期," \
                 "业绩预告统计日期,业绩预告类型," \
                 "业绩预告摘要,预告归属于母公司的净利润增长上限(%)," \
                 "预告归属于母公司的净利润增长下限(%)"
        # columns = labels.split(",")
        columns = rs_forecast.fields
        rs_forecast_list.append(columns)
        while (rs_forecast.error_code == '0') & rs_forecast.next():
            # 分页查询，将每页信息合并在一起
            rs_forecast_list.append(rs_forecast.get_row_data())
        bs.logout()
        return rs_forecast_list
    #证券基本资料
    def StockInfo(self,stockcode):
        lg = bs.login()
        if lg.error_code != "0":
            return "login error"
        # 获取证券基本资料
        rs = bs.query_stock_basic(code=stockcode)
        # 打印结果集
        data_list = []
        labels = "证券代码,证券名称,上市日期,退市日期," \
                 "证券类型1:股票2:指数 3:其它," \
                 "上市状态1:上市0:退市"

        # columns = labels.split(",")
        columns = rs.fields
        data_list.append(columns)
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        # 登出系统
        bs.logout()
        return data_list


# stockFunction = StockFunctions()
# a = stockFunction.ChuquanInfo("sh.600000")
