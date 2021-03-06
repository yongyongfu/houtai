# coding=utf-8

from sqlalchemy import func
from flask import request, render_template, redirect, url_for, flash, current_app, session
from flask_user import login_required, roles_required, current_user
from flask_admin import Admin, expose
from flask_admin.form import rules
from flask_admin.actions import action
from flask_admin.model.template import EndpointLinkRowAction, LinkRowAction

# db
from app.database import db, Column, reference_col, relationship

# model
from app.models.user import SexEnum
from app.models import User, Role

# flask admin base mode view
from .base_view import CustomBaseModelView

# cache
from app.cache import cache

##########################################################################
# amdin model view


class UsersModelView(CustomBaseModelView):
    """Users Model View"""
    can_create = True
    can_delete = False
    can_view_details = True

    column_display_pk = False

    column_list = (
        User.username,
        User.nickname,
        User.sex,
        User.phone,
        User.email,
        User.active,
    )

    column_labels = {
        "username": u"用户名",
        "email": u"邮箱",
        "nickname": u"昵称",
        "group": u"用户组",
        "groups": u"用户组",
        "roles": u"角色",
        "phone": u"手机号码",
        "sex": u"性别",
        "active": u"激活",
        "create_datetime": u"创建时间",
        "current_login_datetime": u"本次登录时间",
        "last_login_datetime": u"上次登录时间",
        "current_login_ip": u"本次登录IP",
        "last_login_ip": u"上次登录IP",
        "api_key": u"API密钥",
    }

    # column_choices = {
    #     'sex': [
    #         (SexEnum.male, u"男"),
    #         (SexEnum.female, u"女"),
    #         (SexEnum.other, u"其他"),
    #         (SexEnum.empty, u"未填"),
    #     ]
    # }

    column_searchable_list = ("username", )

    # 不显示password
    column_exclude_list = ("password_hash", "password", "avatar_hash")

    # 在表单中排除相关的字段
    form_excluded_columns = (
        # "username",
        # "email",
        # "phone",
        "password_hash",
        "avatar_hash",
        "api_key",
    )

    # 表单参数
    form_widget_args = {
        'username': {
            'disabled': True  # 禁止修改
        },
        "password_hash": {
            'disabled': True
        },
    }

    # @cache.cached(60, key_prefix='user_admin_view_get_query')
    def get_query(self):
        return super(UsersModelView, self).get_query()

    # @cache.cached(60)
    def get_count_query(self):
        return super(UsersModelView, self).get_count_query()

    # def get_one(self, id):
    #     prefix = "user"
    #     if self.model.has_cache(prefix, id):
    #         current_app.logger.debug("get model form CACHE: id={}".format(id))
    #         return self.model.get_cache_by_id(prefix, id)
    #     current_app.logger.debug("get model form DATABASE: id={}".format(id))
    #     model = super(UsersModelView, self).get_one(id)
    #     model.add_cache(prefix)  # add cache
    #     return model


class RolesModelView(CustomBaseModelView):
    """
    Roles Model View
    """
    can_create = True
    can_delete = True
    can_edit = True
    can_view_details = False

    column_labels = {"name": u"角色名称", "description": u"描述"}

    # action_disallowed_list = ["delete"]


def init_admin_view(admin: Admin):
    admin.add_view(UsersModelView(User, db.session, name=u"用户",
                                  endpoint="users", menu_icon_type="glyph",
                                  menu_icon_value="glyphicon-user",
                                  category="用户管理"))
    admin.add_view(RolesModelView(
        Role, db.session, name=u"角色", endpoint="roles", category="用户管理"))
