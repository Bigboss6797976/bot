"""
🎰 Slots Game Logic
"""
import random
from database import db

class SlotsGame:
    def __init__(self):
        self.name = "slots"
        self.symbols = ["🍒", "🍋", "🍊", "🍇", "💎", "7️⃣", "🔔", "⭐"]
        self.weights = [30, 25, 20, 15, 5, 3, 1.5, 0.5]

    def spin(self, user_id, bet_amount):
        """Spin the slots"""
        # Generate 3 symbols
        result = random.choices(self.symbols, weights=self.weights, k=3)

        # Calculate payout
        if result[0] == result[1] == result[2]:
            # All 3 match
            symbol = result[0]
            multipliers = {
                "7️⃣": 50, "💎": 30, "🔔": 20, "⭐": 15,
                "🍇": 10, "🍊": 8, "🍋": 5, "🍒": 3
            }
            multiplier = multipliers.get(symbol, 2)
        elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
            # 2 match
            multiplier = 1.5
        else:
            # No match
            multiplier = 0

        payout = bet_amount * multiplier
        won = multiplier > 0

        # Update user
        session = db.get_session()
        try:
            from database import User
            user = session.query(User).filter_by(id=user_id).first()
            user.balance -= bet_amount
            user.total_wagered += bet_amount

            if won:
                user.balance += payout
                user.total_won += payout
                result_str = "win"
            else:
                result_str = "loss"

            session.commit()

            db.add_game_history(
                user_id=user_id,
                game_type="slots",
                bet_amount=bet_amount,
                result=result_str,
                multiplier=multiplier,
                payout=payout if won else 0,
                details=f"Result: {' | '.join(result)}"
            )

            return {
                "won": won,
                "symbols": result,
                "multiplier": multiplier,
                "payout": payout if won else 0,
                "new_balance": user.balance
            }
        finally:
            session.close()
