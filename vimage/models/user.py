# -*- coding: utf-8 -*-
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

from vimage import db, login_manager
from vimage.helpers.utils import timestamp, MixGenId

__all__ = [
    'User',
    'AnonymousUser'
]


class User(UserMixin, db.Model):
    """User model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    sn = db.Column(db.String(11), unique=True, index=True, nullable=True)

    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # 是否已验证
    confirmed = db.Column(db.Boolean, default=False)

    # 系统默认管理员
    is_admin = db.Column(db.Boolean, default=False)

    # 真实资料信息
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.Integer, default=timestamp)
    avatar = db.Column(db.String(200))
    mobile = db.Column(db.String(20))
    description = db.Column(db.String(140))

    # 本地化
    locale = db.Column(db.String(4), default='zh')
    language = db.Column(db.String(4), default='en')
    time_zone = db.Column(db.String(20), nullable=False)
    # disabled at the time
    disabled_at = db.Column(db.Integer, default=0)
    # if online or offline
    online = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.Integer, default=timestamp)
    
    created_at = db.Column(db.Integer, default=timestamp)
    # update time of last time
    update_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        """生成一个令牌，有效期默认为一小时."""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    @property
    def is_master(self):
        """是否为主账号"""
        return self.master_uid == 0
    
    def is_adminstractor(self):
        """判断用户是否具有管理员权限"""
        return self.is_admin

    def confirm(self, token):
        """检验令牌，如果检验通过，则把新添加的confirmed 属性设为True."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception as err:
            current_app.logger.warn('验证用户确认token失败： %s！' % str(err))
            return False

        if data.get('confirm') != self.id:
            return False

        # 更新状态
        self.confirmed = True

        db.session.add(self)
        db.session.commit()

        return True

    def ping(self):
        """每次收到用户的请求时都要调用ping()方法"""
        last_online = self.online
        
        self.last_seen = timestamp()
        self.online = True
        
        db.session.add(self)
        
        return last_online != self.online

    # API基于令牌的认证
    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id})
    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        
        return User.query.get(data['id'])

    def g_avatar(self, size):
        """user avatar"""
        return 'http://www.gravatar.com/avatar/' + md5(self.email.encode('utf8')).hexdigest() + '?d=mm&s=' + str(size)

    @staticmethod
    def make_unique_username(username):
        if User.query.filter_by(username=username).first() is None:
            return username
        version = 2
        while True:
            new_username = username + str(version)
            if User.query.filter_by(username=new_username).first() is None:
                break
            version += 1
        return new_username
    
    @staticmethod
    def make_unique_sn():
        """生成用户编号"""
        sn = MixGenId.gen_user_xid(length=10)
        if User.query.filter_by(sn=sn).first() is None:
            return sn
        
        while True:
            new_sn = MixGenId.gen_user_xid(length=10)
            if User.query.filter_by(sn=new_sn).first() is None:
                break
        return new_sn

    @staticmethod
    def on_before_insert(mapper, connection, target):
        # 自动生成用户编号
        target.sn = User.make_unique_sn()

    @staticmethod
    def find_offline_users():
        """查找离线用户"""
        users = User.query.filter(User.last_seen < timestamp() - 60,
                                  User.online == True).all()
        # 设置用户离线状态
        for user in users:
            user.online = False
            db.session.add(user)
    
        db.session.commit()
    
        return users

    @staticmethod
    def find_by_openid(openid):
        """通过openid查找用户"""
        return User.query.filter_by(openid=openid).first()

    def to_json(self):
        """资源和JSON的序列化转换"""
        json_user = {
            'uid': self.sn,
            'username': self.username,
            'email': self.email,
            'master_uid': self.master_uid,
            'last_seen': self.last_seen,
            'avatar': self.avatar,
            'name': self.name,
            'mobile': self.mobile,
            'about_me': self.about_me,
            'description': self.description
        }
        return json_user

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    locale = None

    def belong_roles(self):
        return []

    @property
    def is_setting(self):
        return False

    @property
    def is_master(self):
        """是否为主账号"""
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    """使用指定的标识符加载用户"""
    return User.query.get(int(user_id))


# 监听事件
db.event.listen(User, 'before_insert', User.on_before_insert)