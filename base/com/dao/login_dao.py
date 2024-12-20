from base import db
from base.com.vo.login_vo import LoginVO


class LoginDAO:
    def insert_login(self, login_vo):
        db.session.add(login_vo)
        db.session.commit()

    def view_login(self):
        login_vo_list = LoginVO.query.all()
        return login_vo_list

    def delete_login(self, login_vo):
        login_vo_list = LoginVO.query.get(login_vo.login_id)
        db.session.delete(login_vo_list)
        db.session.commit()

    def check_login_username(self, login_vo):
        login_vo_list = LoginVO.query.filter_by(
            login_username=login_vo.login_username).all()
        return login_vo_list

    def find_login_id(self, login_vo):
        login_vo_list = \
        LoginVO.query.filter_by(login_username=login_vo.login_username).all()[
            -1].login_id
        return login_vo_list
