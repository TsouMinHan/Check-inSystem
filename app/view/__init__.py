from flask import Blueprint, url_for

main = Blueprint('main', __name__)

from . import index, login, profile, roll_call, create_account, show_record, edit_record, create_course