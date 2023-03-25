class DatabaseTables:

    # Logs
    @classmethod
    def logs(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS logs
                 (id SERIAL PRIMARY KEY,
                 bot_id text, 
                 log text,
                 date TIMESTAMP);'''
        return sql_table

    # Tracks
    @classmethod
    def tracks(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS tracks
                 (id SERIAL PRIMARY KEY,
                 bot_id text, 
                 track text[][],
                 date TIMESTAMP);'''
        return sql_table

    #Campaigns
    #ALTER TABLE campaigns OWNER TO bot;
    @classmethod
    def campaigns(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS campaigns
                 (id SERIAL PRIMARY KEY,
                 campaign_name text, 
                 description text,
                 dst_lists text[],
                 errors text[],
                 stop_after_single_error BOOLEAN,
                 do_not_publish_in_parallel BOOLEAN,
                 stop_campaign_after_errors BOOLEAN,
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def campaigns_posts(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS campaigns_posts
                 (id SERIAL PRIMARY KEY,
                 campaign_id INTEGER, 
                 post_text text,
                 content text,
                 screen text,
                 status text,
                 src text,
                 published_by INTEGER,
                 running text[],
                 posted text[],
                 posted_groups text[],
                 posted_walls text[],
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def campaigns_scrap_and_share_posts(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS campaigns_scrap_and_share_posts
                 (id SERIAL PRIMARY KEY,
                 process_name text,
                 campaign_id INTEGER, 
                 url text,
                 keywords text,
                 exclude_keywords text,
                 ignore_items_without_images BOOLEAN,
                 maximum_posts INTEGER,
                 post_text text,
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def campaigns_scraped_posts(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS campaigns_scraped_posts
                 (id SERIAL PRIMARY KEY,
                 url text,
                 campaign_id INTEGER, 
                 screen text,
                 shared_bots text[],
                 shared_groups text[],
                 shared_text text,
                 permalinks text[],
                 shared_pages text[],
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def campaigns_liked_posts(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS campaigns_liked_posts
                 (id SERIAL PRIMARY KEY,
                 bot_id text,
                 url text,
                 liked_bots text[],
                 campaign_id INTEGER, 
                 screen text,
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def campaigns_where_to_publish(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS campaigns_where_to_publish
                 (id SERIAL PRIMARY KEY,
                 campaign_id INTEGER, 
                 dst_lists text,
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def campaigns_monitor_folders(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS campaigns_monitor_folders
                 (id SERIAL PRIMARY KEY,
                 campaign_id INTEGER, 
                 folders text[],
                 date TIMESTAMP);'''
        return sql_table


    @classmethod
    def campaigns_comment_like(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS campaigns_comment_like
                 (id SERIAL PRIMARY KEY,
                 campaign_id INTEGER, 
                 keywords text[],
                 exclude text[],
                 like_all_posts_in_history BOOLEAN,
                 date TIMESTAMP);'''
        return sql_table


    @classmethod
    def campaigns_scheduler(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS campaigns_scheduler
                 (id SERIAL PRIMARY KEY,
                 campaign_id INTEGER, 
                 posts_per_day INTEGER,
                 post_interval_start text,
                 post_interval_finish text,
                 randomise_interval_each_day BOOLEAN,
                 randomise_number_of_posts BOOLEAN,
                 maximum_randomise_posts INTEGER,
                 wait BOOLEAN,
                 wait_before_publishing_with_same_account INTEGER,
                 rotate_weekdays_randomly BOOLEAN,
                 operate_on text[],
                 date TIMESTAMP);'''
        return sql_table
    # Campaigns

    # Destination lists
    @classmethod
    def destination_lists(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS destination_lists
                 (id SERIAL,
                 dst_name text PRIMARY KEY, 
                 profiles text[],
                 campaigns text[],
                 walls text[],
                 comment text[],                 
                 date TIMESTAMP);'''
        return sql_table
    #campaigns text[] not null default '{}'
    # Destination lists

    @classmethod
    def bot_table(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS bots
                 (login text PRIMARY KEY, 
                 password text, 
                 vpn_provider text, 
                 vpn_region text,
                 vpn_login text,
                 vpn_password text,
                 cookies text,
                 used_status BOOLEAN,
                 block_status text,
                 bot_first_name text,
                 bot_last_name text,
                 bot_gender text,
                 bot_birth_day text,
                 bot_birth_month text,
                 bot_birth_year text,
                 user_agent text,
                 screen text,
                 city text,
                 school text,
                 university text,
                 job text,
                 profile_picture text,
                 bot_images_list text,
                 creation_date TIMESTAMP,
                 last_used_date TIMESTAMP,
                 total_friends INTEGER,
                 scraped_profiles INTEGER,
                 total_actions INTEGER,
                 total_errors INTEGER,
                 proxy_ip text,
                 proxy_port text,
                 proxy_user text,
                 proxy_password text,
                 local_ip text,
                 public_ip text,
                 instance_id text);'''
        return sql_table

    @classmethod
    def action_table(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS action
                 (id SERIAL PRIMARY KEY,
                 bot_id text,
                 groups_id INTEGER,
                 dst_id INTEGER,
                 action_priority text,
                 action_id text,
                 action_status BOOLEAN,
                 image text,
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def friends_table(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS friends
                 (id SERIAL PRIMARY KEY,
                 bot_id text, 
                 friend_link text,
                 status text,
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def post_table(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS post
                 (id SERIAL PRIMARY KEY
                 bot_id text, 
                 post text,
                 link text,
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def comments_table(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS comments
                 (id SERIAL PRIMARY KEY
                 bot_id text, 
                 comment text,
                 link text,
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def following_table(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS following
                 (id SERIAL PRIMARY KEY,
                 bot_id text, 
                 link text,
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def groups_table(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS groups
                 (id SERIAL PRIMARY KEY,
                 bot_id text, 
                 link text,
                 group_name text,
                 status text,
                 dst_select_status BOOLEAN,
                 screen text,
                 date TIMESTAMP);'''
        return sql_table


    @classmethod
    def errors_table(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS errors
                 (id SERIAL PRIMARY KEY,
                 bot_id text, 
                 error text,
                 image text,
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def images_table(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS images
                 (id SERIAL PRIMARY KEY,
                 bot_id text,
                 gender text, 
                 profile text,
                 image text,
                 date TIMESTAMP);'''
        return sql_table

# Tools
    @classmethod
    def comments_settings(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS comments_settings
                 (id SERIAL PRIMARY KEY,
                 dst_id INTEGER,
                 on_off BOOLEAN,
                 wait_between_start INTEGER,
                 wait_between_end INTEGER,
                 execute_between_start text,
                 execute_between_end text,
                 random_sleep_time BOOLEAN,
                 rotate_weekends_randomly BOOLEAN,
                 operate_on text[],
                 comments_maximum_start INTEGER,
                 comments_maximum_end INTEGER,
                 comments_increasing_start INTEGER,
                 comments_increasing_end INTEGER,
                 maximum_single_source_per_day BOOLEAN,
                 comments_single_source_maximum_start INTEGER,
                 comments_single_source_maximum_end INTEGER,
                 comments_post_maximum_age BOOLEAN,
                 comments_maximum_days INTEGER,
                 keywords text[],
                 exclude text[],
                 comment text,
                 date TIMESTAMP);'''
        return sql_table


    @classmethod
    def comments_sources(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS comments_sources
                 (id SERIAL PRIMARY KEY,
                 dst_id INTEGER,
                 comment_like_in_pages BOOLEAN,
                 comment_like_in_walls BOOLEAN,
                 comment_like_in_searches BOOLEAN,
                 keywords text[],
                 exclude_keywords text[],
                 comment_like_in_groups BOOLEAN,
                 comment_like_in_permalinks BOOLEAN,
                 url_text_area text,
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def comments_results(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS comments_results
                 (id SERIAL PRIMARY KEY,
                 dst_id INTEGER,
                 keywords text[],
                 exclude_keywords text[],
                 posted_link text,
                 action_type text,
                 story_text text,
                 action_screen text,
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def tools_find_groups(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS tools_find_groups
                 (id SERIAL PRIMARY KEY,
                 dst_id INTEGER,
                 keywords text[],
                 exclude_keywords text[],
                 groups_extra_urls text[],
                 min_users BOOLEAN,
                 en_gr_groups BOOLEAN,
                 opened_groups BOOLEAN,
                 admin_post BOOLEAN,
                 min_users_count INTEGER,
                 status BOOLEAN,
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def tools_find_pages(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS tools_find_pages
                 (id SERIAL PRIMARY KEY,
                 dst_id INTEGER,
                 keywords text[],
                 exclude_keywords text[],
                 pages_extra_urls text[],
                 min_likes BOOLEAN,
                 en_gr_pages BOOLEAN,
                 min_likes_count INTEGER,
                 status BOOLEAN,
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def tools_find_friends(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS tools_find_friends
                 (id SERIAL PRIMARY KEY,
                 dst_id INTEGER,
                 keywords text[],
                 exclude_keywords text[],
                 friends_extra_urls text[],
                 min_mutual BOOLEAN,
                 en_gr_friends BOOLEAN,
                 opened_friends BOOLEAN,
                 min_mutual_count INTEGER,
                 status BOOLEAN,
                 date TIMESTAMP);'''
        return sql_table


    @classmethod
    def tools_extracted_groups(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS tools_extracted_groups
                 (id SERIAL PRIMARY KEY,
                 dst_id INTEGER,
                 url text,
                 name text,
                 members INTEGER,
                 activity_today INTEGER,
                 activity_last_30 INTEGER,
                 created text,
                 author text,
                 joined text[],
                 bot_error text[],
                 required_answer BOOLEAN,
                 admins text[],
                 access BOOLEAN,
                 keywords text[],
                 exclude_keywords text[],
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def tools_extracted_pages(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS tools_extracted_pages
                 (id SERIAL PRIMARY KEY,
                 dst_id INTEGER,
                 url text,
                 name text,
                 likes INTEGER,
                 follow text[],
                 bot_error text[],
                 required_answer BOOLEAN,
                 access BOOLEAN,
                 keywords text[],
                 exclude_keywords text[],
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def tools_extracted_friends(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS tools_extracted_friends
                 (id SERIAL PRIMARY KEY,
                 dst_id INTEGER,
                 url text,
                 total_friends INTEGER,
                 friends text[],
                 bot_error text[],
                 required_answer BOOLEAN,
                 access BOOLEAN,
                 keywords text[],
                 exclude_keywords text[],
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def tools_joiner(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS tools_joiner
                 (id SERIAL PRIMARY KEY,
                 dst_id INTEGER, 
                 wait_between INTEGER,
                 wait_between_and INTEGER,
                 execute_between text,
                 execute_between_and text,
                 random_sleep_time BOOLEAN,
                 join_between INTEGER,
                 join_between_and INTEGER,
                 auto_stop BOOLEAN,
                 reaching_groups INTEGER,
                 join_between_peer_day INTEGER,
                 join_between_and_peer_day INTEGER,
                 auto_stop_peer_day BOOLEAN,
                 reaching_groups_peer_day INTEGER,
                 operate_on text[],
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def tools_destination_lists(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS tools_destination_lists
                 (id SERIAL,
                 dst_name text PRIMARY KEY, 
                 profiles text[],
                 running text[],
                 extraction text,
                 configuration INTEGER,
                 date TIMESTAMP);'''
        return sql_table

    @classmethod
    def tools_account_actions(cls):
        sql_table = '''CREATE TABLE IF NOT EXISTS tools_account_actions
                 (id SERIAL,
                 dst_id INTEGER PRIMARY KEY,
                 wait_between INTEGER,
                 wait_between_and INTEGER,
                 execute_between text,
                 execute_between_and text,
                 random_sleep_time BOOLEAN,
                 rotate_weekdays_randomly BOOLEAN,
                 operate_on text[],
                 accept_per_login INTEGER,
                 auto_accept_friends BOOLEAN,
                 auto_like_news_feed_posts BOOLEAN,
                 auto_like_news_feed_posts_num INTEGER,
                 auto_like_news_feed_posts_keywords BOOLEAN,
                 auto_like_news_feed_posts_keywords_num INTEGER,
                 keywords text[],
                 exclude_keywords text[],
                 like_between_post_per_login INTEGER,
                 like_between_post_per_login_and INTEGER,
                 read_notifications_and_messages BOOLEAN,
                 high_percent INTEGER,
                 middle_percent INTEGER,
                 low_percent INTEGER,
                 use_session_settings BOOLEAN,
                 long_session_time_min INTEGER,
                 long_session_time_max INTEGER,
                 medium_session_time_min INTEGER,
                 medium_session_time_max INTEGER,
                 short_session_time_min INTEGER,
                 short_session_time_max INTEGER,
                 short_time_min INTEGER,
                 short_time_max INTEGER,
                 medium_time_min INTEGER,
                 medium_time_max INTEGER,
                 long_time_min INTEGER,
                 long_time_max INTEGER,
                 use_engagement_levels BOOLEAN,
                 strong_time_min INTEGER,
                 strong_time_max INTEGER,
                 moderate_time_min INTEGER,
                 moderate_time_max INTEGER,
                 weak_time_min INTEGER,
                 weak_time_max INTEGER,
                 date TIMESTAMP);'''
        return sql_table