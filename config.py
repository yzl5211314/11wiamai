class Config():
    BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'

    SECRET_KEY = 'dasdsadasdas'

    # 设置连接数据库的URL
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123@127.0.0.1:3306/db_11_waimai'

    # 数据库和模型类同步修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True


    #密钥
    APP_SECRET = '25ad4785212d2caf95822d76246e5e6d'
    APP_ID = 'wxbe2170fce5fc80fc'

    MCH_ID = '13145211314'#商户号id

    PAYKEY = 'dsadsadas'

    DOMAIN = 'http://127.0.0.1:5000'

    CALLBACK_URL = '/api/v1/order/callback'


    STATIC_D = 'http://127.0.0.1:5000/static/'

    IGNORE_URLS = ['/api/v1/member/login',
                   '/api/v1/member/cklogin',
                   '/api/v1/food/search',
                   '/api/v1/food/all',
                   '/api/v1/food/info']



# 线上环境
class ProductingConfig(Config):
    DEBUG = False


# 生产环境
class DevelopmentConfig(Config):
    DEBUG = True


mapping_config = {
    'pro': ProductingConfig,
    'dev': DevelopmentConfig,
}
