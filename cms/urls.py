# coding:utf-8
from django.urls import path,re_path,reverse
import cms.views as cms_view



urlpatterns=[
    path('',cms_view.cms_index,name='cms_index'),
    path('test/',cms_view.cms_test,name='cms_test'),
    path('login/',cms_view.cms_login,name='cms_login'),
    path('logout/',cms_view.cms_logout,name='cms_logout'),
    path('create_user/',cms_view.cms_create_user,name='cms_create_user'),
    path('profile/',cms_view.cms_profile,name='cms_profile'),
    path('profile_reset_pwd/',cms_view.ResetPwdView.as_view(),name='cms_profile_reset_pwd'),
    path('profile_reset_email/',cms_view.ResetEmailView.as_view(),name='cms_profile_reset_email'),
    path('send_mail/',cms_view.cms_send_email,name='cms_send_mail'),
    path('user_manage/',cms_view.cms_user_manage,name='cms_user_manage'),
    path('black/',cms_view.cms_black,name='cms_black'),
    path('post_manage/<int:page>/',cms_view.cms_post_manage,name='cms_post_manage'),
    path('post_manage_pub/',cms_view.CMSPublishPostView.as_view(),name='cms_post_manage_pub'),
    path('add_tag/',cms_view.cms_add_tag,name='cms_add_tag'),
    path('post_manage_edit/<str:article_id>/',cms_view.CMSEditPostView.as_view(),name='cms_post_manage_edit'),
    path('post_manage_delete/<str:article_id>/',cms_view.cms_post_manage_delete,name='cms_post_manage_delete'),

]