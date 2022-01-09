# Copyright (c) 2021-2022, Ethan Henderson
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import datetime as dt
import enum
import typing as t
from dataclasses import dataclass

from dateutil.parser import parse as parse_ts

from chatto.channel import Channel
from chatto.stream import Stream


class MessageType(enum.Enum):
    CHAT_ENDED_EVENT = "chatEndedEvent"
    MESSAGE_DELETED_EVENT = "messageDeletedEvent"
    NEW_SPONSOR_EVENT = "newSponsorEvent"
    SPONSOR_ONLY_MODE_ENDED_EVENT = "sponsorOnlyModeEndedEvent"
    SPONSOR_ONLY_MODE_STARTED_EVENT = "sponsorOnlyModeStartedEvent"
    MEMBER_MILESTONE_CHAT_EVENT = "memberMilestoneChatEvent"
    SUPER_CHAT_EVENT = "superChatEvent"
    SUPER_STICKER_EVENT = "superStickerEvent"
    TEXT_MESSAGE_EVENT = "textMessageEvent"
    TOMBSTONE = "tombstone"
    USER_BANNED_EVENT = "userBannedEvent"


@dataclass(eq=True, frozen=True)
class Message:
    id: str
    type: MessageType
    stream: Stream
    channel: Channel
    published_at: dt.datetime
    content: str

    @classmethod
    def from_youtube(cls, item: dict[str, t.Any], stream: Stream) -> Message:
        snippet = item["snippet"]
        return cls(
            id=item["id"],
            type=MessageType(snippet["type"]),
            stream=stream,
            channel=Channel.from_author(item["authorDetails"]),
            published_at=parse_ts(snippet["publishedAt"]),
            content=snippet["displayMessage"],
        )
