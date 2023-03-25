from datetime import datetime
from psycopg2 import sql
from database.connector import DbConnector


class BotSql(DbConnector):
    def __init__(self):
        super().__init__()

    # Logs
    def insert_log(self, bot, text):
        query = "INSERT INTO logs (bot_id, log, date) " \
                "VALUES (%s, %s, %s);"
        data = (bot[0], text, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.cursor.execute(query, data)
        self.connection.commit()

    # Tracks
    def insert_track(self, bot, action_id, running_percent):
        query = "INSERT INTO tracks (bot_id, track, date) " \
                "VALUES (%s, %s, %s);"
        data = (bot[0], [[action_id, str(running_percent), datetime.now().strftime('%Y-%m-%d %H:%M:%S')]], datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
        self.cursor.execute(query, data)
        self.connection.commit()

    def update_track(self, bot, action_id, running_percent):
        query = """update tracks set track = track || %s
        where bot_id = '{0}' and id = (select max(id) from tracks);""".format(bot[0])
        data = [[action_id, str(running_percent), datetime.now().strftime('%Y-%m-%d %H:%M:%S')]]
        self.cursor.execute(query, (data,))
        self.connection.commit()

    # Campaigns DST
    def get_campaign_destination_lists(self, bot_id):
        query = """SELECT * from destination_lists where '{0}' = ANY(profiles);""".format(bot_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_campaigns(self, dst_id):
        query = """SELECT * from campaigns where '{0}' = ANY(dst_lists);""".format(dst_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_campaigns_post_by_camp_id(self, bot_id, campaign_id):
        query = """SELECT * from campaigns_posts where ((array_length(posted, 1) < published_by
        and not '{0}' = ANY(posted)) or (posted IS NULL)) and campaign_id = {1} LIMIT 1;""".format(bot_id, campaign_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_scraped_post(self, campaign_id, link):
        query = """SELECT * from campaigns_scraped_posts where campaign_id = {0} 
        and url = '{1}' LIMIT 1;""".format(campaign_id, link)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_campaigns_scrap_and_share_posts(self, campaign_id):
        query = """SELECT * from campaigns_scrap_and_share_posts where campaign_id = {0};""".format(campaign_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def update_scraped_post_group(self, bot_id, group_url, post_id):
        query = """update campaigns_scraped_posts set shared_bots = array_cat(shared_bots, '{0}'), 
        shared_groups = array_cat(shared_groups, '{1}')
        where id = {2};""".format('{'+str(bot_id)+'}', '{'+str(group_url)+'}', post_id)
        self.cursor.execute(query)
        self.connection.commit()

    def add_scraped_post(self, url, campaign_id, screen):
        query = """SELECT * from campaigns_scraped_posts WHERE url = '{0}' AND campaign_id = {1} LIMIT 1;""".format(url, campaign_id)
        self.cursor.execute(query)
        check = self.cursor.fetchone()
        if check is None:
            query = "INSERT INTO campaigns_scraped_posts (url, campaign_id, screen, date) " \
                    "VALUES (%s, %s, %s, %s);"
            data = (url, campaign_id, screen, datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
            self.cursor.execute(query, data)
            self.connection.commit()
            return True
        else:
            return False

    def add_liked_post(self, bot_id, url, campaign_id, screen):
        query = "INSERT INTO campaigns_liked_posts (bot_id, url, campaign_id, screen, date) " \
                "VALUES (%s, %s, %s, %s, %s);"
        data = (bot_id, url, campaign_id, screen, datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
        self.cursor.execute(query, data)
        self.connection.commit()
    # Working here
    def update_liked_post(self, bot_id, id):
        query = """update campaigns_liked_posts set liked_bots = array_cat(liked_bots, '{0}')
        where id = {1};""".format('{'+str(bot_id)+'}', id)
        self.cursor.execute(query)
        self.connection.commit()

    def check_shared_posts(self, bot, campaign_id):
        query = """SELECT * from campaigns_scraped_posts WHERE 
        (not '{0}' = ANY(shared_bots) or (shared_bots IS NULL)) AND campaign_id = {1} ; LIMIT 1;""".format(bot, campaign_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def check_shared_text(self, text, post_id):
        query = """SELECT * from campaigns_scraped_posts WHERE id = {0} ;""".format(post_id)
        self.cursor.execute(query)
        check = self.cursor.fetchone()
        if check[6] is None:
            return True
        elif text not in check[6]:
            return True
        else:
            return False

    def update_shared_text(self, shared_text, post_id):
        query = """SELECT * from campaigns_scraped_posts WHERE id = {0} ;""".format(post_id)
        self.cursor.execute(query)
        check = self.cursor.fetchone()
        if check[6] is None:
            query = """update campaigns_scraped_posts set
            shared_text = '{0}'
            where id = {1};""".format(shared_text, post_id)
            self.cursor.execute(query)
            self.connection.commit()
        else:
            query = """update campaigns_scraped_posts set
            shared_text = '{0}'
            where id = {1};""".format(check[6]+'|'+str(shared_text), post_id)
            self.cursor.execute(query)
            self.connection.commit()

    def get_campaigns_posts_by_id(self, id, bot_id):
        query = """SELECT * from campaigns_posts where id = {0}
        and not '{1}' = ANY(posted) or (posted IS NULL);""".format(id, bot_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def check_campaigns_posts_group(self, id, group_id):
        query = """SELECT * from campaigns_posts where id = {0}
        and not '{1}' = ANY(posted_groups) or (posted_groups IS NULL);""".format(id, group_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def check_campaigns_posts_walls(self, id, bot_id):
        query = """SELECT * from campaigns_posts where id = {0}
        and not '{1}' = ANY(posted_walls) or (posted_walls IS NULL);""".format(id, bot_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_campaigns_posts(self, bot_id):
        query = """SELECT * from campaigns_posts where (array_length(posted, 1) < published_by
        and not '{0}' = ANY(posted)) or (posted IS NULL) LIMIT 1 FOR UPDATE SKIP LOCKED;""".format(bot_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def remove_campaigns_posts_bot_running_status(self, bot_id, post_id):
        query = """update campaigns_posts set running = array_remove(running, '{0}') 
        where id = {1};""".format('{' + bot_id + '}', post_id)
        self.cursor.execute(query)
        self.connection.commit()

    def update_campaigns_posts_status(self, status, post_id):
        query = """update campaigns_posts set status = '{0}' 
        where id = {1};""".format(status, post_id)
        self.cursor.execute(query)
        self.connection.commit()

    def update_posted_walls(self, bot_id, post_id):
        query = """update campaigns_posts set posted_walls = array_cat(posted_walls, '{0}')
        where id = {1};""".format('{'+str(bot_id)+'}', post_id)
        self.cursor.execute(query)
        self.connection.commit()

    def update_posted_groups(self, group_id, post_id):
        query = """update campaigns_posts set posted_groups = array_cat(posted_groups, '{0}')
        where id = {1};""".format('{'+str(group_id)+'}', post_id)
        self.cursor.execute(query)
        self.connection.commit()

    def update_campaigns_errors(self, post_id):
        query = """SELECT campaign_id from campaigns_posts WHERE id = {0};""".format(post_id)
        self.cursor.execute(query)
        campaign_id = self.cursor.fetchone()
        print(campaign_id[0])
        query = """update campaigns set errors = array_cat(errors, '{0}')
        where id = {1};""".format('{'+str(post_id)+'}', campaign_id[0])
        self.cursor.execute(query)
        self.connection.commit()

    def update_campaigns_posts(self, bot_id, post_id):
        query = """update campaigns_posts set posted = array_cat(posted, '{0}') 
        where id = {1};""".format('{' + bot_id + '}', post_id)
        self.cursor.execute(query)
        self.connection.commit()

        query = """SELECT array_length(posted, 1), published_by from campaigns_posts where id = {0}""".format(post_id)
        self.cursor.execute(query)
        content = self.cursor.fetchone()
        if content[0] >= content[1]:
            query = """update campaigns_posts set status = 'done' where id = {0};""".format(post_id)
            self.cursor.execute(query)
            self.connection.commit()

    # Bot
    def update_bot_instance_details(self, bot, local_ip, public_ip, instance_id):
        query = """update bots set local_ip = '{0}', public_ip = '{1}', instance_id = '{2}' 
        where login = '{3}';""".format(local_ip, public_ip, instance_id, bot)
        self.cursor.execute(query)
        self.connection.commit()

    def check_bot_exist(self, bot_first_name, bot_last_name):
        query = """SELECT * from bots WHERE bot_first_name = '{0}' AND bot_last_name = '{0}';""".format(bot_first_name,
                                                                                                        bot_last_name)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def check_bot_used_time(self, login, time_range):
        query = """SELECT last_used_date from bots WHERE login = '{0}' 
        AND last_used_date < current_timestamp - interval '{1} minutes';""".format(login, time_range)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def add_bot(self, bot):
        # block_status: blocked before login, blocked after scraping, active
        columns = (
            'login', 'password', 'vpn_provider', 'vpn_region', 'vpn_login', 'vpn_password', 'cookies', 'used_status',
            'block_status', 'bot_first_name', 'bot_last_name', 'bot_gender', 'bot_birth_day', 'bot_birth_month',
            'bot_birth_year', 'user_agent', 'screen', 'city', 'school', 'university', 'job', 'profile_picture',
            'bot_images_list', 'creation_date', 'last_used_date', 'total_friends', 'scraped_profiles',
            'total_actions', 'total_errors', 'proxy')
        query_string = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier('bots'),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(bot)),
        ).as_string(self.cursor)
        self.cursor.execute(self.cursor.mogrify(query_string, bot))
        self.connection.commit()

    def update_screen_size(self, login, size):
        query = """UPDATE bots SET screen = '{0}' WHERE login = '{1}';""".format(size, login)
        self.cursor.execute(query)
        self.connection.commit()

    def update_user_agent(self, login, ua):
        query = """UPDATE bots SET user_agent = '{0}' WHERE login = '{1}';""".format(ua, login)
        self.cursor.execute(query)
        self.connection.commit()

    def update_bot_block_status(self, login, status):
        query = """UPDATE bots SET block_status = '{0}' WHERE login = '{1}';""".format(status, login)
        self.cursor.execute(query)
        self.connection.commit()

    def update_bot_errors(self, login):
        query_count = """SELECT total_errors from bots WHERE login = '{0}';""".format(login)
        self.cursor.execute(query_count)
        count = self.cursor.fetchone()[0] + 1
        query = """UPDATE bots SET total_errors = '{0}' WHERE login = '{1}';""".format(count, login)
        self.cursor.execute(query)
        self.connection.commit()

    def update_bot_picture(self, login, profile_picture):
        query = """UPDATE bots SET profile_picture = '{0}' WHERE login = '{1}';""".format(profile_picture, login)
        self.cursor.execute(query)
        self.connection.commit()

    def update_bot_cookies(self, login, cookies):
        query = """UPDATE bots SET cookies = '{0}' WHERE login = '{1}';""".format(cookies, login)
        self.cursor.execute(query)
        self.connection.commit()

    def update_bot_used_status(self, login, status):
        query = """UPDATE bots SET used_status = {0} WHERE login = '{1}';""".format(status, login)
        self.cursor.execute(query)
        self.connection.commit()

    def update_bot_vpn_region(self, login, region):
        query = """UPDATE bots SET vpn_region = '{0}' WHERE login = '{1}';""".format(region, login)
        self.cursor.execute(query)
        self.connection.commit()

    def update_bot_last_used_date(self, login):
        query = """UPDATE bots SET last_used_date = '{0}' WHERE login = '{1}';""".format(
            datetime.now().strftime('%Y-%m-%d_%H:%M:%S'), login)
        self.cursor.execute(query)
        self.connection.commit()

    def update_bot_scraped_profiles(self, login, count):
        query = """UPDATE bots SET scraped_profiles = {0} WHERE login = '{1}';""".format(count, login)
        self.cursor.execute(query)
        self.connection.commit()

    def get_bot(self):
        query = """SELECT * from bots WHERE used_status = False AND block_status = 'active' 
                  AND total_errors < 3
                  AND last_used_date < current_timestamp - interval '3 hours' LIMIT 1 FOR UPDATE SKIP LOCKED;"""
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_bot_test(self):
        query = """SELECT * from bots WHERE login = '+79913971829' LIMIT 1;"""
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_bot_campaign(self, bot):
        query = """SELECT * from bots WHERE login = '{0}' LIMIT 1;""".format(bot)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_bot_creation_date(self):
        query = """SELECT * from bots WHERE used_status = False AND block_status = 'active' 
                  AND creation_date < current_date - 2 LIMIT 1 FOR UPDATE SKIP LOCKED;"""
        self.cursor.execute(query)
        return self.cursor.fetchone()

    # Actions
    def add_action(self, bot_id, action_priority, action_id, action_status, image):
        query = "INSERT INTO action (bot_id, action_priority, action_id, action_status, image, date) " \
                "VALUES (%s, %s, %s, %s, %s, %s);"
        data = (bot_id, action_priority, action_id, action_status, image, datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
        self.cursor.execute(query, data)
        self.connection.commit()

    def get_actions(self, bot, wait_period_for_action):
        query = """SELECT * from action WHERE bot_id = '{0}'
        AND date > (NOW() - INTERVAL '{1} hours' ) AND action_id != 'login';""".format(bot, wait_period_for_action)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_like_actions(self, bot, wait_period_for_action):
        query = """SELECT * from action WHERE bot_id = '{0}'
        AND date > (NOW() - INTERVAL '{1} minutes' ) AND action_id != 'login';""".format(bot, wait_period_for_action)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_profile_actions(self, bot):
        query = """SELECT * from action WHERE bot_id = '{0}'
                                              AND action_priority = 'profile';""".format(bot)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def last_actions(self, bot):
        query = """SELECT * from action WHERE bot_id = '{0}' LIMIT 20;""".format(bot)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # Friends
    def add_friend(self, bot_id, link, status):
        query = "INSERT INTO friends (bot_id, friend_link, status, date) VALUES (%s, %s, %s, %s);"
        data = (bot_id, link, status, datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
        self.cursor.execute(query, data)
        self.connection.commit()

    def get_friends(self, bot):
        query = """SELECT * from friends WHERE bot_id = '{0}';""".format(bot)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # Following
    def add_follow_page(self, bot_id, link):
        query = """SELECT * from following WHERE bot_id = '{0}' and link = '{1}';""".format(bot_id, link)
        self.cursor.execute(query)
        check = self.cursor.fetchone()
        if check is None:
            query = "INSERT INTO following (bot_id, link, date) VALUES (%s, %s, %s);"
            data = (bot_id, link, datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
            self.cursor.execute(query, data)
            self.connection.commit()

    def count_follow_pages(self, bot_id):
        query = """SELECT count(*) from following WHERE bot_id = '{0}';""".format(bot_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_follow(self, bot_id):
        query = """SELECT * from following WHERE bot_id = '{0}';""".format(bot_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # Groups
    def add_group_page(self, bot_id, link, group_name, status, screen):
        query = """SELECT * from groups WHERE bot_id = '{0}' and link = '{1}';""".format(bot_id, link)
        self.cursor.execute(query)
        check = self.cursor.fetchone()
        # Check if None and check if pennding, if it's parser, change status
        if check is None:
            query = "INSERT INTO groups (bot_id, link, group_name, status, dst_select_status, screen, date) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s);"
            data = (bot_id, link, group_name, status, False, screen, datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
            self.cursor.execute(query, data)
            self.connection.commit()
        else:
            query = """UPDATE groups SET status = '{0}' WHERE bot_id = '{1}' and link = '{2}';""".format(status, bot_id, link)
            self.cursor.execute(query)
            self.connection.commit()

    def count_groups_pages(self, bot_id):
        query = """SELECT count(*) from groups WHERE bot_id = '{0}';""".format(bot_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_groups(self, bot_id):
        query = """SELECT * from groups WHERE bot_id = '{0}' and dst_select_status = True;""".format(bot_id) # dst_select_status = True
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def check_group(self, bot_id, link):
        query = """SELECT * from groups WHERE bot_id = '{0}' 
        and dst_select_status = True 
        and link = '{1}';""".format(bot_id, link) # dst_select_status = True
        self.cursor.execute(query)
        return self.cursor.fetchone()

    # Errors
    def add_error(self, bot_id, e, image):
        query = "INSERT INTO errors (bot_id, error, image, date) VALUES (%s, %s, %s, %s);"
        data = (bot_id, e, image, datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
        self.cursor.execute(query, data)
        self.connection.commit()

    def last_errors(self, bot_id):
        query = """SELECT * from errors WHERE bot_id = '{0}' LIMIT 20;""".format(bot_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # Images
    def add_image(self, bot_id, gender, profile, link):
        query = "INSERT INTO images (bot_id, gender, profile, image, date) VALUES (%s, %s, %s, %s, %s);"
        data = (bot_id, gender, profile, link, datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
        self.cursor.execute(query, data)
        self.connection.commit()

    def get_image(self, bot_id, gender):
        query = """SELECT * from images WHERE bot_id = '{0}' LIMIT 1;""".format(bot_id)
        self.cursor.execute(query)
        check = self.cursor.fetchone()
        if check is not None:
            return check[4]
        else:
            query = """SELECT * from images WHERE bot_id = 'None' 
                        AND gender = '{0}' LIMIT 1 FOR UPDATE SKIP LOCKED;""".format(gender)
            self.cursor.execute(query)
            profile = self.cursor.fetchone()
            query = """UPDATE images SET bot_id = '{0}' WHERE profile = '{1}';""".format(bot_id, profile[3])
            self.cursor.execute(query)
            self.connection.commit()
            return profile[4]

    # Tools
    def get_comments_sources(self, bot_id):
        query = """SELECT * from comments_sources WHERE bot_id = '{0}';""".format(bot_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def add_post_result(self, bot_id, keywords, exclude_keywords, posted_link, action_type, story_text, action_screen):
        query = "INSERT INTO comments_results (bot_id, keywords, exclude_keywords, posted_link, action_type, story_text, action_screen, date) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        data = (bot_id, keywords, exclude_keywords, posted_link, action_type, story_text, action_screen, datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
        self.cursor.execute(query, data)
        self.connection.commit()

    def check_post_result(self, bot_id, posted_link):
        print(posted_link)
        query = """SELECT * from comments_results WHERE bot_id = '{0}' and posted_link = '{1}';""".format(bot_id, posted_link)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def check_group_in_extracted_groups(self, dst_id, group):
        query = """SELECT * from tools_extracted_groups WHERE dst_id = {0} and url = '{1}';""".format(dst_id, group)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def check_page_in_extracted_pages(self, dst_id, group):
        query = """SELECT * from tools_extracted_pages WHERE dst_id = {0} and url = '{1}';""".format(dst_id, group)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def check_friend_in_extracted_friends(self, dst_id, group):
        query = """SELECT * from tools_extracted_friends WHERE dst_id = {0} and url = '{1}';""".format(dst_id, group)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_tools_find_groups(self, dst_id):
        query = """SELECT * from tools_find_groups WHERE dst_id = {0};""".format(dst_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_tools_find_pages(self, dst_id):
        query = """SELECT * from tools_find_pages WHERE dst_id = {0};""".format(dst_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def save_extracted_groups(self, dst_id, url, name, members, activity_today, activity_last_30, created, author, joined, bot_error, access, admins):
        query = "INSERT INTO tools_extracted_groups (dst_id, url, name, members, activity_today, activity_last_30, created, author, joined, bot_error, access, admins, date) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        data = (dst_id, url, name, members, activity_today, activity_last_30, created, author, joined, bot_error, access, admins, datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
        self.cursor.execute(query, data)
        self.connection.commit()

    def save_extracted_pages(self, dst_id, url, name, likes, follow, bot_error):
        query = "INSERT INTO tools_extracted_pages (dst_id, url, name, likes, follow, bot_error, date) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s);"
        data = (dst_id, url, name, likes, follow, bot_error, datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
        self.cursor.execute(query, data)
        self.connection.commit()

    def save_extracted_friends(self, dst_id, url, total_friends, friends, bot_error):
        query = "INSERT INTO tools_extracted_friends (dst_id, url, total_friends, friends, bot_error, date) " \
                "VALUES (%s, %s, %s, %s, %s, %s);"
        data = (dst_id, url, total_friends, friends, bot_error, datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
        self.cursor.execute(query, data)
        self.connection.commit()

    def get_extracted_groups_for_join(self, bot_id, dst_id):
        query = """SELECT * from tools_extracted_groups WHERE dst_id = {0} 
        and (not '{1}' = ANY(joined) or (joined IS NULL)) 
        and (not '{1}' = ANY(bot_error) or (bot_error IS NULL));""".format(dst_id, bot_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_extracted_pages_for_join(self, bot_id, dst_id):
        query = """SELECT * from tools_extracted_pages WHERE dst_id = {0} 
        and (not '{1}' = ANY(follow) or (follow IS NULL)) 
        and (not '{1}' = ANY(bot_error) or (bot_error IS NULL));""".format(dst_id, bot_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_extracted_pages_sucess(self, bot_id, link):
        query = """update tools_extracted_pages set follow = array_cat(follow, '{0}')
        where url = '{1}';""".format('{'+str(bot_id)+'}', link)
        self.cursor.execute(query)
        self.connection.commit()

    def update_extracted_groups_sucess(self, bot_id, link, exit_status):
        query = """update tools_extracted_groups set joined = array_cat(joined, '{0}'), required_answer = {1}
        where url = '{2}';""".format('{'+str(bot_id)+'}', exit_status, link)
        self.cursor.execute(query)
        self.connection.commit()

    def update_extracted_groups_error(self, bot_id, link, exit_status):
        query = """update tools_extracted_groups set bot_error = array_cat(bot_error, '{0}'), required_answer = {1}
        where url = '{2}';""".format('{'+str(bot_id)+'}', exit_status, link)
        self.cursor.execute(query)
        self.connection.commit()

    def remove_running_bot_from_dst_group(self, bot_id):
        query = """update tools_destination_lists set running = array_remove(running, '{0}');""".format(bot_id)
        self.cursor.execute(query)
        self.connection.commit()

    # Get bot tools dst id
    def get_tools_bot_dst_id(self, bot):
        query = """SELECT * from tools_destination_lists where '{0}' = ANY(profiles) LIMIT 1;""".format(bot[0])
        self.cursor.execute(query)
        return self.cursor.fetchone()

    # Get account actions by dst id
    def get_account_actions(self, dst_id):
        query = """SELECT * from tools_account_actions where dst_id = {0};""".format(dst_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()