from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Float, Index, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.db.database import Base

# ==========================
# Core IPL Datasets Models
# ==========================

class Team(Base):
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String(255), nullable=False)
    team_name_short = Column(String(50))
    image_url = Column(Text)

    def to_dict(self):
        return {
            "team_id": self.team_id,
            "team_name": self.team_name,
            "team_name_short": self.team_name_short,
            "image_url": self.image_url
        }


class PlayerInfo(Base):
    __tablename__ = "player_info"

    player_id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String(255), nullable=False, index=True)
    bat_style = Column(String(100))
    bowl_style = Column(String(100))
    field_pos = Column(String(100))
    player_full_name = Column(String(255))
    player_name2 = Column(String(255))
    player_image = Column(Text)

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "player_name": self.player_name,
            "bat_style": self.bat_style,
            "bowl_style": self.bowl_style,
            "field_pos": self.field_pos,
            "player_full_name": self.player_full_name,
            "player_image": self.player_image
        }


class IplMatch(Base):
    __tablename__ = "ipl_match"

    match_id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, index=True)
    balls_per_over = Column(Integer, default=6)
    city = Column(String(100))
    match_date = Column(String(100))
    event_name = Column(String(255))
    match_number = Column(Integer)
    gender = Column(String(20))
    match_type = Column(String(100))
    format = Column(String(50))
    overs = Column(Integer)
    season = Column(String(50), index=True)
    team_type = Column(String(50))
    venue = Column(String(255), index=True)
    toss_winner = Column(String(255))
    team1 = Column(String(255))
    team2 = Column(String(255))
    toss_decision = Column(String(50))
    match_winner = Column(String(255))
    win_by_runs = Column(Integer)
    win_by_wickets = Column(Integer)
    player_of_match = Column(Integer, ForeignKey("player_info.player_id"), nullable=True)
    result = Column(String(50))
    stage = Column(String(100))

    # Relationship to player of the match info
    mvp = relationship("PlayerInfo", foreign_keys=[player_of_match])

    def to_dict(self):
        return {
            "match_id": self.match_id,
            "season_id": self.season_id,
            "city": self.city,
            "match_date": self.match_date,
            "venue": self.venue,
            "team1": self.team1,
            "team2": self.team2,
            "toss_winner": self.toss_winner,
            "toss_decision": self.toss_decision,
            "match_winner": self.match_winner,
            "win_by_runs": self.win_by_runs,
            "win_by_wickets": self.win_by_wickets,
            "player_of_match": self.player_of_match,
            "result": self.result,
            "stage": self.stage
        }


class BallByBall(Base):
    __tablename__ = "ball_by_ball"

    # Composite primary key for delivery representation
    match_id = Column(Integer, ForeignKey("ipl_match.match_id"), primary_key=True)
    innings = Column(Integer, primary_key=True)
    over_number = Column(Integer, primary_key=True)
    ball_number = Column(Integer, primary_key=True)
    
    season_id = Column(Integer)
    batter = Column(String(255), index=True)
    bowler = Column(String(255), index=True)
    non_striker = Column(String(255))
    team_batting = Column(String(255))
    team_bowling = Column(String(255))
    batter_runs = Column(Integer)
    extras = Column(Integer)
    total_runs = Column(Integer)
    batsman_type = Column(String(100))
    bowler_type = Column(String(100))
    player_out = Column(String(255), nullable=True)
    fielders_involved = Column(Text, nullable=True)
    is_wicket = Column(Boolean, default=False)
    is_wide_ball = Column(Boolean, default=False)
    is_no_ball = Column(Boolean, default=False)
    is_leg_bye = Column(Boolean, default=False)
    is_bye = Column(Boolean, default=False)
    is_penalty = Column(Boolean, default=False)
    wide_ball_runs = Column(Integer, default=0)
    no_ball_runs = Column(Integer, default=0)
    leg_bye_runs = Column(Integer, default=0)
    bye_runs = Column(Integer, default=0)
    penalty_runs = Column(Integer, default=0)
    wicket_kind = Column(String(100), nullable=True)
    is_super_over = Column(Boolean, default=False)

    # Indexes for optimization of analytics queries
    __table_args__ = (
        Index("idx_match_innings", "match_id", "innings"),
        Index("idx_batter_bowler", "batter", "bowler"),
    )


# ==========================
# User & Authentication Models
# ==========================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    query_history = relationship("QueryHistory", back_populates="user", cascade="all, delete-orphan")
    saved_queries = relationship("SavedQuery", back_populates="user", cascade="all, delete-orphan")


class QueryHistory(Base):
    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    natural_language_query = Column(Text, nullable=False)
    generated_sql = Column(Text, nullable=True)
    execution_time_ms = Column(Integer, nullable=True)
    is_success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="query_history")


class SavedQuery(Base):
    __tablename__ = "saved_queries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    natural_language_query = Column(Text, nullable=False)
    generated_sql = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="saved_queries")
