"""
🎲 Dice Game Logic
"""
import random
from database import db
from locales.i18n import get_text

class DiceGame:
    def __init__(self):
        self.name = "dice"

    def play(self, user_id, bet_amount, chosen_number=None):
        """Play dice game"""
        result = random.randint(1, 6)

        if chosen_number:
            # Number bet (1-6)
            if result == chosen_number:
                multiplier = 5.8
                payout = bet_amount * multiplier
                won = True
            else:
                multiplier = 0
                payout = 0
                won = False
        else:
            # Over/Under bet
            if result >= 4:
                multiplier = 1.9
                payout = bet_amount * multiplier
                won = True
            else:
                multiplier = 0
                payout = 0
                won = False

        # Update user balance and stats
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

            # Add game history
            db.add_game_history(
                user_id=user_id,
                game_type="dice",
                bet_amount=bet_amount,
                result=result_str,
                multiplier=multiplier,
                payout=payout if won else 0,
                details=f"Result: {result}, Chosen: {chosen_number or 'over/under'}"
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
