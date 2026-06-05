"""
🎡 Roulette Game Logic
"""
import random
from database import db

class RouletteGame:
    def __init__(self):
        self.name = "roulette"
        # European roulette numbers
        self.numbers = list(range(37))  # 0-36
        self.colors = self._init_colors()

    def _init_colors(self):
        colors = {}
        red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        for n in self.numbers:
            if n == 0:
                colors[n] = "green"
            elif n in red_numbers:
                colors[n] = "red"
            else:
                colors[n] = "black"
        return colors

    def spin(self, user_id, bet_amount, bet_type, bet_value):
        """Spin roulette"""
        result_number = random.choice(self.numbers)
        result_color = self.colors[result_number]

        won = False
        multiplier = 0

        if bet_type == "number":
            if result_number == bet_value:
                multiplier = 35
                won = True
        elif bet_type == "color":
            if result_color == bet_value:
                multiplier = 1.9
                won = True
        elif bet_type == "even_odd":
            if result_number == 0:
                won = False
            elif bet_value == "even" and result_number % 2 == 0:
                multiplier = 1.9
                won = True
            elif bet_value == "odd" and result_number % 2 == 1:
                multiplier = 1.9
                won = True

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
                game_type="roulette",
                bet_amount=bet_amount,
                result=result_str,
                multiplier=multiplier,
                payout=payout if won else 0,
                details=f"Number: {result_number}, Color: {result_color}"
            )

            return {
                "won": won,
                "number": result_number,
                "color": result_color,
                "multiplier": multiplier,
                "payout": payout if won else 0,
                "new_balance": user.balance
            }
        finally:
            session.close()
