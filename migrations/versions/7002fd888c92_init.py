"""init

Revision ID: 7002fd888c92
Revises:
Create Date: 2022-08-20 23:48:07.025304

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7002fd888c92"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "patients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("dob", sa.Date(), nullable=False),
        sa.Column("address", sa.String(), nullable=True),
        sa.Column("phonenumber_1", sa.String(), nullable=True),
        sa.Column("phonenumber_2", sa.String(), nullable=True),
        sa.Column("phonenumber_3", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_patients_id"), "patients", ["id"], unique=False)
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("is_admin", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_table(
        "dispensers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("users_id", sa.Integer(), nullable=True),
        sa.Column("registration", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["users_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("registration"),
    )
    op.create_index(op.f("ix_dispensers_id"), "dispensers", ["id"], unique=False)
    op.create_table(
        "optometrists",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("users_id", sa.Integer(), nullable=True),
        sa.Column("registration", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["users_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("registration"),
    )
    op.create_index(op.f("ix_optometrists_id"), "optometrists", ["id"], unique=False)
    op.create_table(
        "exams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patients_id", sa.Integer(), nullable=True),
        sa.Column("optometrists_id", sa.Integer(), nullable=True),
        sa.Column(
            "date_created",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("date_updated", sa.DateTime(), nullable=True),
        sa.Column("history", sa.UnicodeText(), nullable=True),
        sa.Column("health", sa.UnicodeText(), nullable=True),
        sa.ForeignKeyConstraint(
            ["optometrists_id"],
            ["optometrists.id"],
        ),
        sa.ForeignKeyConstraint(
            ["patients_id"],
            ["patients.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_exams_id"), "exams", ["id"], unique=False)
    op.create_table(
        "specprescriptions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("exams_id", sa.Integer(), nullable=True),
        sa.Column("patients_id", sa.Integer(), nullable=True),
        sa.Column("optometrists_id", sa.Integer(), nullable=True),
        sa.Column("right_sphere", sa.Numeric(), nullable=True),
        sa.Column("right_cylinder", sa.Numeric(), nullable=True),
        sa.Column("right_axis", sa.Numeric(), nullable=True),
        sa.Column("right_add", sa.Numeric(), nullable=True),
        sa.Column("right_inter_add", sa.Numeric(), nullable=True),
        sa.Column("left_sphere", sa.Numeric(), nullable=True),
        sa.Column("left_cylinder", sa.Numeric(), nullable=True),
        sa.Column("left_axis", sa.Numeric(), nullable=True),
        sa.Column("left_add", sa.Numeric(), nullable=True),
        sa.Column("left_inter_add", sa.Numeric(), nullable=True),
        sa.ForeignKeyConstraint(
            ["exams_id"],
            ["exams.id"],
        ),
        sa.ForeignKeyConstraint(
            ["optometrists_id"],
            ["optometrists.id"],
        ),
        sa.ForeignKeyConstraint(
            ["patients_id"],
            ["patients.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_specprescriptions_id"), "specprescriptions", ["id"], unique=False
    )
    op.create_table(
        "specdispenses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patients_id", sa.Integer(), nullable=True),
        sa.Column("specprescriptions_id", sa.Integer(), nullable=True),
        sa.Column("users_id", sa.Integer(), nullable=True),
        sa.Column("optometrists_id", sa.Integer(), nullable=True),
        sa.Column("frame", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["optometrists_id"],
            ["optometrists.id"],
        ),
        sa.ForeignKeyConstraint(
            ["patients_id"],
            ["patients.id"],
        ),
        sa.ForeignKeyConstraint(
            ["specprescriptions_id"], ["specprescriptions.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["users_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_specdispenses_id"), "specdispenses", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_specdispenses_id"), table_name="specdispenses")
    op.drop_table("specdispenses")
    op.drop_index(op.f("ix_specprescriptions_id"), table_name="specprescriptions")
    op.drop_table("specprescriptions")
    op.drop_index(op.f("ix_exams_id"), table_name="exams")
    op.drop_table("exams")
    op.drop_index(op.f("ix_optometrists_id"), table_name="optometrists")
    op.drop_table("optometrists")
    op.drop_index(op.f("ix_dispensers_id"), table_name="dispensers")
    op.drop_table("dispensers")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_patients_id"), table_name="patients")
    op.drop_table("patients")
    # ### end Alembic commands ###
