import base64
from proto.profile_pb2 import Profile


class User:
    def __init__(self, encoded_profile: str):
        """
        Deserialize a base64 encoded protobuf of a user profile.
        """
        # convert to bytes then unwrap the b64 encoding:
        decoded_profile = base64.b64decode(bytes(encoded_profile))

        # deserialize the protobuf from the decoded data:
        profile = Profile()
        profile.ParseFromString(decoded_profile)

        self.user_id = profile.id
        self.first_name = profile.first
        self.last_name = profile.last
        self.age = profile.age
        self.favorite_color = _decode_colors(profile.color)
        self.following = set()
        self.followers = set()

    def to_dict(self) -> dict:
        return {'user_id': self.user_id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'age': self.age,
                'favorite_color': self.favorite_color,
                'following': self.following,
                'followers': self.followers}

    def __eq__(self, other):
        if isinstance(other, User):
            return self.user_id == other.user_id
        return NotImplemented
        
    def __hash__(self):
        return hash(self.user_id)


def _decode_colors(encoded_colors: int) -> dict:
    """
    Decode and return favorite color RGB values via bitwise ops.
    """
    return {'r': (16711680 & encoded_colors) >> 16,
            'g': (65280 & encoded_colors) >> 8,
            'b': 255 & encoded_colors}
