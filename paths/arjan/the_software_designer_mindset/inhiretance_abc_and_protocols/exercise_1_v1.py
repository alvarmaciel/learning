from dataclasses import dataclass
from time import time


# each social channel has a type
# and the current number of followers
@dataclass
class SocialChannel:
    type: str
    followers: int


# each post has a message and the timestamp when it should be posted
@dataclass
class Post:
    message: str
    timestamp: int


def post_a_message(channel: SocialChannel, message: str) -> None:
    print(f"{channel.type} channel: {message}")


def process_schedule(posts: list[Post], channels: list[SocialChannel]) -> None:
    """process Schedule"""
    for post in posts:
        for channel in channels:
            if post.timestamp <= time():
                post_a_message(channel, post.message)


def main() -> None:
    """Main function"""
    posts = [
        Post(
            "Grandma's carrot cake is available again (limited quantities!)!",
            1568123400,
        ),
        Post("Get your carrot cake now, the promotion ends today!", 1568133400),
    ]
    channels = [
        SocialChannel("youtube", 100),
        SocialChannel("facebook", 100),
        SocialChannel("twitter", 100),
    ]
    process_schedule(posts, channels)


if __name__ == "__main__":
    main()
