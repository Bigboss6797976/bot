"""
🪙 Coin Flip Game Logic
"""
import random
from database import db

class CoinGame:
    def __init__(self):
        self.name = "coin"

    def flip(self, user_id, bet_amount, choice):
        """Flip the coin"""
        result = random.choice(["heads", "tails"])
        won = (result == choice)

        multiplier = 1.9 if won else 0
        payout = bet_amount * multiplier

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
                game_type="coin",
                bet_amount=bet_amount,
                result=result_str,
                multiplier=multiplier,
                payout=payout if won else 0,
                details=f"Choice: {choice}, Result: {result}"
            )

            return {
                "won": won,
                "result": result,
                "multiplier": multiplier,
                "payout": payout if won else 0,
                "new_balance": user.balance
            }
        finally:
            session.close()
