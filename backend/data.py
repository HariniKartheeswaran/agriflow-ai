import random

def get_mock_data(location):

    crops = {
        "Thanjavur": "Paddy",
        "Salem": "Millets",
        "Coimbatore": "Maize"
    }

    return {
        "crop": crops.get(location, "Paddy"),

        # 🔥 Add randomness
        "demand": random.randint(80, 120),
        "stock": random.randint(40, 120),
        "staff": random.randint(4, 10)
    }