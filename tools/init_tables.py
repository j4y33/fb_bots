from database.bot_sql import BotSql


def tables():
    sql = BotSql()
    sql.create_bot_table()


tables()