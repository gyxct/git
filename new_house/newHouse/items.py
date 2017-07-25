# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BjNewhouseItem(scrapy.Item):
    # 北京
    # 精确到房屋
    project_name = scrapy.Field() #项目名称
    project_addr = scrapy.Field() #坐落位置
    house_owner_name = scrapy.Field() #房屋所有权人名称
    house_owner_number = scrapy.Field() #房屋所有权证号
    publish_date = scrapy.Field() #发证日期
    publish_place = scrapy.Field() #转移登记办理部门
    land_use_number = scrapy.Field() #土地使用权证号

    use_for = scrapy.Field() #房屋用途
    build_type = scrapy.Field() #户型
    build_area = scrapy.Field() #建筑面积
    build_in_area = scrapy.Field() #套内面积
    sale_for_build = scrapy.Field() #建筑面积拟售价格
    sale_for_build_in = scrapy.Field() #套内面积拟售价格
    house_url = scrapy.Field() #采集房屋的URL
    city = scrapy.Field() #城市
    province = scrapy.Field()  #省份
    crawl_time = scrapy.Field()  #抓取时间
    house_marking = scrapy.Field()  #房屋标识
    building_name = scrapy.Field()#楼号

class GzNewhouseItem(scrapy.Item):
    # 广州
    # 精确到小区
    project_name = scrapy.Field() #项目名称
    project_address = scrapy.Field()  #坐落位置
    saled_House_num = scrapy.Field() #累计已售房屋套数
    unsaledHouse_num = scrapy.Field() #未售房屋套数
    develop_company = scrapy.Field() #开发单位
    use_area = scrapy.Field()   #占地面积
    deal_area = scrapy.Field() #已经销售面积
    unsaled_area = scrapy.Field() #未销售面积
    avg_price = scrapy.Field() #均价

    url = scrapy.Field() #采集房屋的URL
    city = scrapy.Field() #城市
    province = scrapy.Field()  #省份
    crawl_time = scrapy.Field()  #抓取时间


class SzNewhouseItem(scrapy.Item):
    # 苏州
    # 精确到房屋
    project_name = scrapy.Field()  # 项目名称
    project_addr = scrapy.Field()  # 房屋坐落
    company = scrapy.Field()  # 房产公司
    build_type = scrapy.Field()  # 房屋户型
    build_area = scrapy.Field()  # 建筑面积
    price = scrapy.Field()  # 参考单价
    district = scrapy.Field()  # 行政区


class XmNewhouseItem(scrapy.Item):
    # 厦门
    # 精确到房屋
    permit_presale = scrapy.Field()  # 预售证号
    project_name = scrapy.Field()  # 项目名称
    district = scrapy.Field()  # 行政区
    project_addr = scrapy.Field()  # 项目地址
    company = scrapy.Field()  # 房产公司名称
    start_time = scrapy.Field()  # 建筑开始时间
    end_time = scrapy.Field()  # 建筑结束时间
    approve_time = scrapy.Field()  # 得到预售证号时间
    sale_building_num = scrapy.Field()  # 栋号
    house_cate = scrapy.Field()  # 房子是商铺还是住宅还是单列还是车位
    floor = scrapy.Field()  # 房子层数
    house_number = scrapy.Field()  # 单元号
    build_type = scrapy.Field()  # 房子性质(商品房)
    use_for = scrapy.Field()  # 用途
    build_area = scrapy.Field()  # 建筑面积
    price = scrapy.Field()  # 参考单价
    ownership_restriction = scrapy.Field()  # 权属限制
    house_marking = scrapy.Field()
    city = scrapy.Field()


class SyNewhouseItem(scrapy.Item):
    # 沈阳
    # 精确到房屋
    project_name = scrapy.Field() # 楼盘名称
    district = scrapy.Field()   # 行政区
    develop_company = scrapy.Field()   # 开发商
    opening_time = scrapy.Field()  # 开盘时间
    houses_address = scrapy.Field()  # 楼盘地址
    house_marking = scrapy.Field()   # 门牌号
    build_type = scrapy.Field()  # 房屋类型
    build_in_area = scrapy.Field()  # 套内面积
    AVG_area = scrapy.Field()  # 分摊面积
    balcony_area = scrapy.Field()  # 阳台面积
    saled_area = scrapy.Field()  # 销售面积
    build_area = scrapy.Field()   # 建筑面积
    sale_status = scrapy.Field()  # 状态
    url = scrapy.Field()  # 具体页面的url
    city = scrapy.Field()
    province = scrapy.Field()


class NcNewhouseItem(scrapy.Item):
    # 南昌
    # 精确到房屋
    permit_presale = scrapy.Field()  # 预售证号
    project_name = scrapy.Field()  # 项目名称
    project_addr = scrapy.Field()  # 地址
    company = scrapy.Field()  # 房产公司
    approve_time = scrapy.Field()  # 得到预售证号时间
    sale_building_num =scrapy.Field()  # 栋号
    house_number = scrapy.Field()  # 单元号
    build_type = scrapy.Field()  # 户型
    build_area = scrapy.Field()  # 建筑面积
    total_price = scrapy.Field()  # 预售参考价
    sale_status = scrapy.Field()  # 房屋销售状态
    house_orientation = scrapy.Field()  # 房子朝向


class HfNewhouseItem(scrapy.Item):
    # 合肥
    # 精确到房屋
    project_name = scrapy.Field()  # 小区名称
    district = scrapy.Field()   # 行政区
    company = scrapy.Field()   # 开发公司
    opening_time = scrapy.Field()  # 开盘时间
    address = scrapy.Field()  # 房屋地址
    project_addr = scrapy.Field()  # 小区地址
    house_marking = scrapy.Field()   # 房间号
    build_type = scrapy.Field()  # 房屋类型
    build_in_area = scrapy.Field()  # 套内面积
    AVG_area = scrapy.Field()  # 分摊面积
    build_area = scrapy.Field()   # 建筑面积
    sale_status = scrapy.Field()  # 状态
    price = scrapy.Field()
    city = scrapy.Field()
    province = scrapy.Field()
    completion_time = scrapy.Field()   # 竣工日期
    delivery_time = scrapy.Field()   # 交付日期


class NJNewHouseItem(scrapy.Item):
    # 南京
    # 精确到小区
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 开始销售时间
    opening_date = scrapy.Field()
    # 项目名称
    project_name = scrapy.Field()
    # 全部均价
    all_avg_price = scrapy.Field()
    # 房屋均价
    avg_price = scrapy.Field()
    # 写字楼均价
    office_avg_price = scrapy.Field()
    # 商铺均价
    shop_avg_price = scrapy.Field()
    # 可售套数
    house_num = scrapy.Field()
    # url
    url = scrapy.Field()
    # 项目地址
    project_address = scrapy.Field()
    # 用途
    use_for = scrapy.Field()
    # 行政区
    district = scrapy.Field()
    # 开发公司
    develop_company = scrapy.Field()
    # 成交套数
    deal_num = scrapy.Field()
    # 成交面积
    deal_area = scrapy.Field()
    # 可售面积
    can_sale_total_area = scrapy.Field()


class DongGuanItem(scrapy.Item):
    # 东莞
    # 精确到房屋
    project_addr = scrapy.Field() #坐落位置
    project_name = scrapy.Field() #项目名称
    saled_area = scrapy.Field() #销售面积
    build_area = scrapy.Field() #建筑面积
    build_in_area = scrapy.Field() #套内面积
    price = scrapy.Field() #公示单价

    house_marking = scrapy.Field()#房间标识
    use_for = scrapy.Field()#房间用途
    sale_status = scrapy.Field()#销售状态
    back_status = scrapy.Field()#备案状态
    back_cast_status = scrapy.Field()#按揭状态
    close_status = scrapy.Field()#查封状态
    floor = scrapy.Field()#所在楼层
    AVG_area = scrapy.Field()#分摊面积
    total_price = scrapy.Field()#公示价格
    house_url = scrapy.Field()#抓取网页
    crawl_time = scrapy.Field()#抓取时间
    city = scrapy.Field()#城市
    province = scrapy.Field()#省份
    building_name = scrapy.Field()#楼号


class NNItem(scrapy.Item):
    # 南宁
    # 精确到小区
    develop_company = scrapy.Field()  # 开发商
    project_name = scrapy.Field()  # 小区名称
    project_address = scrapy.Field()  # 小区地址
    total_area = scrapy.Field()  # 预售面积
    approve_time = scrapy.Field()  # 批准时间
    doorplate = scrapy.Field()  # 房号
    price = scrapy.Field()  # 预售价格
    area = scrapy.Field()  # 建筑面积
    use_for = scrapy.Field()  # 用途
    house_structure = scrapy.Field()  # 户型


class SanyaItem(scrapy.Item):
    # 三亚
    # 精确到小区
    avg_price = scrapy.Field()  # 单价
    opening_date = scrapy.Field()  # 开盘时间
    loupan_type = scrapy.Field()  # 楼盘类型
    house_type = scrapy.Field()  # 房屋类型
    district = scrapy.Field()  # 行政区划
    plan_area = scrapy.Field()  # 规划面积
    building_area = scrapy.Field()  # 建筑面积
    building_num = scrapy.Field()  # 总栋数
    house_num = scrapy.Field()  # 规划户数
    property_fee = scrapy.Field()  # 物业费
    green_rate = scrapy.Field()  # 绿化率
    volume_rate = scrapy.Field()  # 容积率
    decorate_status = scrapy.Field()  # 装修情况
    project_name = scrapy.Field()  # 楼盘名称
    project_address = scrapy.Field()  # 项目地址
    part_district = scrapy.Field()  # 所属区域
    develop_company = scrapy.Field()  # 开发商
    url = scrapy.Field()  # 小区url

class GuiYangItem(scrapy.Item):
    # 贵阳
    # 精确到小区
    project_name = scrapy.Field() #楼盘名称
    name = scrapy.Field() #楼盘名称
    house_num = scrapy.Field() #住宅总套数
    can_sale_total_area = scrapy.Field() #预售面积
    project_address = scrapy.Field() #坐落地址
    avg_price = scrapy.Field() #合同均价
    house_type = scrapy.Field() #房屋类型
    can_sale_house = scrapy.Field() #可售套数
    url = scrapy.Field()#抓取网页
    crawl_time = scrapy.Field()#抓取时间
    city = scrapy.Field()#城市
    province = scrapy.Field()#省份


class FuzhouItem(scrapy.Item):
    # 福州
    # 精确到房屋
    permission_area = scrapy.Field()  # 许可面积
    sale_building_num = scrapy.Field()  # 预售楼号
    completion_time = scrapy.Field()  # 计划竣工日期
    project_name = scrapy.Field()  # 项目名称
    district = scrapy.Field()  # 所在区县
    project_addr = scrapy.Field()  # 项目地址
    company = scrapy.Field()  # 企业名称
    approve_time = scrapy.Field()  # 批准日期
    building_name = scrapy.Field()  # 楼栋名称
    house_marking = scrapy.Field()  # 室号
    build_type = scrapy.Field()  # 房屋类型
    build_area = scrapy.Field()  # 建筑面积
    build_in_area = scrapy.Field()  # 套内面积
    AVG_area = scrapy.Field()  # 分摊面积
    sale_status = scrapy.Field()  # 状态
    price = scrapy.Field()  # 单价
    total_price = scrapy.Field()  # 总价
    city = scrapy.Field() #城市


class shaoxingItem(scrapy.Item):
    # 绍兴
    # 精确到小区
    # 省份
    province = scrapy.Field()
    # url
    house_url = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 楼盘名称
    project_name = scrapy.Field()
    # 开发商
    company = scrapy.Field()
    # 所属区域
    district = scrapy.Field()
    # 面积范围
    area_range = scrapy.Field()
    # 占地面积
    use_area = scrapy.Field()
    # 建筑面积
    building_area = scrapy.Field()
    # 起价
    start_price = scrapy.Field()
    # 均价
    avg_price = scrapy.Field()
    # 销售装态
    sale_states = scrapy.Field()
    # 物业类型
    property_type = scrapy.Field()
    # 楼层状况
    floor_status = scrapy.Field()
    # 物业公司
    property_company = scrapy.Field()
    # 装修状态
    decorate_status = scrapy.Field()
    # 开盘时间
    start_sale_time = scrapy.Field()
    # 绿化率
    green_rate = scrapy.Field()
    # 容积率
    volume_rate = scrapy.Field()
    # 停车位
    carport = scrapy.Field()
    # 售楼地址
    sale_address = scrapy.Field()
    # 详细地址
    project_address = scrapy.Field()


class HuzhouItem(scrapy.Item):
    #湖州
    # 精确到房屋
    floor = scrapy.Field()  # 楼层
    house_marking = scrapy.Field()  # 房号
    build_area = scrapy.Field()  # 建筑面积
    build_in_area = scrapy.Field()  # 套内面积
    AVG_area = scrapy.Field()  # 分摊面积
    use_for = scrapy.Field()  # 用途
    total_price = scrapy.Field()  # 备案总价(元)
    project_name = scrapy.Field()
    project_addr = scrapy.Field()  # 项目地址
    district = scrapy.Field()  # 所在区域
    approve_time = scrapy.Field()  # 批售日期
    opening_time = scrapy.Field()  # 开盘日期
    completion_time = scrapy.Field()  # 竣工日期
    xq_total_area = scrapy.Field()  # 总共建筑面积
    structure = scrapy.Field()  # 结构
    total_floor = scrapy.Field()  # 总层数
    building_all_area = scrapy.Field()  # 本幢总面积
    all_house_area = scrapy.Field()  # 住宅面积
    all_sale_area = scrapy.Field()  # 可售面积
    total_num = scrapy.Field()  # 本幢总套数
    house_num = scrapy.Field()  # 住宅套数
    sale_house_num = scrapy.Field()  # 可售套数
    url = scrapy.Field()  # 链接地址
    province = scrapy.Field()
    city = scrapy.Field()


class JinHuaItem(scrapy.Item):
    # 金华
    # 精确到小区
    district = scrapy.Field()  # 区域
    plate = scrapy.Field()  # 板块
    license_key = scrapy.Field()  # 预售许可证号
    project_name = scrapy.Field()  # 项目名称
    develop_company = scrapy.Field()  # 开发企业
    opening_time = scrapy.Field()  # 开盘日期
    project_addr = scrapy.Field()  # 项目地址
    publish_place = scrapy.Field()  # 发证机关
    opening_price = scrapy.Field()  # 开盘均价
    approve_time = scrapy.Field()  # 批售日期
    completion_time = scrapy.Field()  # 竣工日期
    sale_building_num = scrapy.Field()  # 楼幢名称
    structure = scrapy.Field()  # 结构
    total_floor = scrapy.Field()  # 总层数
    building_area = scrapy.Field()  # 建筑面积
    avg_price = scrapy.Field()  # 均价
    use_for = scrapy.Field()  # 用途
    # total_floor = scrapy.Field()  # 总层数
    total_house_num = scrapy.Field()  # 套房总数
    internet_pre_sales_total_nums = scrapy.Field()  # 纳入网上预（销）售总套数
    internet_pre_sales_live_nums = scrapy.Field()  # 其中纳入网上预（销）售住房套数
    internet_pre_sales_other_nums = scrapy.Field()  # 纳入网上预（销）售其它套数
    internet_pre_sales_total_areas = scrapy.Field()  # 纳入网上预（销）售总面积
    internet_pre_sales_live_areas = scrapy.Field()  # 其中纳入网上预（销）售住房面积
    internet_pre_sales_other_areas = scrapy.Field()  # 纳入网上预（销）售其它面积
    pre_sales_total_nums = scrapy.Field()  # 可预（销）售总套数
    pre_sales_total_areas = scrapy.Field()  # 可预（销）售总面积
    house_num = scrapy.Field()  # 其中可预（销）售住宅总套数
    can_sale_total_area = scrapy.Field()  # 其中可预（销）售住宅总面积
    deal_num = scrapy.Field()  # 已预（销）售总套数
    deal_area = scrapy.Field()  # 已预（销）售总面积
    preOrder_or_saled_total_AVG_price = scrapy.Field()  # 已预（销）售幢内均价
    preOrdered_nums = scrapy.Field()  # 已预定套数
    preOrdered_areas = scrapy.Field()  # 已预定面积
    limited_nums = scrapy.Field()  # 限制房产总套数
    limited_areas = scrapy.Field()  # 限制房产总面积
    not_in_internet_sales_nums = scrapy.Field()  # 未纳入网上销售房产总套数
    not_in_internet_sales_areas = scrapy.Field()  # 未纳入网上销售房产总面积
    url = scrapy.Field()  # 数据源
    crawl_time = scrapy.Field()#抓取时间
    city = scrapy.Field()#城市
    province = scrapy.Field()#省份


class WuxiItem(scrapy.Item):
    #无锡
    # 精确到小区
    district = scrapy.Field()  # 行政区
    opening_date = scrapy.Field()  # 开盘时间
    house_type = scrapy.Field()  # 主力在售

    delivery_time = scrapy.Field()  # 交付时间
    property_type = scrapy.Field()  # 物业类型
    sale_house_num = scrapy.Field()  # 可售套数
    green_rate = scrapy.Field()  # 绿化率
    agent_company = scrapy.Field()  # 代理公司
    property_fee = scrapy.Field()  # 物业费
    volume_rate = scrapy.Field()  # 容积率
    total_num = scrapy.Field()  # 总套数
    property_company = scrapy.Field()  # 物业公司

    project_name = scrapy.Field()  # 楼盘名称
    project_address = scrapy.Field()  # 地址
    develop_company = scrapy.Field()  # 开发商
    avg_price = scrapy.Field()  # 均价
    province = scrapy.Field()  # 省份
    city = scrapy.Field()  # 城市


class DalianNewhouseItem(scrapy.Item):
    # 精确到小区
    project_name = scrapy.Field()
    develop_company = scrapy.Field()
    project_address = scrapy.Field()
    district = scrapy.Field()
    build_number = scrapy.Field()
    unit_number = scrapy.Field()
    province = scrapy.Field()  # 省份
    city = scrapy.Field()  # 城市
    permit_presale = scrapy.Field()  # 预售证号
    total_house_number = scrapy.Field()  # 总套数
    house_num = scrapy.Field()  # 住宅套数
    un_house_number = scrapy.Field()  # 非住宅套数
    building_area = scrapy.Field()  # 总面积
    house_area = scrapy.Field()  # 住宅面积
    un_house_area = scrapy.Field()  # 非住宅面积
    can_sale_house = scrapy.Field()  # 可售总套数
    unsaledHouse_num = scrapy.Field()  # 可售住宅总套数
    sale_unhouse_number = scrapy.Field()  # 可售非住宅套数
    can_sale_total_area = scrapy.Field()  # 可售总面积
    unsaled_area = scrapy.Field()  # 可售住宅面积
    sale_unhouse_area = scrapy.Field()  # 可售非住宅面积
    url = scrapy.Field()  # 链接
    crawl_time = scrapy.Field() # 抓取时间

class QingdaoNewhouseItem(scrapy.Item):
    #青岛
    # 精确到房屋
    project_name = scrapy.Field()
    company = scrapy.Field()
    project_addr = scrapy.Field()
    district = scrapy.Field()
    sale_building_num = scrapy.Field()  # 楼号
    house_marking = scrapy.Field()  # 房号
    province = scrapy.Field()  # 省份
    city = scrapy.Field()  # 城市
    permit_presale = scrapy.Field()  # 预售证号
    total_price = scrapy.Field()  # 每栋楼每单元的参考价
    floating_range = scrapy.Field()  # 每栋楼每单元可浮动幅度
    sale_house_num = scrapy.Field()  # 每栋楼每单元可售套数
    total_num = scrapy.Field()  # 每栋楼每单元预售套数
    total_number = scrapy.Field()  # 每栋楼每单元总套数

    floor = scrapy.Field()  # 每个房子的楼层
    build_type = scrapy.Field()  # 每个房子的类型(住宅还是其他)
    structure = scrapy.Field()  # 每个房子的结构
    predicted_floor_area = scrapy.Field()  # 每个房子的预测建筑面积
    build_area = scrapy.Field()  # 每个房子的实测建筑面积
    predicted_inner_area = scrapy.Field()  # 每个房子的预测套内面积
    build_in_area = scrapy.Field()  # 每个房子的实测套内面积
    predicted_area = scrapy.Field()  # 每个房子的预测分摊面积
    AVG_area = scrapy.Field()  # 每个房子的实测分摊面积
    predicted_underground_area = scrapy.Field()  # 每个房子的预测地下面积
    measured_underground_area = scrapy.Field()  # 每个房子的实测地下面积
    house_marking = scrapy.Field()


class TianjinItem(scrapy.Item):
    # 精确到小区
    house_type = scrapy.Field()  # 计划种类
    decorate_status = scrapy.Field()  # 装修状况
    volume_rate = scrapy.Field()  # 容积率
    green_rate = scrapy.Field()  # 绿化率
    structure = scrapy.Field()  # 建筑结构
    district = scrapy.Field()  # 行政区
    property_fee = scrapy.Field()  # 物业费
    property_company = scrapy.Field()  # 物业公司
    property_type = scrapy.Field()  # 物业类型
    project_name = scrapy.Field()  # 楼盘名称
    opening_date = scrapy.Field()  # 开盘时间
    avg_price = scrapy.Field()  # 住宅均价
    nothouse_avg_price = scrapy.Field()  # 非住宅均价
    building_area = scrapy.Field()  # 建筑总面积
    develop_company = scrapy.Field()  # 开发商
    part_district = scrapy.Field()  # 区域
    project_address = scrapy.Field()  # 地址
    province = scrapy.Field()  # 省份
    city = scrapy.Field()  # 城市
    url = scrapy.Field()  # 链接
    crawl_time = scrapy.Field()  # 抓取时间


class ShanghaiItem(scrapy.Item):
    #上海
    # 精确到房屋
    province = scrapy.Field()  # 省份
    city = scrapy.Field()  # 城市
    url = scrapy.Field()  # 链接
    crawl_time = scrapy.Field()  # 抓取时间

    project_name = scrapy.Field()  # 项目名称
    sale_status = scrapy.Field()  # 状态
    project_total_house_num = scrapy.Field()  # 项目总套数
    total_area = scrapy.Field()  # 项目总面积
    district = scrapy.Field()  # 行政区
    permit_presale = scrapy.Field()  # 预售许可证/房地产权证
    opening_time = scrapy.Field()  # 开盘时间
    total_num = scrapy.Field()  # 楼栋总套数
    xq_house_num = scrapy.Field()  # 楼栋总住宅套数
    all_house_area = scrapy.Field()  # 楼栋总住宅面积
    building_all_area = scrapy.Field()  # 楼栋总面积
    # sale_status = scrapy.Field()
    building_name = scrapy.Field()  # 楼栋名称
    max_price = scrapy.Field()  # 最高报价
    min_price = scrapy.Field()  # 最低报价
    total_price = scrapy.Field()  # 参考价
    house_marking = scrapy.Field()  # 室号
    structure = scrapy.Field()  # 房型
    floor = scrapy.Field()  # 楼层
    AVG_area = scrapy.Field()  # 实测分摊面积
    build_in_area = scrapy.Field()  # 实测套内面积
    build_area = scrapy.Field()  # 实测建筑面积
    build_type = scrapy.Field()  # 房屋类型

