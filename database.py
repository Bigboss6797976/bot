"""
Database Models & Manager
"""
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import hashlib
import config

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    language = Column(String(10), default="en")
    balance = Column(Float, default=0.0)
    total_deposited = Column(Float, default=0.0)
    total_withdrawn = Column(Float, default=0.0)
    total_wagered = Column(Float, default=0.0)
    total_won = Column(Float, default=0.0)
    referral_code = Column(String(20), unique=True)
    referred_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    is_banned = Column(Boolean, default=False)
    vip_level = Column(Integer, default=0)

    referrals = relationship("User", backref="referrer", remote_side=[id])
    transactions = relationship("Transaction", back_populates="user")
    game_history = relationship("GameHistory", back_populates="user")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(20), nullable=False)  # deposit, withdraw, bet, win, bonus, referral
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USDT")
    status = Column(String(20), default="pending")  # pending, completed, failed, cancelled
    tx_hash = Column(String(200))
    address = Column(String(200))
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    user = relationship("User", back_populates="transactions")

class GameHistory(Base):
    __tablename__ = "game_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    game_type = Column(String(20), nullable=False)
    bet_amount = Column(Float, nullable=False)
    result = Column(String(20))  # win, loss, push
    multiplier = Column(Float, default=1.0)
    payout = Column(Float, default=0.0)
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="game_history")

class DailyBonus(Base):
    __tablename__ = "daily_bonus"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(String(10), nullable=False)  # YYYY-MM-DD
    claimed = Column(Boolean, default=False)
    streak = Column(Integer, default=0)

# Database Manager
class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(config.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def get_or_create_user(self, telegram_id, username=None, first_name=None, last_name=None):
        session = self.get_session()
        try:
            user = session.query(User).filter_by(telegram_id=telegram_id).first()
            if not user:
                referral_code = hashlib.md5(f"{telegram_id}{datetime.utcnow()}".encode()).hexdigest()[:8].upper()
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    referral_code=referral_code
                )
                session.add(user)
                session.commit()
            else:
                user.last_active = datetime.utcnow()
                session.commit()
            return user
        finally:
            session.close()

    def get_user(self, telegram_id):
        session = self.get_session()
        try:
            return session.query(User).filter_by(telegram_id=telegram_id).first()
        finally:
            session.close()

    def update_balance(self, user_id, amount, session=None):
        close_session = False
        if session is None:
            session = self.get_session()
            close_session = True
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                user.balance += amount
                session.commit()
                return user.balance
            return None
        finally:
            if close_session:
                session.close()

    def add_transaction(self, user_id, tx_type, amount, currency="USDT", status="pending", 
                        tx_hash=None, address=None, note=None):
        session = self.get_session()
        try:
            tx = Transaction(
                user_id=user_id,
                type=tx_type,
                amount=amount,
                currency=currency,
                status=status,
                tx_hash=tx_hash,
                address=address,
                note=note
            )
            session.add(tx)
            session.commit()
            return tx
        finally:
            session.close()

    def add_game_history(self, user_id, game_type, bet_amount, result, multiplier=1.0, payout=0.0, details=None):
        session = self.get_session()
        try:
            history = GameHistory(
                user_id=user_id,
                game_type=game_type,
                bet_amount=bet_amount,
                result=result,
                multiplier=multiplier,
                payout=payout,
                details=details
            )
            session.add(history)
            session.commit()
            return history
        finally:
            session.close()

    def get_leaderboard(self, limit=10):
        session = self.get_session()
        try:
            return session.query(User).order_by(User.total_won.desc()).limit(limit).all()
        finally:
            session.close()

    def get_referral_count(self, user_id):
        session = self.get_session()
        try:
            return session.query(User).filter_by(referred_by=user_id).count()
        finally:
            session.close()

db = DatabaseManager()
