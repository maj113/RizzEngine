from Utilities.loader import load_json

def character_has_money(money: int) -> bool:
    player_stats = load_json("player_stats.json")
    character_money: int = player_stats["money"]
    return character_money > money