import random
from typing import Dict, Type, Union

from core.features.comment import Comment
from core.features.follow_page import FollowPage
from core.features.friend_profile_view import FriendsProfileView
from core.features.join_group import JoinGroup
from core.features.friends_requests import BotFriendsRequests
from core.features.may_know_friends import BotMayKnowFriends
from core.features.news_feed import NewsFeed
from core.features.photo_upload import PhotoUpload
from core.features.post import Post
from core.features.profile_city import BotCity
from core.features.profile_school import BotSchool
from core.features.profile_university import BotUniversity
from core.features.search_for_friends import BotSearchForFriends
from core.features.search_groups import BotSearchGroups
from core.features.search_groups_by_link import BotSearchGroupsByLink
from core.features.search_pages_by_link import BotSearchPagesByLink
from core.features.search_pages_follow import BotSearchPagesFollow
from core.features.search_photos import BotSearchPhotos
from core.features.search_places import BotSearchPlaces
from core.features.search_posts import BotSearchPosts
from core.features.search_videos import BotSearchVideos
from core.features.sharing import GroupsShare


class ActionModel:
    module = 'ActionModel'

    low = {
        'news_feed': NewsFeed
    }

    middle = {
        'news_feed': NewsFeed
    }

    high = {
        #'comment': Comment,
        #'post': Post
        #'search_group': BotSearchGroupsByLink,
        #'search_pages': BotSearchPagesByLink,
        'follow_page': FollowPage,
        'join_group': JoinGroup,
        'share': GroupsShare
    }

    profile = {
        'photo': PhotoUpload,
        'city': BotCity,
        'school': BotSchool,
        'university': BotUniversity
    }

    @classmethod
    def get_random_action(cls, action_type):
        """
        Get random action

        :param action_type: 'high', 'middle', 'low'

        """
        if action_type == 'high':
            return random.choice(list(cls.high.items()))
        elif action_type == 'middle':
            return random.choice(list(cls.middle.items()))
        elif action_type == 'low':
            return random.choice(list(cls.low.items()))
        else:
            return random.choice(list(cls.high.items()))

    @classmethod
    def get_actions(cls, action_type) -> Dict:
        """
        Get all action from action type

        :param action_type: 'high', 'middle', 'low'

        :rtype: Dict
        """
        if action_type == 'high':
            return cls.high
        elif action_type == 'middle':
            return cls.middle
        elif action_type == 'low':
            return cls.low
        elif action_type == 'profile':
            return cls.profile

    @classmethod
    def search_action(cls, action) -> [object, str]:
        """
        Get action

        :param action: action name

        :rtype: [object, str]
        """
        if action in cls.high:
            return cls.high[action], 'high'
        elif action in cls.middle:
            return cls.middle[action], 'middle'
        elif action in cls.low:
            return cls.low[action], 'low'
        elif action in cls.profile:
            return cls.profile[action], 'profile'

