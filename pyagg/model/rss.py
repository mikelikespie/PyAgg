# Copyright (c) 2009, Michael Lewis
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials
#       provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""This is the schema for a bunch of RSS feeds

Documentation for RSS elements from http://cyber.law.harvard.edu/rss/rss.html"""
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Boolean

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relation, dynamic_loader

Base = declarative_base()

class ChannelCategory(Base):
    __tablename__ = 'channel_cagegories'
    id = Column(Integer, primary_key=True)

    channel_id = Column(Integer, ForeignKey('channels.id',
        onupdate="CASCADE", ondelete="CASCADE"))

    category = Column(String)

class ChannelCloud(Base):
    __tablename__ = 'channel_clouds'

    id = Column(Integer, primary_key=True)

    channel_id = Column(Integer, ForeignKey('channels.id',
        onupdate="CASCADE", ondelete="CASCADE"))

    domain = Column(String)
    port = Column(Integer)
    path = Column(String)
    registerProcedure = Column(String)
    protocol = Column(String)

class ChannelImage(Base):
    __tablename__ = 'channel_iamges'

    id = Column(Integer, primary_key=True)

    channel_id = Column(Integer, ForeignKey('channels.id',
        onupdate="CASCADE", ondelete="CASCADE"))

    url = Column(String)
    title = Column(String)
    link = Column(String)

    width = Column(Integer)
    height = Column(Integer)

class ChannelTextInput(Base):
    __tablename__ = 'channel_text_inputs'

    id = Column(Integer, primary_key=True)

    channel_id = Column(Integer, ForeignKey('channels.id',
        onupdate="CASCADE", ondelete="CASCADE"))

    title = Column(String)
    description = Column(String)
    name = Column(String)
    link = Column(String)

class ChannelItemCategory(Base):
    __tablename__ = 'channel_item_cagegories'
    id = Column(Integer, primary_key=True)

    channel_item_id = Column(Integer, ForeignKey('channel_items.id',
        onupdate="CASCADE", ondelete="CASCADE"))

    category = Column(String)


class ChannelItem(Base):
    """This is the item in a channel"""

    __tablename__ = 'channel_items'

    id = Column(Integer, primary_key=True)

    channel_id = Column(Integer, ForeignKey('channels.id',
        onupdate="CASCADE", ondelete="CASCADE"))

    title = Column(String)
    """The title of the item.

    ex:
        Venice Film Festival Tries to Quit Sinking
    """

    link = Column(String)
    """The URL of the item.

    ex:
        http://nytimes.com/2004/12/07FEST.html
    """

    description = Column(String)
    """The item synopsis.

    ex:
        Some of the most heated chatter at the Venice Film Festival this week was
        about the way that the arrival of the stars at the Palazzo del Cinema was
        being staged.
    """

    author = Column(String)
    """Email address of the author of the item.

    ex:
        oprah\@oxygen.net
    """

    _categories = relation(ChannelItemCategory, collection_class=set,
        cascade="all, delete-orphan")
    
    categories = association_proxy('_categories', 'category')
    """Includes the item in one or more categories.

    ex:
        http://www.myblog.org/cgi-local/mt/mt-comments.cgi?entry_id=290
    """

    comments = Column(String)
    """URL of a page for comments relating to the item.  """

    enclosure = Column(String)
    """Describes a media object that is attached to the item.

    ex:
        http://inessential.com/2002/09/01.php#a2
    """

    guid = Column(String)
    """A string that uniquely identifies the item."""

    guidIsAPermaLink = Column(Boolean)
    
    pubDate = Column(DateTime)
    """Indicates when the item was published.

    ex:
        Sun, 19 May 2002 15:21:36 GMT
    """
    
    source = Column(String)
    """The RSS channel that the item came from."""
    
class SkipHour(Base):
    __tablename__ = 'skip_hours'

    id = Column(Integer, primary_key=True)

    channel_id = Column(Integer, ForeignKey('channels.id',
        onupdate="CASCADE", ondelete="CASCADE"))

    hour = Column(Integer)

class SkipDay(Base):
    __tablename__ = 'skip_days'

    id = Column(Integer, primary_key=True)

    channel_id = Column(Integer, ForeignKey('channels.id',
        onupdate="CASCADE", ondelete="CASCADE"))

    day = Column(String)

class Channel(Base):
    """ Subordinate to the <rss> element is a single <channel> element, which
    contains information about the channel (metadata) and its contents.
    """

    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)

    title = Column(String)
    """The name of the channel. It's how people refer to your service. If you
    have an HTML website that contains the same information as your RSS file,
    the title of your channel should be the same as the title of your website. 

    ex:
        GoUpstate.com News Headlines
    """

    link = Column(String)
    """The URL to the HTML website corresponding to the channel.

    ex:
        http://www.goupstate.com/
    """

    description = Column(String)
    """Phrase or sentence describing the channel.

    ex:
        The latest news from GoUpstate.com, a Spartanburg Herald-Journal Web
        site.
    """

    language = Column(String)
    """The language the channel is written in. This allows aggregators to group
    all Italian language sites, for example, on a single page. A list of
    allowable values for this element, as provided by Netscape, is here_. You
    may also use `values defined`_ by the W3C.


    .. _here:  http://cyber.law.harvard.edu/rss/languages.html
    .. _`values defined`: http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes

    ex:
        en-us
    """

    copyright = Column(String)
    """Copyright notice for content in the channel.

    ex:
        Copyright 2002, Spartanburg Herald-Journal
    """

    managingEditor = Column(String)
    """Email address for person responsible for editorial content.

    ex:
        geo@herald.com (George Matesky)
    """

    webMaster = Column(String)
    """Email address for person responsible for technical issues relating to
    channel.
    
    ex:
        betty@herald.com (Betty Guernsey)
    """

    pubDate = Column(DateTime)
    """The publication date for the content in the channel. For example, the New
    York Times publishes on a daily basis, the publication date flips once every
    24 hours. That's when the pubDate of the channel changes.

    ex:
        Sat, 07 Sep 2002 00:00:01 GMT
    """

    lastBuildDate = Column(DateTime)
    """The last time the content of the channel changed.
    
    ex:
        Sat, 07 Sep 2002 09:42:31 GMT
    """

    _categories = relation(ChannelCategory, collection_class=set,
        cascade="all, delete-orphan")
    
    categories = association_proxy('_categories', 'category')
    """Specify one or more categories that the channel belongs to. Follows the
    same rules as the <item>-level  :class:ChannelCategory element.
   
    ex:
        <category>Newspapers</category>
    """

    generator = Column(String)
    """A string indicating the program used to generate the channel.

    ex:
        MightyInHouse Content System v2.3
    """

    docs = Column(String)
    """A URL that points to the documentation for the format used in the RSS
    file. It's probably a pointer to this page. It's for people who might
    stumble across an RSS file on a Web server 25 years from now and wonder what
    it is.

    ex:
        http://blogs.law.harvard.edu/tech/rss
    """
    
    cloud = relation(ChannelCloud)
    """Allows processes to register with a cloud to be notified of updates to
    the channel, implementing a lightweight publish-subscribe protocol for RSS
    feeds.
    """

    ttl = Column(String)
    """ttl stands for time to live. It's a number of minutes that indicates how
    long a channel can be cached before refreshing from the source. More info
    here.

    ex:
        60
    """

    image = relation(ChannelImage)
    """Specifies a GIF, JPEG or PNG image that can be displayed with the
    channel. More info here.
    """

    rating = Column(String)
    """The PICS rating for the channel."""

    textInput = relation(ChannelTextInput)
    """Specifies a text input box that can be displayed with the channel."""

    _skipHours = relation(SkipHour, collection_class=set,
        cascade="all, delete-orphan")
    
    skipHours = association_proxy('_skipHours', 'hour')
    """A hint for aggregators telling them which hours they can skip. More info
    here.
    """

    _skipDays = relation(SkipDay, collection_class=set,
        cascade="all, delete-orphan")
    
    skipDays = association_proxy('_skipDays', 'day')
    """A hint for aggregators telling them which days they can skip. More info
    here.
    """
