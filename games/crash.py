"""
📈 Crash Game Logic
"""
import random
import math
from database import db

class CrashGame:
    def __init__(self):
        self.name = "crash"
        self.active_games = {}  # user_id -> game_data

    def generate_multiplier(self):
        """Generate crash multiplier using exponential distribution"""
        # House edge ~1%
        r = random.random()
        if r < 0.01:
            return 1.0  # Instant crash
        multiplier = 0.99 / (1 - r)
        return round(min(multiplier, 1000), 2)

    def start_game(self, user_id, bet_amount):
        """Start a crash game"""
        multiplier = self.generate_multiplier()
        self.active_games[user_id] = {
            "bet_amount": bet_amount,
            "multiplier": multiplier,
            "current": 1.0,
            "cashed_out": False
        }
        return multiplier

    def cash_out(self, user_id, cash_multiplier):
        """Cash out at current multiplier"""
        if user_id not in self.active_games:
            return None

        game = self.active_games[user_id]

        if cash_multiplier >= game["multiplier"]:
            # Busted!
            return self.bust(user_id)

        payout = game["bet_amount"] * cash_multiplier

        session = db.get_session()
        try:
            from database import User
            user = session.query(User).filter_by(id=user_id).first()
            user.balance -= game["bet_amount"]
            user.total_wagered += game["bet_amount"]
            user.balance += payout
            user.total_won += payout
            session.commit()

            db.add_game_history(
                user_id=user_id,
                game_type="crash",
                bet_amount=game["bet_amount"],
                result="win",
                multiplier=cash_multiplier,
                payout=payout,
                details=f"Cashed out at {cash_multiplier}x"
            )

            del self.active_games[user_id]

            return {
                "won": True,
                "cash_multiplier": cash_multiplier,
                "payout": payout,
                "new_balance": user.balance
            }
        finally:
            session.close()

    def bust(self, user_id):
        """Game busted"""
        if user_id not in self.active_games:
            return None

        game = self.active_games[user_id]

        session = db.get_session()
        try:
            from database import User
            user = session.query(User).filter_by(id=user_id).first()
            user.balance -= game["bet_amount"]
            user.total_wagered += game["bet_amount"]
            session.commit()

            db.add_game_history(
                user_id=user_id,
                game_type="crash",
                bet_amount=game["bet_amount"],
                result="loss",
                multiplier=game["multiplier"],
                payout=0,
                details=f"Busted at {game['multiplier']}x"
            )

            bust_multiplier = game["multiplier"]
            del self.active_games[user_id]

            return {
                "won": False,
                "bust_multiplier": bust_multiplier,
                "new_balance": user.balance
            }
        finally:
            session.close()
