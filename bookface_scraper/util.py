import base64
from proto.profile_pb2 import Profile


def decode_user_profile(encoded_profile: str) -> dict:
    """
    Decodes a base64 encoded protobuf of a user profile.
    Returns a dictionary containing decoded user details.
    """
    # convert to bytes then unwrap the b64 encoding:
    decoded_profile = base64.b64decode(bytes(encoded_profile))

    # deserialize the protobuf from the decoded data:
    profile = Profile()
    profile.ParseFromString(decoded_profile)

    return {'name': f'{profile.first} {profile.last}',
            'age': profile.age,
            'favorite_color': _decode_colors(profile.color)}


def _decode_colors(encoded_colors: int) -> dict:
    """
    Decode and return favorite color RGB values via bitwise ops.
    """
    return {'r': (16711680 & encoded_colors) >> 16,
            'g': (65280 & encoded_colors) >> 8,
            'b': 255 & encoded_colors}
