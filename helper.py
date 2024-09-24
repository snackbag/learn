import hashlib
import secrets
import time

import database as db

from flask import render_template, flash, session
from sqlalchemy import func


def millis() -> int:
    """
    :return: Returns the current time in milliseconds
    """
    return round(time.time() * 1000)


def has_keys(keys: list, check: dict) -> bool:
    return all(key in check for key in keys)


def create_password(original: str) -> list[str]:
    salt = secrets.token_hex(16)
    salted_password = salt + original
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()

    return [salt, hashed_password]


def verify_password(salt: str, hashed_password: str, input_password: str) -> bool:
    salted_input_password = salt + input_password
    hashed_input_password = hashlib.sha256(salted_input_password.encode()).hexdigest()

    return hashed_input_password == hashed_password


def register_checks(email, username, password, i18n, fallback):
    if len(email) < 8 or len(email) > 50:
        return True, "Email must be between 8 and 50 characters long"

    if len(username) < 4 or len(username) > 26:
        return True, "Username must be between 4 and 26 characters long"

    if len(password) < 8 or len(password) > 50:
        return True, "Password must be between 8 and 50 characters long"

    email_query = db.session.query(db.User).filter(
        func.lower(db.User.email) == func.lower(email),
        db.User.account_type != 2
    ).first()

    if email_query is not None:
        flash(i18n("error.exists.email"))

    username_query = db.session.query(db.User).filter(
        func.lower(db.User.username) == func.lower(username),
        db.User.account_type != 2
    ).first()

    if username_query is not None:
        flash(i18n("error.exists.username"))

    if username_query is not None or email_query is not None:
        return True, render_template(fallback, i18n=i18n)

    return False, None


def login(email: str, password: str, account_type: int, user_id_cache, i18n, fallback: str):
    if len(email) < 8 or len(email) > 50:
        return True, "Email must be between 8 and 50 characters long"

    if len(password) < 8 or len(password) > 50:
        return True, "Password must be between 8 and 50 characters long"

    email_query = db.session.query(db.User).filter(
        func.lower(db.User.email) == func.lower(email),
        db.User.account_type == account_type
    ).first()

    if email_query is None:
        flash(i18n("error.notfound.user"))
        return True, render_template(fallback, i18n=i18n)

    if not verify_password(email_query.salt, email_query.password, password):
        flash(i18n("error.notfound.user"))
        return True, render_template(fallback, i18n=i18n)

    session['user_id'] = str(email_query.user_id)
    user_id_cache.cache(email_query)

    return False, None
