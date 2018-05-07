from django.db import models
import django.utils.timezone as timezone


class District(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Customers(models.Model):
    CATEGORY_CHOICES=(
        ('JXS', '经销商'),
        ('ZHD', '终端'),
        ('CHL', '车辆')
    )
    name = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=100, unique=True)
    category = models.CharField(choices=CATEGORY_CHOICES, default='JXS')
    # 客户区域，删除区域时提示错误，需要先调整区域再删除；todo:暂时设置为可以为空
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    key_person = models.CharField(verbose_name='联系人', max_length=50, null=True, blank=True)
    # todo:电话号码格式完善
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.nickname


class Supplier(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class GoodsCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Goods(models.Model):
    bar_code = models.IntegerField(null=True, blank=True, unique=True,)
    name = models.CharField(max_length=200,unique=True)
    nickname = models.CharField(max_length=100, unique=True)
    # todo: category外键GoodsCategory_name
    category = models.ForeignKey(GoodsCategory,on_delete=models.PROTECT)
    # todo : 外键Supplier_name
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True)
    # todo:打款价格暂时可以为空
    price_buy = models.FloatField(verbose_name='打款价格', null=True, blank=True)
    # todo:分销价格暂时可以为空
    price_distribution = models.FloatField(verbose_name='分销价格', null=True, blank=True)
    # todo: 进店价格暂时可以为空
    price_sell = models.FloatField(verbose_name='进店价格', null=True, blank=True)
    unit = models.CharField(verbose_name='单位', max_length=50, default='件')
    specification = models.CharField(verbose_name='规格', max_length=100, default='500ml*12')

    def __str__(self):
        return self.nickname


class Purchasing(models.Model):
    # todo:生成采购编号
    # models.DO_NOTHING如果商品删除了，历史订单不受影响
    name = models.ForeignKey(Goods, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    date = models.DateField(default=timezone.now)
    is_received = models.BooleanField(default=False)
    date_received = models.DateField(null=True, blank=True)

    # 如果收货，自动把'is_received'设为True,把'date_received'设为当前日期
    def receive_goods(self):
        pass

    def __str__(self):
        return self.name


class Sales(models.Model):
    # todo:自动生成订单编号
    customer = models.ForeignKey(to=Customers, on_delete=models.DO_NOTHING)
    goods = models.ManyToManyField(Goods)
    quantity = models.IntegerField()
    payment = models.FloatField(verbose_name='金额')
    date_pay = models.DateField(default=timezone.now, null=True, blank=True)
    is_payed = models.BooleanField(default=True)

    # todo:如果结账，自动设置结账日期为今天
    def is_payed(self):
        pass

    def __str__(self):
        return self.customer


class Inventory(models.Model):
    name = models.ForeignKey(Goods, on_delete=models.DO_NOTHING)
    book_inventory = models.FloatField(verbose_name='账面库存')
    physical_inventory = models.FloatField(verbose_name='实际库存')

    def __str__(self):
        return self.name

