"""create phase 1 tables"""
from alembic import op
import sqlalchemy as sa

revision = "0001_phase1"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("sports", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("code", sa.String(32), nullable=False), sa.Column("name", sa.String(100), nullable=False), sa.UniqueConstraint("code"))
    op.create_index("ix_sports_code", "sports", ["code"], unique=False)
    op.create_table("fixtures", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("provider_id", sa.Integer(), nullable=False), sa.Column("sport", sa.String(32), nullable=False), sa.Column("league_name", sa.String(150)), sa.Column("home_team", sa.String(150), nullable=False), sa.Column("away_team", sa.String(150), nullable=False), sa.Column("kickoff_at", sa.DateTime(timezone=True), nullable=False), sa.Column("status", sa.String(32)), sa.Column("home_form", sa.Float()), sa.Column("away_form", sa.Float()), sa.Column("home_goals_avg", sa.Float()), sa.Column("away_goals_avg", sa.Float()), sa.Column("raw_json", sa.Text()), sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=False), sa.UniqueConstraint("provider_id"))
    op.create_index("ix_fixtures_provider_id", "fixtures", ["provider_id"], unique=False)
    op.create_index("ix_fixtures_sport", "fixtures", ["sport"], unique=False)
    op.create_index("ix_fixtures_kickoff_at", "fixtures", ["kickoff_at"], unique=False)
    op.create_index("ix_fixtures_fetched_at", "fixtures", ["fetched_at"], unique=False)
    op.create_table("predictions", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("fixture_id", sa.Integer(), sa.ForeignKey("fixtures.id", ondelete="CASCADE"), nullable=False), sa.Column("market", sa.String(50), nullable=False), sa.Column("selection", sa.String(100), nullable=False), sa.Column("confidence", sa.Float(), nullable=False), sa.Column("explanation", sa.Text(), nullable=False), sa.Column("provider", sa.String(50), nullable=False), sa.Column("engine_version", sa.String(50), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.UniqueConstraint("fixture_id", "market", "engine_version"))
    op.create_index("ix_predictions_fixture_id", "predictions", ["fixture_id"], unique=False)

def downgrade():
    op.drop_table("predictions")
    op.drop_table("fixtures")
    op.drop_table("sports")
