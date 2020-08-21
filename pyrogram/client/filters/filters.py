#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import re
from typing import Callable, Union

from .filter import Filter
from ..types import Message, CallbackQuery, InlineQuery
from ..types.bots_and_keyboards import InlineKeyboardMarkup, ReplyKeyboardMarkup

CUSTOM_FILTER_NAME = "CustomFilter"


def create(func: Callable, name: str = None, **kwargs) -> Filter:
    """Easily create a custom filter.

    Custom filters give you extra control over which updates are allowed or not to be processed by your handlers.

    Parameters:
        func (``callable``):
            A function that accepts two positional arguments *(filter, update)* and returns a boolean: True if the
            update should be handled, False otherwise. The *filter* argument refers to the filter itself and can be used
            to access keyword arguments (read below). The *update* argument type will vary depending on which
            `Handler <handlers>`_ is coming from. For example, in a :obj:`MessageHandler` the *update* argument will be
            a :obj:`Message`; in a :obj:`CallbackQueryHandler` the *update* will be a :obj:`CallbackQuery`. Your
            function body can then access the incoming update attributes and decide whether to allow it or not.

        name (``str``, *optional*):
            Your filter's name. Can be anything you like.
            Defaults to "CustomFilter".

        **kwargs (``any``, *optional*):
            Any keyword argument you would like to pass. Useful when creating parameterized custom filters, such as
            :meth:`~Filters.command` or :meth:`~Filters.regex`.
    """
    # TODO: unpack kwargs using **kwargs into the dict itself. For Python 3.5+ only
    d = {"__call__": func}
    d.update(kwargs)

    return type(name or CUSTOM_FILTER_NAME, (Filter,), d)()


class Filters:
    """This class provides access to all library-defined Filters available in Pyrogram.

    The Filters listed here are currently intended to be used with the :obj:`MessageHandler` only.
    At the moment, if you want to filter updates coming from different `Handlers <handlers.html>`_ you have to create
    your own filters with :meth:`~Filters.create` and use them in the same way.
    """

    create = create

    all = create(lambda _, m: True, "AllFilter")
    """Filter all messages."""

    me = create(lambda _, m: bool(m.from_user and m.from_user.is_self), "MeFilter")
    """Filter messages generated by you yourself."""

    bot = create(lambda _, m: bool(m.from_user and m.from_user.is_bot), "BotFilter")
    """Filter messages coming from bots."""

    incoming = create(lambda _, m: not m.outgoing, "IncomingFilter")
    """Filter incoming messages. Messages sent to your own chat (Saved Messages) are also recognised as incoming."""

    outgoing = create(lambda _, m: m.outgoing, "OutgoingFilter")
    """Filter outgoing messages. Messages sent to your own chat (Saved Messages) are not recognized as outgoing."""

    text = create(lambda _, m: bool(m.text), "TextFilter")
    """Filter text messages."""

    reply = create(lambda _, m: bool(m.reply_to_message), "ReplyFilter")
    """Filter messages that are replies to other messages."""

    forwarded = create(lambda _, m: bool(m.forward_date), "ForwardedFilter")
    """Filter messages that are forwarded."""

    caption = create(lambda _, m: bool(m.caption), "CaptionFilter")
    """Filter media messages that contain captions."""

    edited = create(lambda _, m: bool(m.edit_date), "EditedFilter")
    """Filter edited messages."""

    audio = create(lambda _, m: bool(m.audio), "AudioFilter")
    """Filter messages that contain :obj:`Audio` objects."""

    document = create(lambda _, m: bool(m.document), "DocumentFilter")
    """Filter messages that contain :obj:`Document` objects."""

    photo = create(lambda _, m: bool(m.photo), "PhotoFilter")
    """Filter messages that contain :obj:`Photo` objects."""

    sticker = create(lambda _, m: bool(m.sticker), "StickerFilter")
    """Filter messages that contain :obj:`Sticker` objects."""

    animation = create(lambda _, m: bool(m.animation), "AnimationFilter")
    """Filter messages that contain :obj:`Animation` objects."""

    game = create(lambda _, m: bool(m.game), "GameFilter")
    """Filter messages that contain :obj:`Game` objects."""

    video = create(lambda _, m: bool(m.video), "VideoFilter")
    """Filter messages that contain :obj:`Video` objects."""

    media_group = create(lambda _, m: bool(m.media_group_id), "MediaGroupFilter")
    """Filter messages containing photos or videos being part of an album."""

    voice = create(lambda _, m: bool(m.voice), "VoiceFilter")
    """Filter messages that contain :obj:`Voice` note objects."""

    video_note = create(lambda _, m: bool(m.video_note), "VideoNoteFilter")
    """Filter messages that contain :obj:`VideoNote` objects."""

    contact = create(lambda _, m: bool(m.contact), "ContactFilter")
    """Filter messages that contain :obj:`Contact` objects."""

    location = create(lambda _, m: bool(m.location), "LocationFilter")
    """Filter messages that contain :obj:`Location` objects."""

    venue = create(lambda _, m: bool(m.venue), "VenueFilter")
    """Filter messages that contain :obj:`Venue` objects."""

    web_page = create(lambda _, m: m.web_page, "WebPageFilter")
    """Filter messages sent with a webpage preview."""

    poll = create(lambda _, m: m.poll, "PollFilter")
    """Filter messages that contain :obj:`Poll` objects."""

    private = create(lambda _, m: bool(m.chat and m.chat.type in {"private", "bot"}), "PrivateFilter")
    """Filter messages sent in private chats."""

    group = create(lambda _, m: bool(m.chat and m.chat.type in {"group", "supergroup"}), "GroupFilter")
    """Filter messages sent in group or supergroup chats."""

    channel = create(lambda _, m: bool(m.chat and m.chat.type == "channel"), "ChannelFilter")
    """Filter messages sent in channels."""

    new_chat_members = create(lambda _, m: bool(m.new_chat_members), "NewChatMembersFilter")
    """Filter service messages for new chat members."""

    left_chat_member = create(lambda _, m: bool(m.left_chat_member), "LeftChatMemberFilter")
    """Filter service messages for members that left the chat."""

    new_chat_title = create(lambda _, m: bool(m.new_chat_title), "NewChatTitleFilter")
    """Filter service messages for new chat titles."""

    new_chat_photo = create(lambda _, m: bool(m.new_chat_photo), "NewChatPhotoFilter")
    """Filter service messages for new chat photos."""

    delete_chat_photo = create(lambda _, m: bool(m.delete_chat_photo), "DeleteChatPhotoFilter")
    """Filter service messages for deleted photos."""

    group_chat_created = create(lambda _, m: bool(m.group_chat_created), "GroupChatCreatedFilter")
    """Filter service messages for group chat creations."""

    supergroup_chat_created = create(lambda _, m: bool(m.supergroup_chat_created), "SupergroupChatCreatedFilter")
    """Filter service messages for supergroup chat creations."""

    channel_chat_created = create(lambda _, m: bool(m.channel_chat_created), "ChannelChatCreatedFilter")
    """Filter service messages for channel chat creations."""

    migrate_to_chat_id = create(lambda _, m: bool(m.migrate_to_chat_id), "MigrateToChatIdFilter")
    """Filter service messages that contain migrate_to_chat_id."""

    migrate_from_chat_id = create(lambda _, m: bool(m.migrate_from_chat_id), "MigrateFromChatIdFilter")
    """Filter service messages that contain migrate_from_chat_id."""

    pinned_message = create(lambda _, m: bool(m.pinned_message), "PinnedMessageFilter")
    """Filter service messages for pinned messages."""

    game_high_score = create(lambda _, m: bool(m.game_high_score), "GameHighScoreFilter")
    """Filter service messages for game high scores."""

    reply_keyboard = create(lambda _, m: isinstance(m.reply_markup, ReplyKeyboardMarkup), "ReplyKeyboardFilter")
    """Filter messages containing reply keyboard markups"""

    inline_keyboard = create(lambda _, m: isinstance(m.reply_markup, InlineKeyboardMarkup), "InlineKeyboardFilter")
    """Filter messages containing inline keyboard markups"""

    mentioned = create(lambda _, m: bool(m.mentioned), "MentionedFilter")
    """Filter messages containing mentions"""

    via_bot = create(lambda _, m: bool(m.via_bot), "ViaBotFilter")
    """Filter messages sent via inline bots"""

    service = create(lambda _, m: bool(m.service), "ServiceFilter")
    """Filter service messages.

    A service message contains any of the following fields set: *left_chat_member*,
    *new_chat_title*, *new_chat_photo*, *delete_chat_photo*, *group_chat_created*, *supergroup_chat_created*,
    *channel_chat_created*, *migrate_to_chat_id*, *migrate_from_chat_id*, *pinned_message*, *game_score*.
    """

    media = create(lambda _, m: bool(m.media), "MediaFilter")
    """Filter media messages.

    A media message contains any of the following fields set: *audio*, *document*, *photo*, *sticker*, *video*,
    *animation*, *voice*, *video_note*, *contact*, *location*, *venue*, *poll*.
    """

    scheduled = create(lambda _, m: bool(m.scheduled), "ScheduledFilter")
    """Filter messages that have been scheduled (not yet sent)."""

    from_scheduled = create(lambda _, m: bool(m.from_scheduled), "FromScheduledFilter")
    """Filter new automatically sent messages that were previously scheduled."""

    # Messages from linked channels are forwarded automatically by Telegram and have no sender (from_user is None).
    linked_channel = create(lambda _, m: bool(m.forward_from_chat and not m.from_user), "LinkedChannelFilter")
    """Filter messages that are automatically forwarded from the linked channel to the group chat."""

    @staticmethod
    def command(
        commands: str or list,
        prefixes: str or list = "/",
        case_sensitive: bool = False
    ):
        """Filter commands, i.e.: text messages starting with "/" or any other custom prefix.

        Parameters:
            commands (``str`` | ``list``):
                The command or list of commands as string the filter should look for.
                Examples: "start", ["start", "help", "settings"]. When a message text containing
                a command arrives, the command itself and its arguments will be stored in the *command*
                field of the :obj:`Message`.

            prefixes (``str`` | ``list``, *optional*):
                A prefix or a list of prefixes as string the filter should look for.
                Defaults to "/" (slash). Examples: ".", "!", ["/", "!", "."], list(".:!").
                Pass None or "" (empty string) to allow commands with no prefix at all.

            case_sensitive (``bool``, *optional*):
                Pass True if you want your command(s) to be case sensitive. Defaults to False.
                Examples: when True, command="Start" would trigger /Start but not /start.
        """
        command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

        def func(flt, message):
            text = message.text or message.caption
            message.command = None

            if not text:
                return False

            pattern = r"^{}(?:\s|$)" if flt.case_sensitive else r"(?i)^{}(?:\s|$)"

            for prefix in flt.prefixes:
                if not text.startswith(prefix):
                    continue

                without_prefix = text[len(prefix):]

                for cmd in flt.commands:
                    if not re.match(pattern.format(re.escape(cmd)), without_prefix):
                        continue

                    # match.groups are 1-indexed, group(1) is the quote, group(2) is the text
                    # between the quotes, group(3) is unquoted, whitespace-split text

                    # Remove the escape character from the arguments
                    message.command = [cmd] + [
                        re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                        for m in command_re.finditer(without_prefix[len(cmd):])
                    ]

                    return True

            return False

        commands = commands if isinstance(commands, list) else [commands]
        commands = {c if case_sensitive else c.lower() for c in commands}

        prefixes = [] if prefixes is None else prefixes
        prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
        prefixes = set(prefixes) if prefixes else {""}

        return create(
            func,
            "CommandFilter",
            commands=commands,
            prefixes=prefixes,
            case_sensitive=case_sensitive
        )

    @staticmethod
    def regex(pattern: Union[str, re.Pattern], flags: int = 0):
        """Filter updates that match a given regular expression pattern.

        Can be applied to handlers that receive one of the following updates:

        - :obj:`Message`: The filter will match ``text`` or ``caption``.
        - :obj:`CallbackQuery`: The filter will match ``data``.
        - :obj:`InlineQuery`: The filter will match ``query``.

        When a pattern matches, all the `Match Objects <https://docs.python.org/3/library/re.html#match-objects>`_ are
        stored in the ``matches`` field of the update object itself.

        Parameters:
            pattern (``str`` | ``Pattern``):
                The regex pattern as string or as pre-compiled pattern.

            flags (``int``, *optional*):
                Regex flags.
        """

        def func(flt, update):
            if isinstance(update, Message):
                value = update.text or update.caption
            elif isinstance(update, CallbackQuery):
                value = update.data
            elif isinstance(update, InlineQuery):
                value = update.query
            else:
                raise ValueError("Regex filter doesn't work with {}".format(type(update)))

            if value:
                update.matches = list(flt.p.finditer(value)) or None

            return bool(update.matches)

        return create(
            func,
            "RegexFilter", 
            p=pattern if isinstance(pattern, re.Pattern) else re.compile(pattern, flags)
        )

    # noinspection PyPep8Naming
    class user(Filter, set):
        """Filter messages coming from one or more users.

        You can use `set bound methods <https://docs.python.org/3/library/stdtypes.html#set>`_ to manipulate the
        users container.

        Parameters:
            users (``int`` | ``str`` | ``list``):
                Pass one or more user ids/usernames to filter users.
                For you yourself, "me" or "self" can be used as well.
                Defaults to None (no users).
        """

        def __init__(self, users: int or str or list = None):
            users = [] if users is None else users if isinstance(users, list) else [users]

            super().__init__(
                "me" if u in ["me", "self"]
                else u.lower().strip("@") if isinstance(u, str)
                else u for u in users
            )

        def __call__(self, message):
            return (message.from_user
                    and (message.from_user.id in self
                         or (message.from_user.username
                             and message.from_user.username.lower() in self)
                         or ("me" in self
                             and message.from_user.is_self)))

    # noinspection PyPep8Naming
    class chat(Filter, set):
        """Filter messages coming from one or more chats.

        You can use `set bound methods <https://docs.python.org/3/library/stdtypes.html#set>`_ to manipulate the
        chats container.

        Parameters:
            chats (``int`` | ``str`` | ``list``):
                Pass one or more chat ids/usernames to filter chats.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                Defaults to None (no chats).
        """

        def __init__(self, chats: int or str or list = None):
            chats = [] if chats is None else chats if isinstance(chats, list) else [chats]

            super().__init__(
                "me" if c in ["me", "self"]
                else c.lower().strip("@") if isinstance(c, str)
                else c for c in chats
            )

        def __call__(self, message):
            return (message.chat
                    and (message.chat.id in self
                         or (message.chat.username
                             and message.chat.username.lower() in self)
                         or ("me" in self
                             and message.from_user
                             and message.from_user.is_self
                             and not message.outgoing)))

    dan = create(lambda _, m: bool(m.from_user and m.from_user.id == 23122162), "DanFilter")
